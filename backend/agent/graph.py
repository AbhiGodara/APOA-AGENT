from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.memory import ConversationBufferMemory
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import GROQ_API_KEY, MODEL_NAME
from agent.tools import all_tools
# from memory.short_term import get_short_term_memory
from memory.long_term import get_or_create_vectorstore, save_to_memory, search_memory

# ── LLM Setup ───────────────────────────────────────────────────
llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model_name=MODEL_NAME,
    temperature=0,
)

llm_with_tools = llm.bind_tools(all_tools)

# ── ReAct Prompt ─────────────────────────────────────────────────
prompt = ChatPromptTemplate.from_messages([
    ("system",
    "You are APOA — Autonomous Personal Operations Agent.\n\n"
    "STRICT RULES:\n"
    "1. Use ONLY ONE tool per response\n"
    "2. After tool result, give Final Answer immediately\n"
    "3. Never call multiple tools for one request\n\n"
    "TOOL SELECTION — follow EXACTLY:\n"
    "- User says hello/hi/their name/introduction → general_response\n"
    "- User asks about current events/news/who is X → tavily_search\n"
    "- User asks for math/calculation → calculator\n"
    "- User asks what day/time/date it is → datetime_tool\n"
    "- User asks to draft/send an email → email_draft_tool\n"
    "- User asks to set/save a reminder → reminder_tool\n"
    "- Anything else → general_response\n\n"
    "NEVER use email_draft_tool unless user explicitly says 'draft email' or 'send email'.\n"
    "NEVER use reminder_tool unless user explicitly says 'remind me' or 'set reminder'."
    ),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# ── Agent Builder ────────────────────────────────────────────────
def build_agent():
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="output"
    )
    vectorstore = get_or_create_vectorstore()

    agent = create_tool_calling_agent(
        llm=llm_with_tools,
        tools=all_tools,
        prompt=prompt,
    )

    agent_executor = AgentExecutor(
        agent=agent,
        tools=all_tools,
        memory=memory,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=5,
        max_execution_time=30,
        return_intermediate_steps=True,
    )

    return agent_executor, vectorstore


# ── Main Run Function ────────────────────────────────────────────
async def run_agent(user_input: str, agent_executor, vectorstore) -> dict:
    long_term_context = search_memory(vectorstore, user_input)

    try:
        result = await agent_executor.ainvoke({
            "input": f"{user_input}\n\nPast context: {long_term_context}",
        })

        output = result.get("output", "")
        intermediate_steps = result.get("intermediate_steps", [])
        tools_used = [step[0].tool for step in intermediate_steps]

        # ── If email or reminder tool was used, return tool output directly ──
        for step in intermediate_steps:
            tool_name = step[0].tool
            tool_output = step[1]
            if tool_name in ["email_draft_tool", "reminder_tool"]:
                output = str(tool_output)  # use raw tool output, skip LLM summary
                break

        save_to_memory(
            vectorstore,
            f"User: {user_input} | Agent: {output[:200]}",
            metadata={"type": "task"}
        )

        return {
            "response": output,
            "tools_used": tools_used,
            "memory_updated": True,
            "steps_taken": len(intermediate_steps)
        }

    except Exception as e:
        return {
            "response": f"Agent error: {str(e)}",
            "tools_used": [],
            "memory_updated": False,
            "steps_taken": 0
        }