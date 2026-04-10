# medisense
# 💊 MediSense — Affordable Medicine Intelligence Platform

## 🚨 Problem

In India, the same medicine (same composition) is sold under multiple brands at drastically different prices.
Most patients are unaware of cheaper alternatives, leading to unnecessary financial burden.

---

## 💡 Solution

MediSense is an AI-powered platform that allows users to:

* Enter or scan a medicine name
* Get detailed analysis (composition, usage, dosage)
* Discover cheaper generic or branded alternatives
* Compare prices across options
* View nearby pharmacy availability

---

##  Core Features

* 🔍 Medicine Search & Analysis
* 💰 Cost Comparison & Savings Insight
* 🔄 Generic Alternative Recommendation
* 📷 Prescription OCR (Image Upload)
* 📍 Nearby Pharmacy Finder (Mock Data)
* 📊 Affordability Score

---

## 🧠 How It Works

1. User inputs medicine name or uploads prescription
2. System extracts medicine details (OCR + AI)
3. Matches composition (salt) from dataset
4. Finds all equivalent medicines
5. Ranks by price → suggests cheapest alternatives

---

##  Tech Stack

* **Frontend:** React (Vite + Tailwind)
* **Backend:** FastAPI (Python)
* **AI Engine:** Claude API (analysis + structuring)
* **Data Processing:** Pandas
* **Dataset:** Extensive_A_Z_medicines_dataset_of_India

---

##  Project Structure

medismart/
├── frontend/        # UI (React)
├── backend/         # API (FastAPI)
├── ai_engine/       # AI + OCR logic
├── data/            # dataset + cleaning
├── docs/            # demo assets

---

##  Team Roles

* Frontend Developer
* Backend Developer
* AI/ML Engineer
* Data Engineer
* Integration & Deployment

---

## 🚀 Setup Instructions (Basic)

```bash
git clone https://github.com/your-team/medismart
cd medisense
```

(Setup instructions will be expanded during development)

---

## 📊 Impact

* Reduces medicine cost for users
* Improves awareness of generic drugs
* Supports informed healthcare decisions

---

##  Note

This project is a prototype built during a 24-hour hackathon.
Medical decisions should always be verified by professionals.

---

##  Status

 In Development (Hackathon Mode)
