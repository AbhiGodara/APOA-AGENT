from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langchain_classic.agents import AgentExecutor
from langchain_core.prompts import PromptTemplate
from langchain_classic.memory import ConversationBufferMemory
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import GROQ_API_KEY, MODEL_NAME
from agent.tools import all_tools
from memory.short_term import get_short_term_memory
from memory.long_term import get_or_create_vectorstore, save_to_memory, search_memory

# ── LLM Setup ───────────────────────────────────────────────────
llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model_name=MODEL_NAME,
    temperature=0,
)

# ── ReAct Prompt ─────────────────────────────────────────────────
REACT_PROMPT = PromptTemplate.from_template("""
You are APOA — Autonomous Personal Operations Agent.
You are a highly capable AI agent that can execute real-world tasks autonomously.

You have access to the following tools:
{tools}

You also have access to previous context from long-term memory:
{long_term_context}

Previous conversation:
{chat_history}

Use the following format STRICTLY:

Question: the input question you must answer
Thought: think about what to do
Action: the action to take, must be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (repeat Thought/Action/Action Input/Observation as needed)
Thought: I now know the final answer
Final Answer: the final answer to the original question

IMPORTANT RULES:
- Always think step by step
- Use tools when needed, don't guess
- Be concise but complete in final answer
- If a task has multiple steps, execute them one by one

Begin!

Question: {input}
Thought: {agent_scratchpad}
""")

# ── Agent Builder ────────────────────────────────────────────────
def build_agent():
    """
    Builds and returns the ReAct agent with tools + memory.
    """
    memory = get_short_term_memory()
    vectorstore = get_or_create_vectorstore()

    agent = create_react_agent(
        model=llm,
        tools=all_tools,
        prompt=REACT_PROMPT,
    )

    agent_executor = AgentExecutor(
        agent=agent,
        tools=all_tools,
        memory=memory,
        verbose=True,           # shows reasoning steps in terminal
        handle_parsing_errors=True,
        max_iterations=10,
        return_intermediate_steps=True,
    )

    return agent_executor, vectorstore


# ── Main Run Function ────────────────────────────────────────────
async def run_agent(user_input: str, agent_executor, vectorstore) -> dict:
    """
    Runs the agent on a user input.
    Returns response + tools used + memory update confirmation.
    """
    # Search long-term memory for relevant context
    long_term_context = search_memory(vectorstore, user_input)

    # Run agent
    result = await agent_executor.ainvoke({
        "input": user_input,
        "long_term_context": long_term_context,
    })

    # Extract output
    output = result.get("output", "")

    # Extract tools used
    intermediate_steps = result.get("intermediate_steps", [])
    tools_used = [step[0].tool for step in intermediate_steps]

    # Save task to long-term memory
    save_to_memory(
        vectorstore,
        f"User asked: {user_input} | Agent responded: {output[:200]}",
        metadata={"type": "task"}
    )

    return {
        "response": output,
        "tools_used": tools_used,
        "memory_updated": True,
        "steps_taken": len(intermediate_steps)
    }