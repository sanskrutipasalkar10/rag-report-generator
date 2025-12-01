from app.services import embeddings
from app.services import ingestion

def test_embedding_indexing(tmp_path):
    # create dummy docs
    docs = [
        {"id": "1", "text": "This is a test document about pumps.", "meta": {"source": "test1"}},
        {"id": "2", "text": "Another document about valves and motors.", "meta": {"source": "test2"}},
    ]
    retriever = embeddings.index_documents_and_get_retriever(docs, collection_name="test_collection")
    results = retriever("pumps", top_k=1)
    assert isinstance(results, list)
