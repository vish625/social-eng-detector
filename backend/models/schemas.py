from pydantic import BaseModel

class AnalyzeRequest(BaseModel):
    url: str
    pageText: str
    interactionText: str = ""

class AnalyzeResponse(BaseModel):
    risk_level: str
    score: int
    attack_category: str
    explanation: str
    