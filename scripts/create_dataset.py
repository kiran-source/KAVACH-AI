import os
import json

SYNTHETIC_DATA_DIR = "data/synthetic_audio"
LABELS_DIR = "data/labels"

os.makedirs(SYNTHETIC_DATA_DIR, exist_ok=True)
os.makedirs(LABELS_DIR, exist_ok=True)

DATASET_MANIFEST = [
    {
        "scenario_id": "SCENARIO_001",
        "title": "Digital Arrest CBI Scam (Hindi-English)",
        "language": "hi",
        "expected_classification": "scam",
        "expected_severity": "Critical",
        "expected_categories": ["Authority Impersonation", "Urgency and Threats", "Digital Arrest Patterns"],
        "script": "Namaste. I am Inspector Sharma from CBI headquarters Delhi. Your Aadhaar number is involved in money laundering. You are placed under digital arrest right now.",
        "noise_condition": "clean"
    },
    {
        "scenario_id": "SCENARIO_002",
        "title": "Bank KYC & OTP Theft (English)",
        "language": "en",
        "expected_classification": "scam",
        "expected_severity": "High",
        "expected_categories": ["Credential Theft", "Urgency and Threats"],
        "script": "Sir your bank account KYC verification is pending today. If you do not update PAN card right now your account will be blocked. Please tell me the OTP immediately.",
        "noise_condition": "telephone"
    },
    {
        "scenario_id": "SCENARIO_003",
        "title": "Telugu Bank Account Block Scam (Telugu)",
        "language": "te",
        "expected_classification": "scam",
        "expected_severity": "High",
        "expected_categories": ["Credential Theft", "Urgency and Threats"],
        "script": "నమస్కారం మీ బ్యాంకు అకౌంట్ బ్లాక్ అయింది. వెంటనే మీ ఏటీఎం పిన్ నంబర్ మరియు ఓటీపీ చెప్పండి.",
        "noise_condition": "moderate_noise"
    },
    {
        "scenario_id": "SCENARIO_004",
        "title": "Legitimate Customer Support (English)",
        "language": "en",
        "expected_classification": "safe",
        "expected_severity": "Low",
        "expected_categories": [],
        "script": "Hello sir, this is calling from ABC customer support regarding your recent ticket inquiry. How can I assist you with your software subscription today?",
        "noise_condition": "clean"
    },
    {
        "scenario_id": "SCENARIO_005",
        "title": "Courier Customs Parcel Scam (Hindi)",
        "language": "hi",
        "expected_classification": "scam",
        "expected_severity": "High",
        "expected_categories": ["Courier and Customs Fraud", "Authority Impersonation"],
        "script": "আপনার پارسل میں ڈرگس ملے ہیں۔ کسٹم ڈیپارٹمنٹ نے ضبط کر لیا ہے۔ پولیس کو فوری فیس ٹرانسفر کرو.",
        "noise_condition": "telephone"
    }
]

manifest_path = os.path.join(LABELS_DIR, "dataset_manifest.json")
with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(DATASET_MANIFEST, f, indent=2, ensure_ascii=False)

print(f"Synthetic dataset manifest created successfully at {manifest_path} with {len(DATASET_MANIFEST)} scenarios.")
