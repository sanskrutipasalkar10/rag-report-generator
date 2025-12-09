import requests
from typing import List, Dict
from app.config import LLM_PROVIDER, OLLAMA_HOST, OLLAMA_MODEL

def _build_prompt(instructions: str, docs: List[Dict]):
    """
    Create a prompt for the LLM combining instructions and retrieved docs.
    Produces a professional structured report.
    """
    ctx = "\n\n".join([f"[source={d.get('metadata',{}).get('source','unknown')}] {d.get('document','')}" for d in docs])
    prompt = f"""
You are an expert supply chain and manufacturing analyst. 

Instructions:
{instructions}

Use the following context to create a professional, structured report with:
- Executive Summary
- Key Findings / Risks
- Recommendations
- Tables or bullet points where appropriate
- Clear professional language

Context:
{ctx}
"""
    return prompt

def synthesize_report(instructions: str, retrieved_docs: List[Dict]):
    """
    Call Ollama local HTTP API if configured, otherwise fallback.
    """
    prompt = _build_prompt(instructions, retrieved_docs)

    if LLM_PROVIDER == "ollama":
        try:
            url = f"{OLLAMA_HOST}/api/generate"
            payload = {
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "max_tokens": 2000,
                "temperature": 0.3
            }
            r = requests.post(url, json=payload, timeout=120)
            r.raise_for_status()
            data = r.json()
            # Ollama may return text under "text" or "response" depending on version
            if "text" in data:
                return data["text"]
            elif "response" in data:
                return data["response"]
            else:
                return str(data)
        except Exception as e:
            return _fallback_summarize(prompt, retrieved_docs, reason=str(e))
    else:
        # fallback for testing
        return _fallback_summarize(prompt, retrieved_docs, reason="no LLM provider configured")

def _fallback_summarize(prompt: str, retrieved_docs: List[Dict], reason: str = ""):
    """
    Very simple fallback: stitch top docs and produce a basic structure.
    Only used when LLM fails.
    """
    parts = [f"NOTE: fallback summarizer used. Reason: {reason}\n"]
    parts.append("=== INSTRUCTIONS ===\n")
    parts.append(prompt[:1000] + ("\n...\n" if len(prompt) > 1000 else "\n"))
    parts.append("\n=== RETRIEVED SNIPPETS ===\n")
    for i, d in enumerate(retrieved_docs):
        src = d.get("metadata", {}).get("source", "unknown")
        parts.append(f"[{i+1}] source={src}\n{d.get('document')[:1000]}\n---\n")
    parts.append("\n=== BASIC FINDINGS ===\n")
    findings = []
    for d in retrieved_docs:
        text = d.get("document","")
        first = text.split(".")[0].strip()
        if first:
            findings.append(first + ".")
    parts.append("\n".join([f"- {f}" for f in findings[:10]]))
    parts.append("\n\n=== END OF REPORT ===")
    return "\n".join(parts)
