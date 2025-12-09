from pydantic import BaseModel

class ReportRequest(BaseModel):
    instructions: str
    top_k: int = 5
