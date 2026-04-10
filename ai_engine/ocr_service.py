# ai_engine/ocr_service.py
import easyocr
import numpy as np
from PIL import Image
import io
import re

reader = None

def get_reader():
    global reader
    if reader is None:
        reader = easyocr.Reader(['en'], gpu=False)
    return reader


def extract_text_from_image(image_bytes: bytes) -> str:
    reader = get_reader()
    image = Image.open(io.BytesIO(image_bytes))
    img_array = np.array(image)
    results = reader.readtext(img_array)

   
    text = " ".join([r[1] for r in results]) if results else ""
    return text


def extract_medicine_names(raw_text: str) -> list:
    
 
    # Match medicine-like patterns
    pattern = r'\b[A-Z][a-zA-Z0-9\-]*(?:\s\d+(?:mg|ML|mg)?)?\b'

    matches = re.findall(pattern, raw_text)

    # Clean + unique
    medicines = list(set([m.strip() for m in matches if len(m) > 3]))

    return medicines[:5]