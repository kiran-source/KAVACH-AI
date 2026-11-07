# Dataset Card: KAVACH-AI Multilingual Synthetic Dataset v2.0 (500 Conversations)

## 1. Summary
The **KAVACH-AI Synthetic Dataset v2.0** is an expanded multilingual benchmark comprising **500 domain-curated scripted multi-turn conversations** across five language categories: English, Hindi, Telugu, and code-mixed Hindi-English and Telugu-English.

## 2. Quantitative Breakdown
- **Total Conversations:** 500
- **Class Distribution:** SCAM: 200 (40.0%), LEGITIMATE: 175 (35.0%), AMBIGUOUS: 125 (25.0%)
- **Language Distribution:** Exactly 100 conversations per language category (`en`, `hi`, `te`, `hi-en`, `te-en`)
- **Dialogue Turns:** Exactly 8 turns per conversation alternating caller and recipient
- **Splits (70 / 15 / 15):** Train: 350, Validation: 75, Test: 75
- **Scenario Leakage:** 0% overlap across splits
- **Review Status:** Strictly marked `pending_review` to maintain transparent governance.
