from app.services import ingestion

def test_ingest_sample(tmp_path):
    # create a small csv
    p = tmp_path / "sample.csv"
    p.write_text("col1,col2\n1,2\n3,4")
    docs = ingestion.ingest_files([str(p)])
    assert isinstance(docs, list)
    assert docs[0]["text"].count("col1") >= 1
