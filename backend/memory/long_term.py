from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
import os

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def get_or_create_vectorstore():
    """
    Always creates a fresh in-memory vector store.
    No persistence — each session gets clean memory.
    """
    vectorstore = FAISS.from_documents(
        [Document(page_content="APOA agent initialized.", metadata={"type": "system"})],
        embeddings
    )
    print("✅ Created fresh in-memory store")
    return vectorstore

def save_to_memory(vectorstore, text: str, metadata: dict = {}):
    doc = Document(page_content=text, metadata=metadata)
    vectorstore.add_documents([doc])

def search_memory(vectorstore, query: str, k: int = 3):
    results = vectorstore.similarity_search(query, k=k)
    if not results:
        return "No relevant memory found."
    return "\n".join([f"- {r.page_content}" for r in results])