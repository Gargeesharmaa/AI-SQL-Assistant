import asyncio
from agent.state import GraphState
from config import AsyncSessionLocal
from middleware.db_executor import execute_safe_query
from agent.prompts import FINAL_ANSWER_PROMPT
from agent.nodes.generator import llm
from typing import Any, Dict


def execute_sql_node(state: GraphState) -> Dict[str, Any]:
    """Executes the validated SQL against PostgreSQL and formats the summary answer."""
    sql_to_run = state.get("modified_sql") or state.get("generated_sql")
    
    # Run async database query in synchronous node thread
    async def run_query():
        async with AsyncSessionLocal() as session:
            return await execute_safe_query(sql_to_run, session)
            
    exec_result = asyncio.run(run_query())
    
    if not exec_result["success"]:
        return {
            "query_results": exec_result,
            "final_response": f"Execution failed: {exec_result.get('error')}"
        }
        
    # Generate natural language summary of execution results
    summary_prompt = FINAL_ANSWER_PROMPT.format(
        user_query=state["user_query"],
        sql=sql_to_run,
        results=exec_result["rows"]
    )
    summary_res = llm.invoke(summary_prompt)
    
    return {
        "query_results": exec_result,
        "final_response": str(summary_res.content)
    }