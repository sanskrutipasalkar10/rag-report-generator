# app/services/report_generator.py
from pathlib import Path
from datetime import datetime
import uuid
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from app.config import OUTPUT_DIR
from app.services.llm_adapter import synthesize_report

async def generate_final_report(instructions, retrieved_chunks, file_text):
    """
    Generate PDF report from instructions and retrieved chunks
    """
    docs = [{"document": c, "metadata": {}} for c in retrieved_chunks]

    report_text = synthesize_report(instructions, docs)

    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    file_name = f"report_{ts}_{uuid.uuid4().hex[:6]}.pdf"
    output_path = Path(OUTPUT_DIR) / file_name

    styles = getSampleStyleSheet()
    story = []

    for p in report_text.split("\n\n"):
        if p.strip():
            story.append(Paragraph(p.replace("\n", "<br/>"), styles["Normal"]))
            story.append(Spacer(1, 8))

    doc = SimpleDocTemplate(str(output_path))
    doc.build(story)

    return str(output_path)
