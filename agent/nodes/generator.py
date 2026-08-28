from langchain_groq import ChatGroq
from agent.state import GraphState
from agent.prompts import SQL_GENERATION_PROMPT
from config import settings
from typing import Any, Dict

llm = ChatGroq(
    groq_api_key=settings.GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile",
    temperature=0.0
)


def generate_sql_node(state: GraphState) -> Dict[str, Any]:
    """Uses Groq to generate a raw SQL query from natural language context."""
    context_str = "\n\n".join(state.get("retrieved_context", []))
    prompt = SQL_GENERATION_PROMPT.format(
        context=context_str,
        user_query=state["user_query"]
    )
    
    response = llm.invoke(prompt)
    raw_sql = str(response.content).strip()
    
    # Strip accidental code blocks if model formats output
    if raw_sql.startswith("```"):
        raw_sql = raw_sql.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
        
    return {"generated_sql": raw_sql}