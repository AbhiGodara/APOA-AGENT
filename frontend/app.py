import streamlit as st
import httpx
import asyncio

API_BASE = "http://localhost:8000/api/v1"

# ── Page Config ──────────────────────────────────────────────────
st.set_page_config(
    page_title="APOA - Autonomous Agent",
    page_icon="🤖",
    layout="wide"
)

# ── Header ───────────────────────────────────────────────────────
st.title("🤖 APOA — Autonomous Personal Operations Agent")
st.caption("Give me any goal. I'll plan it, execute it, and remember it.")

# ── Session State ─────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent_logs" not in st.session_state:
    st.session_state.agent_logs = []

# ── Layout ───────────────────────────────────────────────────────
col1, col2 = st.columns([2, 1])

# ── Chat Column ──────────────────────────────────────────────────
with col1:
    st.subheader("💬 Chat")

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Input
    user_input = st.chat_input("Give me a goal... e.g. 'Search latest AI frameworks and summarize'")

    if user_input:
        # Show user message
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        with st.chat_message("user"):
            st.markdown(user_input)

        # Call API
        with st.chat_message("assistant"):
            with st.spinner("Agent is thinking and executing... 🔄"):
                try:
                    response = httpx.post(
                        f"{API_BASE}/chat",
                        json={"message": user_input},
                        timeout=60.0
                    )
                    data = response.json()

                    agent_response = data.get("response", "No response")
                    tools_used = data.get("tools_used", [])
                    steps_taken = data.get("steps_taken", 0)
                    memory_updated = data.get("memory_updated", False)

                    # Show response
                    st.markdown(agent_response)

                    # Save to session
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": agent_response
                    })

                    # Save logs
                    st.session_state.agent_logs.append({
                        "task": user_input,
                        "tools_used": tools_used,
                        "steps_taken": steps_taken,
                        "memory_updated": memory_updated
                    })

                except httpx.ConnectError:
                    st.error("❌ Cannot connect to backend. Make sure uvicorn is running!")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# ── Agent Logs Column ─────────────────────────────────────────────
with col2:
    st.subheader("🔧 Agent Logs")

    if not st.session_state.agent_logs:
        st.info("Agent logs will appear here after each task.")
    else:
        for i, log in enumerate(reversed(st.session_state.agent_logs)):
            with st.expander(f"Task {len(st.session_state.agent_logs) - i}"):
                st.write(f"**Goal:** {log['task']}")
                st.write(f"**Steps taken:** {log['steps_taken']}")
                st.write(f"**Memory updated:** {'✅' if log['memory_updated'] else '❌'}")
                if log['tools_used']:
                    st.write("**Tools used:**")
                    for tool in log['tools_used']:
                        st.write(f"  - 🔧 `{tool}`")
                else:
                    st.write("**Tools used:** None")

    st.divider()

    # ── Memory Viewer ─────────────────────────────────────────────
    st.subheader("🧠 Conversation Memory")
    if st.button("Load Memory"):
        try:
            res = httpx.get(f"{API_BASE}/history", timeout=10.0)
            history = res.json().get("history", [])
            if not history:
                st.info("No memory yet.")
            else:
                for msg in history:
                    role = msg.get("role", "unknown")
                    content = msg.get("content", "")
                    st.write(f"**{role.capitalize()}:** {content[:100]}...")
        except Exception as e:
            st.error(f"Error loading memory: {str(e)}")

    st.divider()

    # ── Health Check ──────────────────────────────────────────────
    st.subheader("⚡ System Status")
    if st.button("Check Status"):
        try:
            res = httpx.get(f"{API_BASE}/health", timeout=5.0)
            st.success(res.json().get("status", "Unknown"))
        except:
            st.error("❌ Backend not reachable")