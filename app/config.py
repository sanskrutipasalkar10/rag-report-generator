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

# LLM config (Ollama)
LLM_PROVIDER = "ollama"                 # change to 'ollama' for local LLM
OLLAMA_HOST = "http://localhost:11434" # Ollama HTTP API host
OLLAMA_MODEL = "llama2"                 # your local Ollama model name
