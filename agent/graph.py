from langgraph.graph import StateGraph, END
from agent.state import GraphState
from agent.nodes.retriever import retrieve_context_node
from agent.nodes.generator import generate_sql_node
from agent.nodes.validator import validate_sql_node
from agent.nodes.executor import execute_sql_node


def route_after_validation(state: GraphState) -> str:
    """Routes execution based on validation checks and HITL flags."""
    if not state["is_valid_sql"]:
        return "END"
    if state["requires_human_review"]:
        return "hitl_checkpoint"
    return "execute_sql"


# 1. Build State Graph
builder = StateGraph(GraphState)

# 2. Add Nodes
builder.add_node("retrieve_context", retrieve_context_node)
builder.add_node("generate_sql", generate_sql_node)
builder.add_node("validate_sql", validate_sql_node)
builder.add_node("execute_sql", execute_sql_node)

# 3. Define Edges & Workflow Transitions
builder.set_entry_point("retrieve_context")
builder.add_edge("retrieve_context", "generate_sql")
builder.add_edge("generate_sql", "validate_sql")

builder.add_conditional_edges(
    "validate_sql",
    route_after_validation,
    {
        "END": END,
        "execute_sql": "execute_sql",
        "hitl_checkpoint": END  # Interrupted for API/UI approval handling
    }
)

builder.add_edge("execute_sql", END)

# 4. Compile Workflow Graph
app_graph = builder.compile()