# app/db/vector_db.py
from pathlib import Path
from app.config import VECTOR_DB_DIR
import logging

VECTOR_DB_DIR = Path(VECTOR_DB_DIR)
VECTOR_DB_DIR.mkdir(parents=True, exist_ok=True)

# Try new API first, fallback if not present
try:
    from chromadb import PersistentClient
    CHROMA_CLIENT = PersistentClient(path=str(VECTOR_DB_DIR))
    def get_or_create_collection(name: str = "rag_collection"):
        return CHROMA_CLIENT.get_or_create_collection(name=name)
except Exception:
    # fallback to older client style if installed
    try:
        import chromadb
        from chromadb.config import Settings
        CHROMA_CLIENT = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory=str(VECTOR_DB_DIR)))
        def get_or_create_collection(name: str = "rag_collection"):
            try:
                return CHROMA_CLIENT.get_collection(name=name)
            except Exception:
                return CHROMA_CLIENT.create_collection(name=name)
    except Exception as e:
        logging.exception("Chroma client import failed")
        raise
