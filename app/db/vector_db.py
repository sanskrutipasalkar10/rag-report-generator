# vector_db.py
import chromadb
from chromadb.config import Settings
from app.config import VECTOR_DB_DIR

_client = None

def get_client():
    global _client
    if _client is None:
        # New Chroma client constructor
        _client = chromadb.Client(
            Settings(
                chroma_db_impl="duckdb+parquet",
                persist_directory=str(VECTOR_DB_DIR)
            )
        )
    return _client

def get_or_create_collection(collection_name: str = "rag_reports"):
    """
    Get an existing collection or create a new one.
    Compatible with new Chroma client API.
    """
    client = get_client()
    try:
        # New API: get_collection will raise an error if it doesn't exist
        collection = client.get_collection(name=collection_name)
    except Exception:
        # Use the new API to create collection
        collection = client.create_collection(name=collection_name)
    return collection
