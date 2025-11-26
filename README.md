# 🚀 Modular Agent System with Google Gemini — Planner → Decomposer → Action Agents → Combiner

![Project Banner](screenshots/blog_screenshot.png)

## ⭐ Tagline
A complete modular agent pipeline enhanced with Google Gemini for reasoning, planning, and content generation.

## 📌 Project Description
This project implements a multi-stage agent architecture using an ER-diagram-based workflow.  
A user request moves through:

1. **Planner** → Creates high-level task plan  
2. **Task Decomposer** → Breaks plan into actionable steps  
3. **Action Agents** → Each agent performs one clear atomic action  
4. **Combiner** → Merges all agent outputs into a final structured response  
5. **Gemini LLM** → Powers reasoning, text generation, and decision steps  

This system demonstrates clean modular design + real LLM integration using the **Google Gemini API**.

---

# 🧠 Architecture Overview  
```
User Input
    ↓
Gemini Model (for reasoning / planning)
    ↓
Planner
    ↓
Task Decomposer
    ↓
Action Agents
    ↓
Combiner
    ↓
Final Output (JSON)
```

Gemini enhances the system by:
- Generating plans
- Refining decomposed steps
- Assisting action agents
- Producing summaries or structured outputs

---

# 🤖 Model Used — Google Gemini  
**Model:** `gemini-1.5-flash`  
(You may also choose `gemini-1.5-pro` depending on complexity)

Gemini is used for:
- Task planning  
- Reasoning  
- Text generation  
- Summaries  
- Sample code generation  

**Environment variable (never hardcode):**
```
GEMINI_API_KEY=your_api_key_here
```

Configured through `.env` (not uploaded).  
Shared through `.env.example`.

---

# 📂 Project Structure
```
project/
├─ planner.py
├─ decomposer.py
├─ combiner.py
├─ run_agent.py
│
├─ agents/
│  ├─ agent_reader.py
│  ├─ agent_processor.py
│  └─ agent_writer.py
│
├─ gemini/
│  ├─ test_gemini_call.py
│  ├─ agentic_agent_demo_gemini.py
│  ├─ find_working_model.py
│  └─ list_models.py
│
├─ outputs/
│  └─ final_output.json
│
├─ screenshots/
│  └─ blog_screenshot.png
│
├─ .env.example
├─ .gitignore
└─ README.md
```

---

# ⚙️ Environment Setup
Install dependencies:
```bash
pip install google-generativeai python-dotenv
```

Create `.env` (local only — do NOT upload):
```
GEMINI_API_KEY="your_real_api_key_here"
```

Create `.env.example` (to upload):
```
GEMINI_API_KEY=your_api_key_here
```

---

# 🚀 Running the Project
### 1) Run core agent pipeline:
```bash
python run_agent.py
```

Final output appears in:
```
outputs/final_output.json
```

### 2) Test Gemini model:
```bash
python gemini/test_gemini_call.py
```

### 3) List all Gemini models:
```bash
python gemini/list_models.py
```

---

# 🔍 Component Breakdown

## 1️⃣ Gemini Integration  
Used for:
- High-level reasoning  
- Tasks planning  
- Content generation  
- Summaries  
- Error explanation

Example call:
```python
import google.generativeai as genai
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Create the plan for this task")
```

---

## 2️⃣ Planner  
Uses either:
- Your Python logic, or  
- Gemini-enhanced reasoning  

Generates steps like:
```
["read_input", "process_data", "summarize"]
```

---

## 3️⃣ Task Decomposer  
Breaks each step into smaller actions:
```
"process_data" → ["clean", "analyze"]
```

---

## 4️⃣ Action Agents
### 🟦 Reader Agent  
Loads or extracts input data.

### 🟩 Processor Agent  
Processes or transforms data.

### 🟧 Writer Agent  
Formats text or structured data.

Each agent returns:
```
{"step":"clean","result":"success"}
```

---

## 5️⃣ Combiner  
Produces the final well-structured output:
```json
{
  "status": "complete",
  "steps": [...],
  "final_result": "summary text..."
}
```

---

## 📸 Screenshots

![Goal Prompt](screenshots/02_agent_goal_prompt.png)

### 🟩 Planner Output
![Planner Output](screenshots/03_planner_output.png)

### 🟧 Final Result JSON
![Final Result](screenshots/01_result_output.png)


# 🔒 Security  
- `.env` is **never** uploaded.  
- `.gitignore` blocks sensitive files.  
- API keys must stay local only.  
- `.env.example` safely shows required variables.

---

# 🙏 Acknowledgements  
Special thanks to **Imarticus Learning** and mentors for guidance and support throughout the development of this project.

---

# 👤 Author  
**Akshatha**  
Data Science Intern — Imarticus Learning

le Gemini — includes Planner, Decomposer, Action Agents, Combiner, and LLM reasoning. Clean, scalable, and production-ready.
