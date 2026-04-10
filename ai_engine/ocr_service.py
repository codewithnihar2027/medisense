
import pytesseract
from PIL import Image
import io

# ⚠️ Windows path (change if different)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_image(image_bytes: bytes) -> str:
    image = Image.open(io.BytesIO(image_bytes))
    text = pytesseract.image_to_string(image)
    return text

import re

def extract_medicine_names(raw_text: str) -> list:
    raw_text = raw_text.lower()

    # remove noise
    raw_text = re.sub(r'[^a-zA-Z0-9\s]', ' ', raw_text)

    words = raw_text.split()

    candidates = []

    for w in words:
        # medicine patterns
        if len(w) > 4:
            if any(suffix in w for suffix in [
                "mab","cillin","prazole","olol","azole","statin","vir","ine","cin"
            ]):
                candidates.append(w)

    # fallback if nothing found
    if not candidates:
        candidates = [w for w in words if len(w) > 5]

    return candidates[:5]