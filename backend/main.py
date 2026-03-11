from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router

# ── App Setup ────────────────────────────────────────────────────
app = FastAPI(
    title="APOA — Autonomous Personal Operations Agent",
    description="An AI agent that executes real-world tasks autonomously using LangGraph, LangChain, and Groq LLaMA.",
    version="1.0.0"
)

# ── CORS (allows frontend to talk to backend) ────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Include Routes ───────────────────────────────────────────────
app.include_router(router, prefix="/api/v1")

# ── Root ─────────────────────────────────────────────────────────
@app.get("/")
async def root():
    return {
        "agent": "APOA — Autonomous Personal Operations Agent",
        "status": "running ✅",
        "docs": "/docs",
        "endpoints": {
            "chat": "/api/v1/chat",
            "task": "/api/v1/task",
            "history": "/api/v1/history",
            "health": "/api/v1/health"
        }
    }