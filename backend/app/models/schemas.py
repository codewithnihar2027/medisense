from pydantic import BaseModel
from typing import List, Optional


# ----------------------------
# 🔍 REQUEST SCHEMA
# ----------------------------
class SearchRequest(BaseModel):
    medicine_name: str


# ----------------------------
# 💊 ALTERNATIVE MEDICINE
# ----------------------------
class AlternativeMedicine(BaseModel):
    brand_name: str
    price: float
    manufacturer: Optional[str]
    savings_percent: Optional[float]


# ----------------------------
# 🧠 AI ENHANCEMENT (Gemini)
# ----------------------------
class AIEnhancement(BaseModel):
    purpose: Optional[str]
    safety_note: Optional[str]
    better_explanation: Optional[str]


# ----------------------------
# ✅ SUCCESS RESPONSE
# ----------------------------
class MedicineResponse(BaseModel):
    medicine: str
    price: float
    therapeutic_class: Optional[str]
    affordability_score: Optional[float]

    alternatives: List[AlternativeMedicine]

    # AI fields (Gemini)
    purpose: Optional[str]
    safety_note: Optional[str]
    better_explanation: Optional[str]


# ----------------------------
# ⚠️ ERROR RESPONSE
# ----------------------------
class ErrorResponse(BaseModel):
    error: str


# ----------------------------
# 📸 OCR RESPONSE (optional future use)
# ----------------------------
class OCRResponse(BaseModel):
    extracted_text: str
    medicines: List[MedicineResponse]