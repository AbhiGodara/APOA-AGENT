from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
import os

VECTOR_STORE_PATH = "memory/faiss_store"

# Load embedding model (runs locally, no API needed)
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

def get_or_create_vectorstore():
    """
    Long-term memory — persists important info across sessions using FAISS.
    Stores things like: previous tasks, user preferences, search results.
    """
    if os.path.exists(VECTOR_STORE_PATH):
        vectorstore = FAISS.load_local(
            VECTOR_STORE_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )
        print("✅ Loaded existing long-term memory")
    else:
        # Create with a dummy doc on first run
        vectorstore = FAISS.from_documents(
            [Document(page_content="APOA agent initialized.", metadata={"type": "system"})],
            embeddings
        )
        vectorstore.save_local(VECTOR_STORE_PATH)
        print("✅ Created new long-term memory")

    return vectorstore

def save_to_memory(vectorstore, text: str, metadata: dict = {}):
    """
    Save any important info to long-term memory.
    Example: save_to_memory(vs, "User searched for AI internships", {"type": "task"})
    """
    doc = Document(page_content=text, metadata=metadata)
    vectorstore.add_documents([doc])
    vectorstore.save_local(VECTOR_STORE_PATH)

def search_memory(vectorstore, query: str, k: int = 3):
    """
    Search long-term memory for relevant past context.
    Returns top-k most relevant stored memories.
    """
    results = vectorstore.similarity_search(query, k=k)
    if not results:
        return "No relevant memory found."
    return "\n".join([f"- {r.page_content}" for r in results])