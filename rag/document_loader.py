import os
import json
import logging
from typing import List, Dict, Any
from rag.vector_store import vector_store

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KNOWLEDGE_BASE_DIR = os.path.join(BASE_DIR, "knowledge_base")


def load_knowledge_base():
    """Reads DDLs, Golden Queries, and Glossaries and indexes them into VectorStore."""
    documents: List[Dict[str, Any]] = []
    doc_id = 1

    # 1. Parse DDL Schemas
    ddl_path = os.path.join(KNOWLEDGE_BASE_DIR, "ddl_schemas.sql")
    if os.path.exists(ddl_path):
        with open(ddl_path, "r", encoding="utf-8") as f:
            content = f.read()
            # Split by CREATE TABLE block
            tables = content.split("CREATE TABLE")
            for table in tables:
                if table.strip():
                    table_ddl = "CREATE TABLE " + table.strip()
                    documents.append({
                        "id": doc_id,
                        "text": f"Database Table Schema DDL:\n{table_ddl}",
                        "metadata": {"type": "ddl_schema"}
                    })
                    doc_id += 1

    # 2. Parse Golden Queries
    golden_path = os.path.join(KNOWLEDGE_BASE_DIR, "golden_queries.json")
    if os.path.exists(golden_path):
        with open(golden_path, "r", encoding="utf-8") as f:
            golden_list = json.load(f)
            for item in golden_list:
                text_content = f"Golden Query Example:\nQuestion: {item['question']}\nSQL: {item['sql']}"
                documents.append({
                    "id": doc_id,
                    "text": text_content,
                    "metadata": {"type": "golden_query", "question": item["question"]}
                })
                doc_id += 1

    # 3. Parse Business Glossary
    glossary_path = os.path.join(KNOWLEDGE_BASE_DIR, "business_glossary.md")
    if os.path.exists(glossary_path):
        with open(glossary_path, "r", encoding="utf-8") as f:
            content = f.read()
            documents.append({
                "id": doc_id,
                "text": f"Business Definitions & Glossary:\n{content}",
                "metadata": {"type": "business_glossary"}
            })
            doc_id += 1

    if documents:
        vector_store.add_documents(documents)
        logger.info("Knowledge base indexing successfully completed.")
    else:
        logger.warning("No files found in knowledge base directory to index.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    load_knowledge_base()