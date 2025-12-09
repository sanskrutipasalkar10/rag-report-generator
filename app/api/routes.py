# app/api/routes.py
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services.ingestion import save_uploaded_file
from app.services.embeddings import embed_docs, search_similar
from app.services.report_generator import generate_final_report

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload file endpoint: saves uploaded file and returns path
    """
    try:
        file_path = await save_uploaded_file(file)
        return {"status": "success", "file_path": str(file_path)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-report")
async def generate_report(
    file: UploadFile = File(...),
    instructions: str = Form(...),
    top_k: int = Form(5)
):
    try:
        # ---- 1) Load & extract text ----
        from app.services.ingestion import ingest_file
        file_path = await save_uploaded_file(file)
        chunks = ingest_file(file_path)

        if not chunks:
            raise HTTPException(status_code=400, detail="Uploaded file is empty")

        # ---- 2) Embed & store chunks ----
        embed_docs(chunks)

        # ---- 3) Vector search ----
        retrieved_chunks = search_similar(instructions, top_k=top_k)

        # ---- 4) Generate final report ----
        final_report_path = await generate_final_report(
            instructions=instructions,
            retrieved_chunks=retrieved_chunks,
            file_text="\n".join(chunks)
        )

        return {"status": "success", "report_path": final_report_path}

    except Exception as e:
        print("ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))
