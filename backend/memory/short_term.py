from langchain_classic.memory import ConversationBufferMemory

def get_short_term_memory():
    """
    Short-term memory — stores conversation history within a session.
    Agent remembers what was said earlier in the same conversation.
    """
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="output"
    )
    return memory