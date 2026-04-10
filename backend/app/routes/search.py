from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel

from backend.app.services.medicine_service import get_alternatives
from backend.app.services.gemini_service import enhance_with_ai
from ai_engine.ocr_service import extract_text_from_image, extract_medicine_name

import re

router = APIRouter()


class SearchRequest(BaseModel):
    medicine_name: str


def clean_medicine_name(text: str):
    text = text.lower()
    text = re.sub(r'\d+mg', '', text)
    text = re.sub(r'[^a-zA-Z ]', '', text)

    words = text.split()

    stopwords = ["tablet", "tablets", "capsule", "capsules", "ip", "strip"]
    words = [w for w in words if w not in stopwords]

    return words[0] if words else ""


# -----------------------
# SEARCH API
# -----------------------
@router.post("/search")
def search(req: SearchRequest):

    medicine = req.medicine_name.strip()

    if not medicine:
        return {"error": "Medicine name required"}

    result = get_alternatives(medicine)

    if "error" not in result:
        result = enhance_with_ai(result)

    return result


# -----------------------
# SCAN API (FAIL-SAFE)
# -----------------------
@router.post("/scan")
async def scan_medicine(file: UploadFile = File(...)):

    try:
        image_bytes = await file.read()

        raw_text = extract_text_from_image(image_bytes)

        if not raw_text:
            return {"error": "No text detected"}

        # 🔥 SIMPLE EXTRACTION
        medicine_name = extract_medicine_name(raw_text)
        print("EXTRACTED:", medicine_name)

        if not medicine_name:
            return {"error": "Could not detect medicine"}

        result = get_alternatives(medicine_name)

        if "error" not in result:
            result = enhance_with_ai(result)

        return {
            "ocr_text": raw_text,
            "detected_medicine": medicine_name,
            "result": result
        }

    except Exception as e:
        print("SCAN ERROR:", e)
        return {"error": "Scan failed"}