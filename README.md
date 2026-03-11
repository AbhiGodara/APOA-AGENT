# 🤖 APOA — Autonomous Personal Operations Agent

An autonomous AI agent that executes real-world tasks by orchestrating tools, managing memory, and reasoning step-by-step — without human intervention.

> Built to demonstrate production-grade agentic AI architecture using LangChain, Groq LLaMA, and FastAPI.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-red?style=for-the-badge&logo=streamlit)](https://abhishek-APOA-Agent.streamlit.app/)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?style=for-the-badge&logo=github)](https://github.com/AbhiGodara/APOA-AGENT)
```

---

## 🎬 Demo

| Task | Tools Used |
|---|---|
| "What day is it and what's 10 days from now?" | `datetime_tool` |
| "Calculate compound interest at 8% for 3 years" | `calculator` |
| "Search latest AI agent frameworks in 2026" | `tavily_search` |
| "Draft an email to rahul@gmail.com about meeting" | `email_draft_tool` |
| "Remind me to push code tonight" | `reminder_tool` |

---

## 🏗️ Architecture
```
User Request
     │
     ▼
FastAPI Backend (Async)
     │
     ▼
AgentExecutor (LangChain)
     │
     ▼
Tool Router — selects from 6 tools autonomously
 ┌──────────┬──────────┬───────────┬──────────┬──────────┐
 ▼          ▼          ▼           ▼          ▼
Web      Wikipedia  Calculator  DateTime   Email &
Search              Tool        Tool       Reminder
     │
     ▼
Dual-Layer Memory
├── Short-term: ConversationBufferMemory (session context)
└── Long-term:  FAISS Vector Store (persistent across sessions)
     │
     ▼
Response to User
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| LLM | Groq LLaMA 3.3 70B |
| Agent Framework | LangChain AgentExecutor |
| Tool Orchestration | LangChain Tool Calling |
| Short-term Memory | ConversationBufferMemory |
| Long-term Memory | FAISS + HuggingFace Embeddings |
| Backend | FastAPI (Async) |
| Frontend | Streamlit |
| Web Search | Tavily API |

---

## 📁 Project Structure
```
apoa-agent/
│
├── backend/
│   ├── main.py                  # FastAPI entry point
│   │
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── graph.py             # LangGraph agent workflow
│   │   ├── planner.py           # Task decomposition logic
│   │   └── tools.py             # All 5 tools defined here
│   │
│   ├── memory/
│   │   ├── __init__.py
│   │   ├── short_term.py        # ConversationBufferMemory
│   │   └── long_term.py         # FAISS vector store
│   │
│   └── api/
│       ├── __init__.py
│       └── routes.py            # Async FastAPI routes
│
├── frontend/
│   └── app.py                   # Streamlit UI
│
├── config/
│   └── settings.py              # All env vars loaded here
│
├── .env                         # API keys
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/AbhiGodara/APOA-AGENT.git
cd apoa-agent
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
```bash
# Create .env file in backend/
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

### 4. Run the backend
```bash
cd backend
uvicorn main:app --host 127.0.0.1 --port 8001
```

### 5. Run the frontend
```bash
streamlit run frontend/app.py
```

### 6. Open in browser
```
http://localhost:8501
```

---

## 🧠 How the Agent Reasons
```
User: "Search latest AI frameworks and draft an email about them"

Step 1 → Agent picks: tavily_search
Step 2 → Gets results, decides to also use: email_draft_tool
Step 3 → Drafts complete email with search results
Step 4 → Saves task to long-term memory
Step 5 → Returns full response to user
```

---

## 📝 Resume Highlights

- Engineered a goal-driven autonomous agent using LangChain's AgentExecutor with dynamic tool selection across 6 integrated APIs
- Implemented dual-layer memory architecture combining ConversationBufferMemory for session context and FAISS vector store for long-term knowledge persistence
- Built async FastAPI backend exposing agent capabilities via RESTful endpoints with complex JSON request/response schemas
- Integrated Groq LLaMA 3.3 70B with tool calling for autonomous multi-step task execution without human intervention

---

## 🔮 Future Improvements

- [ ] Connect real Gmail API for actual email sending
- [ ] Add Google Calendar integration
- [ ] React + TypeScript frontend
- [ ] Multi-agent architecture (Planner + Executor agents)
- [ ] Docker containerization

---

## 👨‍💻 Author

**Abhishek Godara**  
B.Tech CSE (AI & ML) — IIIT Nagpur  
[LinkedIn](https://www.linkedin.com/in/abhishek-godara-a82a1b2a0/) | [GitHub](https://github.com/AbhiGodara) | [Kaggle](https://www.kaggle.com/abhishekgodara)