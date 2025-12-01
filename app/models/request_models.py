from pydantic import BaseModel
from typing import List, Optional

class ReportRequest(BaseModel):
    instructions: str
    files: Optional[List[str]] = []
    top_k: Optional[int] = 5
