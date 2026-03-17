# 🤖 APOA — Autonomous Personal Operations Agent

An autonomous AI agent that executes real-world tasks by orchestrating tools, managing memory, and reasoning step-by-step — without human intervention.

> Built to demonstrate production-grade agentic AI architecture using LangChain, Groq LLaMA, and Streamlit.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-red?style=for-the-badge&logo=streamlit)](https://abhishek-APOA-Agent.streamlit.app/)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?style=for-the-badge&logo=github)](https://github.com/AbhiGodara/APOA-AGENT)

---

## 🎬 Demo

| Task | Tools Used |
|---|---|
| "What day is it and what's 10 days from now?" | `datetime_tool` |
| "Calculate compound interest at 8% for 3 years" | `calculator` |
| "Search latest AI agent frameworks in 2026" | `tavily_search` |
| "Draft an email to abhishekgodara032@gmail.com about meeting" | `email_draft_tool` |
| "Remind me to push code tonight" | `reminder_tool` |

---

## 🏗️ Architecture

**Request Flow:**

```
User Request
      ↓
AgentExecutor (LangChain)
      ↓
Tool Router — selects from 6 tools autonomously
      ↓
 ┌─────────────┬─────────────┬─────────────┬─────────────┬─────────────┐
 ↓             ↓             ↓             ↓             ↓             ↓
Web Search  Wikipedia   Calculator   DateTime     Email       Reminder
      ↓
Dual-Layer Memory
      ├── Short-term : ConversationBufferMemory  (session context)
      └── Long-term  : FAISS Vector Store        (persistent across sessions)
      ↓
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
| Frontend | Streamlit |
| Web Search | Tavily API |

---

## 📁 Project Structure

```
apoa-agent/
│
├── app.py                        # Streamlit entry point
│
├── backend/
│   ├── agent/
│   │   ├── graph.py              # Agent orchestration logic
│   │   └── tools.py              # 6 tool definitions
│   │
│   ├── memory/
│   │   ├── short_term.py         # ConversationBufferMemory
│   │   └── long_term.py          # FAISS vector store
│   │
│   └── api/
│       └── routes.py             # FastAPI async routes
│
├── config/
│   └── settings.py               # Environment variables
│
├── .env                          # API keys (not committed)
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

**1. Clone the repo**
```bash
git clone https://github.com/AbhiGodara/APOA-AGENT.git
cd apoa-agent
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set up environment variables**
```bash
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

**4. Run the app**
```bash
streamlit run app.py
```

**5. Open in browser**
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

## 👨‍💻 Author

**Abhishek Godara**
B.Tech CSE (AI & ML) — IIIT Nagpur

[![LinkedIn](https://img.shields.io/badge/LinkedIn-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/abhishek-godara-a82a1b2a0/)
[![GitHub](https://img.shields.io/badge/GitHub-black?style=flat&logo=github)](https://github.com/AbhiGodara)
[![Kaggle](https://img.shields.io/badge/Kaggle-blue?style=flat&logo=kaggle)](https://www.kaggle.com/abhishekgodara)