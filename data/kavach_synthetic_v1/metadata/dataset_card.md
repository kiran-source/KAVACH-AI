# Dataset Card: KAVACH-AI Multilingual Synthetic Dataset v1.0

## Dataset Summary

The **KAVACH-AI Multilingual Synthetic Dataset v1.0** is a benchmark dataset comprising **100 multi-turn synthetic dialogue transcripts** and **20 speech audio samples** designed for voice scam detection, transcript classification, and explainable scam tactic identification in Indian multilingual contexts.

The dataset spans five language categories representative of Indian mobile phone communication: English, Hindi, Telugu, and natural code-switched Hindi-English (Hinglish) and Telugu-English (Tenglish).

## Dataset Details

- **Total Conversations:** 100
- **Class Distribution:** SCAM: 40 (40%), LEGITIMATE: 35 (35%), AMBIGUOUS: 25 (25%)
- **Language Distribution:** Exactly 20 records per language (`en`: 20, `hi`: 20, `te`: 20, `te-en`: 20, `hi-en`: 20)
- **Stratified Balance:** Exactly 8 SCAM, 7 LEGITIMATE, and 5 AMBIGUOUS per language category
- **Dialogue Turns:** Exactly 8 turns per conversation (caller / recipient turns alternating)
- **Audio Samples:** 20 WAV audio files (4 files per language category: 1 Stage 2 Pilot, 3 Stage 3 Bulk)
- **Total Audio Duration:** 331.84 seconds
- **Audio Format:** 16,000 Hz, 16-bit PCM mono RIFF/WAVE

## Dataset Splits (70 / 15 / 15)

- **Train (`splits/train.jsonl`):** 70 conversations (30 SCAM, 25 LEGITIMATE, 15 AMBIGUOUS; 14 per language)
- **Validation (`splits/validation.jsonl`):** 15 conversations (5 SCAM, 5 LEGITIMATE, 5 AMBIGUOUS; 3 per language)
- **Test (`splits/test.jsonl`):** 15 conversations (5 SCAM, 5 LEGITIMATE, 5 AMBIGUOUS; 3 per language)
- **Scenario Leakage:** 0% overlap across train, validation, and test splits (strictly scenario-grouped).

## Provenance & Synthetic Methodology

- **Text Generation:** Created using a Domain-Curated Multilingual Scenario Engine based on verified Indian financial fraud typologies (police advisories, RBI circulars, TRAI telecom notices).
- **Audio Synthesis:** Synthesized using **Gnani Timbre v2.5** (`timbre-v2.5`, voices: `Nalini` for Hindi/English and `Chitra` for Telugu/Tenglish).
- **Audio Validation:** Preliminary ASR validation performed using **Gnani Prisma v3.0** (`POST /stt/v3`).
- **Ethics & Synthetic Compliance:** 100% synthetic dialogues. Zero real personal phone recordings used.
- **PII Checks:** Automated regex scanning confirms zero real credit card numbers, Aadhaar numbers, or valid personal identities.
- **Human Review Status:** All records carry `review_status: 'pending_review'` to maintain strict honesty regarding automated generation.
