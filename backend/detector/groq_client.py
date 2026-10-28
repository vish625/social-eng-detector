import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

SYSTEM_PROMPT = """
You are a cybersecurity analyst specializing in social engineering attack detection.
Analyze webpage content and classify it.
Return ONLY valid JSON.
Format:
{
 "risk_level": "SAFE" | "CAUTION" | "DANGER",
 "score" : 0-100
 "attack_category" : "string",
 "explanation" : "short explanation:
 }
 """

def analyze_page(page_text: str):

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": page_text

            }
        ]
    )
    result = response.choices[0].message.content
    print("\nRAW AI RESPONSE:\n")
    print(result)

    # Extract JSON safely
    json_match = re.search(r'\{.*\}', result, re.DOTALL)

    if not json_match:
        return {
            "risk_level": "CAUTION",
            "score": 50,
            "attack_category": "Parsing Error",
            "explanation": "AI response could not be parsed."
        }

    json_text = json_match.group()

    try:
        return json.loads(json_text)

    except json.JSONDecodeError:

        return {
            "risk_level": "CAUTION",
            "score": 50,
            "attack_category": "JSON Error",
            "explanation": "Invalid JSON returned by AI."
        }