import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)
def enhance_with_ai(data):

    if "error" in data:
        return data

    api_key = os.getenv("GEMINI_API_KEY")

    # 🔒 SAFETY: if key missing, skip AI
    if not api_key:
        data["ai_explanation"] = "AI not configured"
        return data

    try:
        prompt = f"""
Explain this medicine in simple terms:
{data}
Keep it short.
"""

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        data["ai_explanation"] = response.text

    except Exception:
        data["ai_explanation"] = "AI temporarily unavailable"

    return data