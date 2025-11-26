# agentic_agent_demo_gemini.py
# ------------------------------------------
# Minimal working Agentic AI pipeline using Google Gemini
# Planner → Task Decomposer → Action Agents → Combiner
# ------------------------------------------

import os
import json
import time
from dataclasses import dataclass, asdict
from typing import Any, Dict, List

import pandas as pd
from dotenv import load_dotenv
from tqdm import tqdm

# ======================================
# LOAD ENV + GEMINI SETUP
# ======================================

# Use the official google-genai SDK import pattern
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise Exception("ERROR: No Gemini API key found! Add it to .env")

# Create the client (explicitly pass the key)
client = genai.Client(api_key=API_KEY)
MODEL_NAME = "gemini-2.5-flash"
  # change if necessary



# ======================================
# HELPER: Gemini LLM wrapper
# ======================================

def llm_complete_genai(prompt: str, max_tokens: int = 300) -> str:
    """
    Simple, robust wrapper for the google-genai client.
    Uses only the parameters we know are supported in your SDK version:
      - model (string)
      - contents (string)
    We avoid passing optional keyword args (like max_output_tokens) which your SDK rejected.
    """
    try:
        # NOTE: use 'contents' only (no max_output_tokens argument here)
        resp = client.models.generate_content(model=MODEL_NAME, contents=prompt)

        # Newer SDKs expose 'text' attribute
        if hasattr(resp, "text") and resp.text:
            return resp.text.strip()

        # If it's a complex object, try to extract candidate content
        # Fallback to stringified object if nothing else
        try:
            # some SDK responses include .candidates[0].content
            cand = getattr(resp, "candidates", None)
            if cand and len(cand) > 0:
                first = cand[0]
                # try attributes or dict keys
                out = getattr(first, "content", None) or getattr(first, "text", None) or (first.get("content") if isinstance(first, dict) else None)
                if out:
                    return out.strip()
        except Exception:
            pass

        return str(resp)

    except Exception as e:
        # Print full traceback so you can see it in the terminal
        import traceback
        traceback.print_exc()
        # return an audit-safe message
        return f"[LLM ERROR] {type(e).__name__}: {e}"


# ======================================
# AUDIT LOGGER
# ======================================

LOG_FILE = "agent_audit_log.jsonl"

def log_action(record: Dict[str, Any]):
    """Append an action record to audit log."""
    record["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


# ======================================
# DATACLASS STRUCTS
# ======================================

@dataclass
class Task:
    id: int
    name: str
    payload: Dict[str, Any]
    status: str = "pending"

@dataclass
class AgentResponse:
    task_id: int
    agent: str
    status: str
    output: Any
    meta: Dict[str, Any]


# ======================================
# 1) PLANNER AGENT
# ======================================

def planner_agent(user_goal: str) -> List[Task]:
    """Use Gemini to break the goal into small tasks."""
    prompt = f"""
Break down the following user goal into a JSON array of 3–6 atomic tasks.
Respond ONLY with JSON:
[{{"name":"...", "notes":"..."}}]

Goal: {user_goal}
"""
    raw = llm_complete_genai(prompt, max_tokens=350)

    try:
        tasks_json = json.loads(raw)
    except:
        # fallback if JSON fails
        tasks_json = [{"name": user_goal, "notes": ""}]

    tasks = [
        Task(id=i+1, name=t.get("name",""), payload={"notes":t.get("notes","")})
        for i, t in enumerate(tasks_json)
    ]

    log_action({"component":"planner", "goal":user_goal, "tasks":[asdict(t) for t in tasks]})
    return tasks


# ======================================
# 2) ACTION AGENTS
# ======================================

def search_agent(task: Task) -> AgentResponse:
    q = task.name
    prompt = f"Give me 3 short, factual bullets for: {q}"
    out = llm_complete_genai(prompt)
    log_action({"agent":"search", "task":asdict(task), "output":out})
    return AgentResponse(task.id, "search_agent", "ok", out, {})

def summarization_agent(task: Task) -> AgentResponse:
    text = task.payload.get("notes") or task.name
    prompt = f"Summarize this in 3 bullets:\n\n{text}"
    out = llm_complete_genai(prompt)
    log_action({"agent":"summary", "task":asdict(task), "output":out})
    return AgentResponse(task.id, "summarization_agent", "ok", out, {})

def email_agent(task: Task) -> AgentResponse:
    body = task.payload.get("body") or task.name
    prompt = f"Write a 4-line professional email based on:\n\n{body}"
    out = llm_complete_genai(prompt)
    log_action({"agent":"email", "task":asdict(task), "output":out})
    return AgentResponse(task.id, "email_agent", "ok", out, {})


# Map task keywords to agents
ACTION_MAP = {
    "search": search_agent,
    "summarize": summarization_agent,
    "email": email_agent,
}


def classify_task(task: Task) -> str:
    """Simple rule-based classifier."""
    name = task.name.lower()

    if "search" in name or "find" in name or "collect" in name:
        return "search"
    if "summarize" in name or "insight" in name or "bullet" in name:
        return "summarize"
    if "email" in name or "draft" in name:
        return "email"

    # default to summary
    return "summarize"


# ======================================
# 3) COMBINER
# ======================================

def combine_responses(responses: List[AgentResponse]) -> Dict[str, Any]:
    combined = {
        "summaries": [],
        "emails": [],
        "raw": []
    }

    for r in responses:
        combined["raw"].append({"agent":r.agent, "output":r.output})

        if r.agent in ("search_agent","summarization_agent"):
            combined["summaries"].append(r.output)

        if r.agent == "email_agent":
            combined["emails"].append(r.output)

    log_action({"component":"combiner", "final":combined})
    return combined


# ======================================
# 4) MAIN PIPELINE
# ======================================

def run_agent_pipeline(user_goal: str):
    tasks = planner_agent(user_goal)
    responses = []

    for t in tqdm(tasks, desc="Running tasks"):
        tag = classify_task(t)
        func = ACTION_MAP.get(tag)

        try:
            res = func(t)
        except Exception as e:
            res = AgentResponse(t.id, tag, "error", str(e), {})
            log_action({"error":str(e), "task":asdict(t)})

        responses.append(res)

    final = combine_responses(responses)

    out_file = f"result_{int(time.time())}.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump({"goal":user_goal, "final":final}, f, indent=2, ensure_ascii=False)

    print("\nFinal result saved to:", out_file)
    return out_file, final


# ======================================
# 5) ENTRY POINT
# ======================================

if __name__ == "__main__":
    goal = input("Enter your goal for the agent: ").strip()
    run_agent_pipeline(goal)
