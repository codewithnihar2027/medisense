import pandas as pd
from rapidfuzz import process

# Load dataset ONCE
df = pd.read_csv("data/medicines_clean.csv")

# -----------------------
# Fuzzy Search
# -----------------------
def fuzzy_search(name):
    choices = df['brand_name'].dropna().tolist()
    match, score, _ = process.extractOne(name, choices)

    if score < 60:
        return None

    return match

# -----------------------
# Affordability Score
# -----------------------
def affordability_score(original, cheapest):
    if original == 0:
        return 0
    savings = (original - cheapest) / original
    return round(min(savings * 10, 10), 1)

# -----------------------
# MAIN FUNCTION
# -----------------------
def get_alternatives(medicine_name):

    matched_name = fuzzy_search(medicine_name)

    if not matched_name:
        return {"error": "Medicine not found"}

    med = df[df['brand_name'] == matched_name].iloc[0]

    salt = med['salt_clean']
    original_price = float(med['price'])

    same_salt = df[df['salt_clean'] == salt].copy()

    if same_salt.empty or len(same_salt) < 2:
        substitutes = [
            med.get('substitute0'),
            med.get('substitute1'),
            med.get('substitute2'),
            med.get('substitute3'),
            med.get('substitute4')
        ]

        substitutes = [s for s in substitutes if pd.notna(s)]

        return {
            "medicine": matched_name,
            "price": original_price,
            "note": "Using dataset substitutes",
            "alternatives": substitutes
        }

    same_salt = same_salt.sort_values(by='price')

    same_salt['savings_percent'] = (
        (original_price - same_salt['price']) / original_price * 100
    )

    cheapest_price = float(same_salt.iloc[0]['price'])
    score = affordability_score(original_price, cheapest_price)

    return {
        "medicine": matched_name,
        "price": original_price,
        "therapeutic_class": med.get('therapeutic_class'),
        "affordability_score": score,
        "alternatives": same_salt[['brand_name','price','manufacturer','savings_percent']]
                        .head(5)
                        .to_dict(orient="records")
    }