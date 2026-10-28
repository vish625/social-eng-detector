from fastapi import FastAPI
from detector.groq_client import analyze_page
from detector.keyword_filter import keyword_scan
from models.schemas import (AnalyzeRequest,AnalyzeResponse)

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Backend running successfully"}

@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(data: AnalyzeRequest):

    combined_text = f"""
    {data.pageText}

    {data.interactionText}
    """

    keyword_result = keyword_scan(combined_text)

    # HIGH CONFIDENCE RULE DETECTION
    if keyword_result["score"] >= 60:

        return {
            "risk_level": "DANGER",
            "score": keyword_result["score"],
            "attack_category": "Keyword Detection",
            "explanation": "Dangerous command-execution instructions detected."
        }

    # OTHERWISE USE AI
    ai_result = analyze_page(combined_text)

    return ai_result