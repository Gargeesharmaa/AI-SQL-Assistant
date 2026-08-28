from agent.state import GraphState
from rag.vector_store import vector_store
from typing import Any, Dict


def retrieve_context_node(state: GraphState) -> Dict[str, Any]:
    """Retrieves relevant table DDLs, glossaries, and golden queries from VectorStore."""
    user_query = state["user_query"]
    results = vector_store.search_context(query=user_query, limit=3)
    
    context_chunks = [item["text"] for item in results]
    return {"retrieved_context": context_chunks}