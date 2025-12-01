# embeddings.py
from langchain_community.embeddings import OllamaEmbeddings
from app.db.vector_db import get_or_create_collection
import asyncio

embedder = OllamaEmbeddings(model="nomic-embed-text")

async def embed_chunk(chunk: str):
    """Embed a single chunk asynchronously."""
    return embedder.embed_query(chunk)

async def store_embeddings(text: str, chunk_size: int = 500):
    """
    Split text into chunks, embed them asynchronously, and store in Chroma collection.
    """
    collection = get_or_create_collection()
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

    # Create tasks for asynchronous embedding
    tasks = [embed_chunk(chunk) for chunk in chunks]
    embeddings = await asyncio.gather(*tasks)

    # Batch insert into Chroma
    ids = [f"doc_{i}" for i in range(len(chunks))]
    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids
    )
