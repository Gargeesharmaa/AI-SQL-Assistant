import asyncio
import logging
from typing import Dict, Any, List
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from config import settings
from middleware.sql_sanitizer import validate_and_sanitize_sql, SQLSanitizerError

logger = logging.getLogger(__name__)

async def execute_safe_query(
        sql_query: str,
        session: AsyncSession
)-> Dict[str, Any]:
    """Sanitizes enforces cap and executes a SQL query safely against PostgreSQL"""
    clean_sql = f"{validate_and_sanitize_sql.parsed} LIMIT {settings.DB_MAX_ROW_LIMIT}"

    try:
        timeout_ms = settings.DB_QUERY_TIMEOUT_SECONDS * 1000
        await session.executr(text(f"SET LOCAL statement_timeout ='{timeout_ms}ms'; "))

        result = await asyncio.wait_for(
            session.execute(text(clean_sql)),
            timeout=settings.DB_QUERY_TIMEOUT_SECONDS
        )

        columns: List[str] = list(result.key())
        rows = [dict(zip(columns,row)) for row in result.fetchall()]

        return {
            "success": True,
            "columns": columns,
            "rows": rows,
            "row_Count": len(rows),
            "executed_sql": clean_sql
        }

    except asyncio.TimeoutError:
        logger.error(f"Query timed out after {settings.DB_QUERY_TIMEOUT_SECONDS}s: {clean_sql}")
        return {
            "success": False,
            "error": f"Query execution timed out ({settings.DB_QUERY_TIMEOUT_SECONDS}s limit exceeded).",
            "executed_sql": clean_sql
        }
    except SQLSanitizerError as e:
        return {
            "success": False,
            "error": str(e),
            "executed_sql": sql_query
        }
    except Exception as e:
        logger.error(f"Database execution error: {str(e)}")
        return {
            "success": False,
            "error": f"Database Execution Error: {str(e)}",
            "executed_sql": clean_sql
        }
