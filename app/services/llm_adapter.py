"""
Pluggable LLM adapter.

Default implementation: fallback_synthesizer() which composes a report
from retrieved docs + instructions (useful for testing / development).

If you run Ollama locally, set config.LLM_PROVIDER = "ollama" and
implement ollama_synthesize() to call your running Ollama service.

Two options to connect Ollama:
 - Ollama HTTP API (if available) - call requests to localhost:11434
 - Ollama Python package (if you have it) - import and call directly

This file includes the fallback and a template to add Ollama calls.
"""

from app.config import LLM_PROVIDER, OLLAMA_HOST, OLLAMA_MODEL
import textwrap
from typing import List, Dict
import requests
import os

def fallback_synthesize(instructions: str, retrieved_docs: List[Dict]) -> str:
    """
    Simple synthesizer: concatenate the top docs with headings and apply
    the instruction as a generation prompt. This is NOT a true LLM,
    but allows the pipeline to function immediately.
    """
    sb = []
    sb.append("GENERATED REPORT\n")
    sb.append("INSTRUCTIONS: " + instructions + "\n\n")
    sb.append("RETRIEVED SOURCE SNIPPETS (most relevant first):\n")
    for i, d in enumerate(retrieved_docs, 1):
        src = d.get("meta", {}).get("source", "unknown")
        sb.append(f"--- Source {i}: {src} (score: {d.get('distance')}) ---\n")
        snippet = d.get("text", "")
        # shorten too-long snippets
        if len(snippet) > 4000:
            snippet = snippet[:4000] + " ... [truncated]"
        sb.append(snippet + "\n\n")

    sb.append("\nSYNTHESIS:\n")
    # Basic heuristic summary: take first sentences and echo instruction
    combined = " ".join([d.get("text","")[:1500] for d in retrieved_docs])
    summary = combined[:3000]  # safeguard
    sb.append(summary + "\n\n")
    sb.append("End of generated report.")
    return "\n".join(sb)

def ollama_synthesize(instructions: str, retrieved_docs: List[Dict]) -> str:
    """
    Example: call Ollama HTTP API if you have it running.
    This function must be adapted to the exact Ollama HTTP contract you have.
    (Ollama's HTTP API shape may vary; consult Ollama docs. This is a schematic.)
    """
    prompt_parts = [
        "You are an expert report writer. Use the retrieved snippets and the user instructions to produce a professional report.",
        "USER INSTRUCTIONS: " + instructions,
        "RETRIEVED_SNIPPETS:"
    ]
    for i, d in enumerate(retrieved_docs, 1):
        src = d.get("meta", {}).get("source", "unknown")
        snippet = d.get("text", "")
        prompt_parts.append(f"--- snippet {i} from {src} ---\n{snippet}\n")

    prompt = "\n\n".join(prompt_parts)

    # Example: If Ollama provides a /api/generate endpoint (schematic)
    try:
        resp = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "max_tokens": 800
            },
            timeout=60
        )
        resp.raise_for_status()
        data = resp.json()
        # extract text depending on response format
        text = data.get("text") or data.get("result") or str(data)
        return text
    except Exception as e:
        return f"[Ollama request failed: {e}]\n\n" + fallback_synthesize(instructions, retrieved_docs)

def synthesize_report(instructions: str, retrieved_docs: List[Dict]) -> str:
    if LLM_PROVIDER == "ollama":
        return ollama_synthesize(instructions, retrieved_docs)
    else:
        return fallback_synthesize(instructions, retrieved_docs)
