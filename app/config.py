import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
VECTOR_DB_DIR = PROJECT_ROOT / "vector_store"

# Ensure directories exist
for d in (DATA_DIR, OUTPUT_DIR, VECTOR_DB_DIR):
    d.mkdir(parents=True, exist_ok=True)

# Embedding model (sentence-transformers)
EMBEDDING_MODEL = "all-MiniLM-L6-v2"   # lightweight, fast, accurate

# LLM config placeholder (for Ollama or other local LLM)
LLM_PROVIDER = "fallback"  # "ollama" or "fallback"
OLLAMA_HOST = "http://localhost:11434"  # if using Ollama HTTP API
OLLAMA_MODEL = "llama2"  # update as your local model name in Ollama
