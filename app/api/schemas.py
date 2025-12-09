from pydantic import BaseModel

class ReportRequest(BaseModel):
    instructions: str
