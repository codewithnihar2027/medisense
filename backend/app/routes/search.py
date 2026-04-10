from fastapi import APIRouter
from pydantic import BaseModel

from app.services.medicine_service import get_alternatives
from app.services.gemini_service import enhance_with_ai

router = APIRouter()

class SearchRequest(BaseModel):
    medicine_name: str

@router.post("/search")
def search(req: SearchRequest):

    result = get_alternatives(req.medicine_name)

    # AI enhance
    if "error" not in result:
        result = enhance_with_ai(result)

    return result