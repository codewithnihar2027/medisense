import pytesseract
from PIL import Image
import io
import re

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text_from_image(image_bytes: bytes) -> str:
    try:
        image = Image.open(io.BytesIO(image_bytes))

        text = pytesseract.image_to_string(image)

        print("OCR RAW:", text)

        return text.strip()

    except Exception as e:
        print("OCR ERROR:", e)
        return ""


def extract_medicine_name(raw_text: str) -> str:
    raw_text = raw_text.lower()

    # clean noise
    raw_text = re.sub(r'[^a-zA-Z\s]', ' ', raw_text)

    words = raw_text.split()

    stopwords = [
        "tablet", "tablets", "capsule", "capsules",
        "ip", "strip", "mg", "dose"
    ]

    words = [w for w in words if w not in stopwords and len(w) > 3]

    print("CLEAN WORDS:", words)

    # 👉 return first meaningful word
    return words[0] if words else ""