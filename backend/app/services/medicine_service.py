import pandas as pd
import requests
from rapidfuzz import process
import re
import os

# -----------------------
# LOAD DATA
# -----------------------
BASE_DIR = os.path.abspath(os.path.join(__file__, "../../../../"))
CSV_PATH = os.path.join(BASE_DIR, "data", "medicines_clean.csv")

print("CSV PATH:", CSV_PATH)

df = pd.read_csv(CSV_PATH)

df['brand_name_clean'] = df['brand_name'].astype(str).str.lower().str.strip()
df['salt_clean'] = df['salt_clean'].astype(str).str.lower().str.strip()
df['comp1'] = df['comp1'].astype(str).str.lower().str.strip()
df['comp2'] = df['comp2'].astype(str).str.lower().str.strip()


# -----------------------
# HELPERS
# -----------------------
def extract_numbers(text):
    return re.findall(r'\d+', str(text))


def remove_combinations(df_subset):
    return df_subset[
        ~df_subset['salt_clean'].str.contains(r'\+|,| and ', case=False, na=False)
    ]


def prefer_tablet(df_subset):
    preferred = df_subset[
        df_subset['brand_name'].str.contains('tablet|tab|capsule', case=False, na=False)
    ]
    return preferred if not preferred.empty else df_subset


def is_pure_single_salt(row, query):
    comp1 = str(row.get('comp1', '')).lower().strip()
    comp2 = str(row.get('comp2', '')).lower().strip()
    return (query in comp1) and (comp2 == "" or comp2 == "nan")


# -----------------------
# 🔥 IMPROVED FUZZY MATCH (KEY FIX)
# -----------------------
def smart_match(name):
    name = name.lower().strip()

    choices = df['brand_name_clean'].dropna().tolist()

    match = process.extractOne(name, choices)

    if match:
        matched_name, score, _ = match
        print("FUZZY MATCH:", matched_name, "Score:", score)

        # ✅ relaxed threshold (IMPORTANT FIX)
        if score >= 75:
            return df[df['brand_name_clean'] == matched_name]['brand_name'].values[0]

    return None


# -----------------------
# OPENFDA API
# -----------------------
def fetch_from_openfda(query):
    try:
        query = query.lower().strip()

        url = f"https://api.fda.gov/drug/label.json?search={query}&limit=1"
        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            return None

        data = response.json()

        if "results" not in data:
            return None

        result = data["results"][0]

        return {
            "input_medicine": query,
            "source": "OpenFDA",
            "generic_name": result.get("openfda", {}).get("generic_name", ["N/A"])[0],
            "manufacturer": result.get("openfda", {}).get("manufacturer_name", ["N/A"])[0],
            "purpose": result.get("purpose", ["N/A"])[0],
            "warnings": result.get("warnings", ["N/A"])[0]
        }

    except Exception as e:
        print("OpenFDA error:", e)
        return None


# -----------------------
# AFFORDABILITY SCORE
# -----------------------
def affordability_score(original, cheapest):
    if original <= 0:
        return 0

    savings = (original - cheapest) / original
    return round(max(min(savings * 10, 10), 0), 1)


# -----------------------
# MAIN FUNCTION
# -----------------------
def get_alternatives(medicine_name):

    query = medicine_name.lower().strip()

    # =======================
    # STEP 1: PURE GENERIC MATCH
    # =======================
    generic_match = df[
        df.apply(lambda row: is_pure_single_salt(row, query), axis=1)
    ]

    if not generic_match.empty:
        generic_match = prefer_tablet(generic_match)
        med = generic_match.iloc[0]
        matched_name = med['brand_name']
        salt = med['salt_clean']

    else:
        # =======================
        # STEP 2: EXACT SALT MATCH
        # =======================
        exact_salt = df[df['salt_clean'] == query]

        if not exact_salt.empty:
            exact_salt = prefer_tablet(exact_salt)
            med = exact_salt.iloc[0]
            matched_name = med['brand_name']
            salt = med['salt_clean']

        else:
            # =======================
            # STEP 3: 🔥 FUZZY MATCH (MAIN FIX)
            # =======================
            matched_name = smart_match(query)

            if matched_name is None:
                print("→ No dataset match, trying API")

                api_data = fetch_from_openfda(medicine_name)

                if api_data:
                    return api_data

                return {
                    "error": "Medicine not found in dataset or OpenFDA"
                }

            med = df[df['brand_name'] == matched_name].iloc[0]
            salt = med['salt_clean']

    # =======================
    # BASIC INFO
    # =======================
    original_price = float(med['price'])

    comp1 = med.get('comp1') or ""
    comp2 = med.get('comp2') or ""

    generic_name = f"{comp1} {comp2}".replace("nan", "").strip()

    # =======================
    # SAME SALT FILTER
    # =======================
    same_salt = df[df['salt_clean'] == salt].copy()

    same_salt = same_salt[same_salt['brand_name'] != matched_name]
    same_salt = remove_combinations(same_salt)
    same_salt = prefer_tablet(same_salt)

    # =======================
    # DOSAGE FILTER
    # =======================
    input_nums = extract_numbers(med['brand_name'])

    if input_nums:
        same_salt['dose_match'] = same_salt['brand_name'].apply(
            lambda x: len(set(extract_numbers(x)) & set(input_nums))
        )
        same_salt = same_salt[same_salt['dose_match'] > 0]

    # =======================
    # PRICE FILTER
    # =======================
    cheaper = same_salt[same_salt['price'] < original_price]

    if not cheaper.empty:
        same_salt = cheaper
        note = "✅ Same strength & cheaper alternatives"
    else:
        if not same_salt.empty:
            note = "⚠️ Same strength alternatives (not cheaper)"
        else:
            return {
                "input_medicine": medicine_name,
                "matched_medicine": matched_name,
                "price": original_price,
                "note": "❌ No valid alternatives found"
            }

    # =======================
    # SORT
    # =======================
    same_salt = same_salt.sort_values(by='price')

    same_salt['savings_percent'] = (
        (original_price - same_salt['price']) / original_price * 100
    )

    cheapest = same_salt.iloc[0]

    # =======================
    # FINAL RESPONSE
    # =======================
    return {
        "input_medicine": medicine_name,
        "matched_medicine": matched_name,

        "generic_equivalent": generic_name,
        "price": original_price,

        "cheapest_option": cheapest['brand_name'],
        "cheapest_price": float(cheapest['price']),

        "therapeutic_class": med.get('therapeutic_class'),
        "affordability_score": affordability_score(original_price, cheapest['price']),

        "note": note,

        "alternatives": same_salt[
            ['brand_name', 'price', 'manufacturer', 'savings_percent']
        ]
        .head(5)
        .to_dict(orient="records")
    }