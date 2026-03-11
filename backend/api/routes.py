from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from agent.graph import build_agent, run_agent

router = APIRouter()

# Build agent once when server starts
agent_executor, vectorstore = build_agent()

# ── Request/Response Schemas ─────────────────────────────────────
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    tools_used: list
    memory_updated: bool
    steps_taken: int

class HistoryResponse(BaseModel):
    history: list

# ── Routes ───────────────────────────────────────────────────────

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint.
    Send a goal → agent executes it autonomously.
    """
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    try:
        result = await run_agent(
            user_input=request.message,
            agent_executor=agent_executor,
            vectorstore=vectorstore
        )
        return ChatResponse(**result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/task", response_model=ChatResponse)
async def execute_task(request: ChatRequest):
    """
    Task execution endpoint.
    Same as /chat but semantically for multi-step tasks.
    """
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Task cannot be empty")

    try:
        result = await run_agent(
            user_input=f"Execute this task step by step: {request.message}",
            agent_executor=agent_executor,
            vectorstore=vectorstore
        )
        return ChatResponse(**result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history", response_model=HistoryResponse)
async def get_history():
    """
    Returns conversation history from short-term memory.
    """
    try:
        memory_vars = agent_executor.memory.load_memory_variables({})
        messages = memory_vars.get("chat_history", [])
        history = [
            {"role": m.type, "content": m.content}
            for m in messages
        ]
        return HistoryResponse(history=history)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "APOA agent is running ✅"}