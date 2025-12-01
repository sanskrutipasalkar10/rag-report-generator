from app.services import report_generation, embeddings

def test_generate_report(tmp_path):
    docs = [
        {"id": "1", "text": "Company A produced 100 units. Revenue increased by 5%.", "meta": {"source": "a.csv"}},
        {"id": "2", "text": "Company B produced 150 units. Defects 2%.", "meta": {"source": "b.csv"}},
    ]
    retriever = embeddings.index_documents_and_get_retriever(docs, collection_name="test_report_collection")
    path = report_generation.generate_report_from_instructions("Create a short summary report", retriever, top_k=2)
    assert path.endswith(".pdf")
