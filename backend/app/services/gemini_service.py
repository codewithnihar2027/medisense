import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def enhance_with_ai(data):

    prompt = f"""
    Improve this medicine data:

    {json.dumps(data)}

    Return JSON only:
    {{
      "purpose": "",
      "safety_note": "",
      "better_explanation": ""
    }}
    """

    try:
        res = model.generate_content(prompt)
        text = res.text.strip().replace("```json", "").replace("```", "")
        ai_data = json.loads(text)

        data.update(ai_data)
        return data

    except:
        return data