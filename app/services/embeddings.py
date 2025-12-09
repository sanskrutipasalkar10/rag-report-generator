# app/services/embeddings.py
from sentence_transformers import SentenceTransformer, util

print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Model loaded.")

embeddings_store = []   # [(text_chunk, vector)]

def embed_docs(chunks):
    global embeddings_store
    embeddings_store = []
    for chunk in chunks:
        vec = model.encode(chunk)
        embeddings_store.append((chunk, vec))

def search_similar(query, top_k=5):
    query_vec = model.encode(query)
    similarities = [
        (chunk, util.cos_sim(query_vec, vec).item())
        for (chunk, vec) in embeddings_store
    ]
    similarities.sort(key=lambda x: x[1], reverse=True)
    return [chunk for chunk, _ in similarities[:top_k]]
