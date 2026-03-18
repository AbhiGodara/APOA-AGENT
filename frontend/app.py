import streamlit as st
import asyncio
import nest_asyncio
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))

from agent.graph import build_agent, run_agent

# ── Page Config ──────────────────────────────────────────────────
st.set_page_config(
    page_title="APOA - Autonomous Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 APOA — Autonomous Personal Operations Agent")
st.caption("Give me any goal. I'll plan it, execute it, and remember it.")

# ── Session State ─────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent_logs" not in st.session_state:
    st.session_state.agent_logs = []
if "agent_executor" not in st.session_state:
    st.session_state.agent_executor = None
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

# ── Build Agent once ─────────────────────────────────────────────
# @st.cache_resource
def get_agent():
    if "agent_executor" not in st.session_state or st.session_state.agent_executor is None:
        executor, vs = build_agent()
        st.session_state.agent_executor = executor
        st.session_state.vectorstore = vs
    return st.session_state.agent_executor, st.session_state.vectorstore

# ── Layout ───────────────────────────────────────────────────────
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💬 Chat")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.text(msg["content"])

    user_input = st.chat_input("Give me a goal...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.text(user_input)

        with st.spinner("Agent is thinking... 🔄"):
            try:
                agent_executor, vectorstore = get_agent()

                # Build conversation history string from session state
                history = ""
                for msg in st.session_state.messages[-6:]:  # last 3 exchanges
                    role = "User" if msg["role"] == "user" else "Assistant"
                    history += f"{role}: {msg['content']}\n"

                # Inject history into input
                full_input = f"{user_input}"
                if history:
                    full_input = f"Conversation so far:\n{history}\nUser's new message: {user_input}"

                result = agent_executor.invoke({"input": full_input})
                output = result.get("output", "")
                output = output.replace("Final Answer:", "").strip()
                output = output.replace("The final answer is", "").strip()
                intermediate_steps = result.get("intermediate_steps", [])
                tools_used = [step[0].tool for step in intermediate_steps]

                for step in intermediate_steps:
                    if step[0].tool in ["email_draft_tool", "reminder_tool"]:
                        output = str(step[1])
                        break

                if not output:
                    output = "Agent completed but returned no output."
                steps_taken = len(intermediate_steps)

            except Exception as e:
                output = f"❌ Error: {str(e)}"
                tools_used = []
                steps_taken = 0

        st.chat_message("assistant").text(output)

        st.session_state.messages.append({"role": "assistant", "content": output})
        st.session_state.agent_logs.append({
            "task": user_input,
            "tools_used": tools_used,
            "steps_taken": steps_taken,
        })

        st.rerun()

with col2:
    st.subheader("🔧 Agent Logs")

    if not st.session_state.agent_logs:
        st.info("Agent logs will appear here after each task.")
    else:
        for i, log in enumerate(reversed(st.session_state.agent_logs)):
            with st.expander(f"Task {len(st.session_state.agent_logs) - i}"):
                st.write(f"**Goal:** {log['task']}")
                st.write(f"**Steps taken:** {log['steps_taken']}")
                if log['tools_used']:
                    st.write("**Tools used:**")
                    for t in log['tools_used']:
                        st.write(f"  - 🔧 `{t}`")
                else:
                    st.write("**Tools used:** None")

    st.divider()

    st.subheader("🧠 Memory")
    if st.button("Load Memory"):
        try:
            agent_executor, _ = get_agent()
            memory_vars = agent_executor.memory.load_memory_variables({})
            messages = memory_vars.get("chat_history", [])
            if not messages:
                st.info("No memory yet.")
            else:
                for msg in messages:
                    st.write(f"**{msg.type.capitalize()}:** {msg.content[:150]}...")
        except Exception as e:
            st.error(f"Error: {str(e)}")

    st.divider()

    st.subheader("⚡ System Status")
    if st.button("Check Agent"):
        try:
            get_agent()
            st.success("✅ Agent is ready!")
        except Exception as e:
            st.error(f"❌ {str(e)}")

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.agent_logs = []
        st.rerun()
