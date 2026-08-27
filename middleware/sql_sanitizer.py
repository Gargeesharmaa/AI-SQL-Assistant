import logging
import sqlglot
from  sqlglot import exp

logger = logging.getLogger(__name__)

FORBIDDEN_NODES = (
    exp.Delete,
    exp.Drop,
    exp.Insert,
    exp.Update,
    exp.Alter,
    exp.Create,
    exp.Grant,
    exp.Revoke,
)

class SQLSanitizerError(Exception):
    """Custom exception raised when SQL fails security or syntax checks."""
    pass

def validate_and_sanitize_sql(sql_str: str, dialect: str="postres") -> str:
    """
    parses a SQL string using SQLGlot, verifies it contains only safe SELECT queries,
    and returns a clean, dialect-formatted SQL string.
    """
    if not sql_str or not sql_str.strip():
        raise SQLSanitizerError("Empty SQL string provided. ")

    try:
        parsed = sqlglot.parse_one(sql_str, read=dialect)
    except Exception as e:
        logger.error(f"SQLGlot Parsing failed: {e}")
        raise SQLSanitizerError(f"Invalid SQL syntax: {str(e)}")

    if parsed is None:
        raise SQLSanitizerError("Faileed to parse SQL statement.")

    if not isinstance(parsed, exp.Select):
        raise SQLSanitizerError(f"Only SELECT queries are allowed. Detected: {type(parsed).__name__}")

    for node in parsed.walk():
        if isinstance(node, FORBIDDEN_NODES):
            raise SQLSanitizerError(f"Forbidden SQL operation detected: {type(node).__name__}")

    return parsed.sql(dialect=dialect)
    