import streamlit as st
import httpx

API_BASE = "http://127.0.0.1:8001/api/v1"

st.set_page_config(
    page_title="APOA - Autonomous Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 APOA — Autonomous Personal Operations Agent")
st.caption("Give me any goal. I'll plan it, execute it, and remember it.")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent_logs" not in st.session_state:
    st.session_state.agent_logs = []

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💬 Chat")

    # Display full chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.text(msg["content"])  # use text not markdown

    user_input = st.chat_input("Give me a goal...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.text(user_input)

        with st.spinner("Agent is thinking and executing... 🔄"):
            try:
                response = httpx.post(
                    f"{API_BASE}/chat",
                    json={"message": user_input},
                    timeout=180.0
                )
                data = response.json()
                agent_response = data.get("response", "No response")
                tools_used = data.get("tools_used", [])
                steps_taken = data.get("steps_taken", 0)
                memory_updated = data.get("memory_updated", False)

                if not agent_response or agent_response.strip() == "":
                    agent_response = str(data)

            except httpx.ConnectError:
                agent_response = "❌ Cannot connect to backend!"
                tools_used = []
                steps_taken = 0
                memory_updated = False
            except Exception as e:
                agent_response = f"❌ Error: {str(e)}"
                tools_used = []
                steps_taken = 0
                memory_updated = False

        # ── Display response OUTSIDE spinner and chat_message ────
        st.chat_message("assistant").text(agent_response)

        # Save to session
        st.session_state.messages.append({
            "role": "assistant",
            "content": agent_response
        })

        st.session_state.agent_logs.append({
            "task": user_input,
            "tools_used": tools_used,
            "steps_taken": steps_taken,
            "memory_updated": memory_updated
        })

        st.rerun()  # force UI refresh

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
                    st.write(f"**{role.capitalize()}:** {content[:150]}...")
        except Exception as e:
            st.error(f"Error: {str(e)}")

    st.divider()

    st.subheader("⚡ System Status")
    if st.button("Check Status"):
        try:
            res = httpx.get(f"{API_BASE}/health", timeout=5.0)
            st.success(res.json().get("status", "Unknown"))
        except:
            st.error("❌ Backend not reachable")