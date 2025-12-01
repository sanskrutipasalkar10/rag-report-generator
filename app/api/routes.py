from fastapi import APIRouter, UploadFile, File
from app.services import ingestion, embeddings as embed_svc

router = APIRouter()

# -------------------------
# FILE UPLOAD ENDPOINT
# -------------------------
@router.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):
    file_bytes = await file.read()

    # 1. Parse CSV/Excel/PDF
    text_data = ingestion.read_file(file.filename, file_bytes)

    # 2. Store embeddings in vector DB
    embed_svc.store_embeddings(text_data)

    return {"status": "success", "filename": file.filename, "message": "File processed & embeddings stored"}

# -------------------------
# GENERATE REPORT ENDPOINT (optional if exists)
# -------------------------
@router.post("/generate-report")
async def generate_report():
    report_data = ingestion.generate_report()  # implement this in your service
    return {"status": "success", "report": report_data}
