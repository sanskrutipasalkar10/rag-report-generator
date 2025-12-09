import chromadb
from chromadb.utils import embedding_functions
from app.config import VECTOR_DB_DIR, EMBEDDING_MODEL


# ---------------------------------------------------------
# New Chroma Persistent Client
# ---------------------------------------------------------

def get_chroma_client():
    """
    Creates a PersistentClient using NEW Chroma API.
    """
    return chromadb.PersistentClient(path=str(VECTOR_DB_DIR))


def get_collection():
    """
    Loads or creates the 'rag_documents' collection.
    """
    client = get_chroma_client()

    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_MODEL
    )

    collection = client.get_or_create_collection(
        name="rag_documents",
        embedding_function=embedding_fn,
        metadata={"hnsw:space": "cosine"}
    )

    return collection


# ---------------------------------------------------------
# ADD DOCUMENTS
# ---------------------------------------------------------

def add_document(text: str, source: str):
    """
    Adds one document to the vector DB.
    """
    col = get_collection()

    new_id = f"doc_{col.count() + 1}"

    col.add(
        ids=[new_id],
        documents=[text],
        metadatas=[{"source": source}]
    )

    return {"id": new_id, "source": source}


# ---------------------------------------------------------
# RETRIEVE DOCUMENTS
# ---------------------------------------------------------

def retrieve_documents(query: str, top_k: int = 5):
    """
    Retrieves top_k similar documents.
    """
    col = get_collection()

    results = col.query(
        query_texts=[query],
        n_results=top_k
    )

    docs = results["documents"][0]
    metas = results["metadatas"][0]

    # Return list of (text, metadata)
    return list(zip(docs, metas))
