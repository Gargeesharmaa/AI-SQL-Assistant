from agent.state import GraphState
from middleware.sql_sanitizer import validate_and_sanitize_sql, SQLSanitizerError
from typing import Dict, Any

def validate_sql_node(state: GraphState) -> Dict[str, Any]:
    """Validates generated SQL with SQLGlot AST parser and flags complex queries for HITL review."""
    sql = state.get("generated_sql", "")
    
    try:
        clean_sql = validate_and_sanitize_sql(sql)
        
        # Flag multi-table joins or aggregate subqueries for Human-in-the-Loop review
        sql_upper = clean_sql.upper()
        needs_review = "JOIN" in sql_upper and ("GROUP BY" in sql_upper or "HAVING" in sql_upper)
        
        return {
            "generated_sql": clean_sql,
            "is_valid_sql": True,
            "requires_human_review": needs_review,
            "error_message": None
        }
    except SQLSanitizerError as e:
        return {
            "is_valid_sql": False,
            "requires_human_review": False,
            "error_message": str(e)
        }