from typing import TypedDict, List, Dict, Any, Optional


class GraphState(TypedDict):
    """Represents the complete state of the Text-to-SQL agent workflow."""
    
    # Input
    user_query: str
    
    # RAG Retrieval Context
    retrieved_context: List[str]
    
    # Generation & Validation
    generated_sql: Optional[str]
    error_message: Optional[str]
    is_valid_sql: bool
    requires_human_review: bool
    
    # Execution & Output
    is_human_approved: Optional[bool]
    modified_sql: Optional[str]
    query_results: Optional[Dict[str, Any]]
    final_response: Optional[str]