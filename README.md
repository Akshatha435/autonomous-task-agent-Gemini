# 🚀 Modular Agent System — Planner → Decomposer → Action Agents → Combiner

![Project Banner](screenshots/blog_screenshot.png)

## ⭐ Tagline
A clean and modular agent pipeline built from an ER diagram — structured, scalable, and simple to extend.

## 📌 Project Description
This project implements a complete multi-stage agent workflow. A single user input flows through a **Planner**, a **Task Decomposer**, multiple **Action Agents**, and finally a **Combiner** that produces a structured final output.

Built with clarity and modularity in mind, the system is ideal for learning agent architecture and workflow-based automation.

---

# 🧠 Architecture Overview
```
User Input
    ↓
Planner
    ↓
Task Decomposer
    ↓
Action Agents (Reader / Processor / Writer)
    ↓
Combiner
    ↓
Final Output (JSON)
```

This design keeps tasks organized, easy to debug, and highly expandable.

---

# 📂 Project Structure
```
project/
├─ planner.py
├─ decomposer.py
├─ combiner.py
├─ run_agent.py
├─ agents/
│  ├─ agent_reader.py
│  ├─ agent_processor.py
│  └─ agent_writer.py
├─ outputs/
│  └─ final_output.json
├─ screenshots/
│  └─ blog_screenshot.png
└─ README.md
```

---

# 🚀 How to Run
```bash
# clone and run
git clone <your-repo-url>
cd project
python run_agent.py
```

The final structured output will be generated at:
```
outputs/final_output.json
```

---

# 🔍 Component Breakdown

## 1️⃣ Planner
- Receives the main user instruction and produces a sequence of subtasks (e.g. `["read_input","process_data","generate_summary"]`).

## 2️⃣ Task Decomposer
- Breaks each Planner step into precise, executable actions (e.g. `process_data -> ["clean","analyze"]`).

## 3️⃣ Action Agents
- **Reader Agent**: loads/parses input  
- **Processor Agent**: performs transformations/logic  
- **Writer Agent**: formats results for output  
Each agent returns a JSON-like dict: `{"step":"clean","result":"success"}`.

## 4️⃣ Combiner
- Merges agent outputs, removes inconsistencies, and builds the final result:
```json
{
  "status": "complete",
  "steps": [...],
  "final_result": "summary text here"
}
```

---

# 📸 Screenshots
Place your screenshot(s) in the `/screenshots` folder. An example image is already referenced above as:
```
screenshots/blog_screenshot.png
```
(Replace that file with your actual screenshot file. Keep the same filename or update the image link in this README.)

---

# 🔒 Security
- No sensitive credentials in the repo.  
- Do not commit `.env` or API keys.  
- Safe to upload publicly.

---

# 🙏 Acknowledgements
Special thanks to **Imarticus Learning** and mentors for guidance.

---

# 👤 Author
**Acchu**  
Data Science Intern — Imarticus Learning
