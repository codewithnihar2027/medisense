from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel

from backend.app.services.medicine_service import get_alternatives
from backend.app.services.gemini_service import enhance_with_ai
from ai_engine.ocr_service import extract_text_from_image, extract_medicine_names

router = APIRouter()

class SearchRequest(BaseModel):
    medicine_name: str


# -----------------------
# SEARCH API
# -----------------------
@router.post("/search")
def search(req: SearchRequest):

    result = get_alternatives(req.medicine_name)

    if "error" not in result:
        result = enhance_with_ai(result)

    return result


# -----------------------
# SCAN API
# -----------------------
@router.post("/scan")
async def scan_medicine(file: UploadFile = File(...)):

    image_bytes = await file.read()

    text = extract_text_from_image(image_bytes)
    medicines = extract_medicine_names(text)

    if not medicines:
        return {"error": "No medicine detected"}

    result = get_alternatives(medicines[0])

    # 🔥 ADD AI HERE
    if "error" not in result:
        result = enhance_with_ai(result)

    return {
        "detected_text": text,
        "detected_medicine": medicines[0],
        "result": result
    }