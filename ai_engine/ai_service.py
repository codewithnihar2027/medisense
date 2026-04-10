import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# The client automatically looks for the GEMINI_API_KEY environment variable
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """You are a pharmaceutical expert for Indian medicines.
Always respond with valid JSON only. No extra text, no markdown."""

def analyze_medicine(medicine_name: str) -> dict:
    prompt = f'Analyze this medicine: "{medicine_name}"\n\nReturn ONLY this JSON structure...'
    
    # Note: Prompt structure is slightly cleaner in Gemini configs
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",  # High-speed model, perfect for JSON
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.3,
                response_mime_type="application/json",
            ),
        )
        
        # Gemini provides a .parsed or .text attribute. 
        # For simple JSON mode, use response.text
        text = response.text
        result = json.loads(text)

        # Affordability score calculation
        if result.get("alternatives"):
         best = min(result["alternatives"], key=lambda x: float(x.get("price_inr", 9999)))
         orig = result.get("original_price_inr", 1)
            
         if orig > 0:
                savings = (orig - best["price_inr"]) / orig
                result["affordability_score"] = min(round(savings * 10, 1), 10)

        return result

    except Exception as e:
        # Catching both JSON errors and API errors
        return {"error": f"API Error: {str(e)}", "raw": locals().get('text', '')}