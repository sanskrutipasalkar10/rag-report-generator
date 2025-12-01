from fastapi import FastAPI
from app.api.routes import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="RAG Report Generator")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins for development
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes with /api prefix
app.include_router(router, prefix="/api")


@app.get("/")
def root():
    return {"status": "ok", "service": "RAG Report Generator Backend"}
