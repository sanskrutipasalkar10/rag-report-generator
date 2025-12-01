from app.services.llm_adapter import synthesize_report
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
from pathlib import Path
from app.config import OUTPUT_DIR
import uuid
import os

def generate_report_from_instructions(instructions: str, retriever, top_k: int = 5) -> str:
    """
    Steps:
      1) Use retriever(query) to get top_k docs
      2) Call LLM adapter to synthesize
      3) Save to PDF and return path
    """
    # 1) Retrieve relevant docs using instruction as a query
    retrieved = retriever(instructions, top_k=top_k)

    # 2) Synthesize with LLM adapter
    report_text = synthesize_report(instructions, retrieved)

    # 3) Save result as PDF
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    filename = f"report_{ts}_{uuid.uuid4().hex[:6]}.pdf"
    out_path = Path(OUTPUT_DIR) / filename

    styles = getSampleStyleSheet()
    story = []
    for paragraph in report_text.split("\n\n"):
        paragraph = paragraph.strip()
        if not paragraph:
            continue
        story.append(Paragraph(paragraph.replace("\n", "<br/>"), styles["Normal"]))
        story.append(Spacer(1, 6))

    doc = SimpleDocTemplate(str(out_path))
    doc.build(story)

    return str(out_path)
