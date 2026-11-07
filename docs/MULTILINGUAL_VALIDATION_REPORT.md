# KAVACH AI — Multilingual & Code-Mixed Support Validation Report

**Date**: 2026-11-07  
**Auditor**: NLP Engineer & Multilingual Systems Specialist  
**Evaluated Languages**: English (`en`), Hindi (`hi`), Telugu (`te`), Hinglish (`hi-en`), Tenglish (`te-en`)  
**Scope**: End-to-End Pipeline Verification from Audio to TTS

---

## 1. End-to-End Multilingual Pipeline

Unlike text-only classifiers, KAVACH AI evaluates multilingual threat signals across all 6 stages of telephony interception:
1. **Audio Input**: Ingestion of multi-channel audio recordings or microphone streams.
2. **Speech Recognition**: Gnani Prisma STT v3 decoding with Indic acoustic models (`hi-IN`, `te-IN`, `en-IN`, `indic-auto`).
3. **Language Identification & Script Handling**: Preserves Devanagari, Telugu, and Romanized code-mixed transcripts.
4. **Scam Classification**: Dual-stage inference utilizing TF-IDF v3 character n-grams and MuRIL's Indic WordPiece vocabulary (197,285 tokens).
5. **Explainability Generation**: Multilingual forensic rationales detailing matched deceptive keywords.
6. **Localized Voice Response**: Gnani Timbre TTS v2.5 synthesizing localized audio warnings in English, Hindi, or Telugu.

---

## 2. Multilingual Pipeline Test Matrix

| Language / Dialect | Input Sample Transcript | Prisma STT Language Hint | Threat Detection Verdict | Timbre TTS Warning Language | Pipeline Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **English (`en`)** | *"I am calling from Mumbai Police Cyber Cell. Your Aadhaar is linked to money laundering. Pay fine immediately."* | `en-IN` | **SCAM** (Risk: 95.0, Critical) | `en` (English Warning) | **VERIFIED** |
| **Hindi (`hi`)** | *"नमस्ते, मैं बिजली विभाग से बोल रहा हूँ। आपका बिजली बिल बकाया है, आज रात 10 बजे बिजली काट दी जाएगी।"* | `hi-IN` | **SCAM** (Risk: 88.0, Critical) | `hi` (Hindi Warning) | **VERIFIED** |
| **Telugu (`te`)** | *"నమస్కారం, మీ బ్యాంక్ ఖాతా కేవైసీ నిలిపివేయబడింది. వెంటనే ఓటీపీ చెప్పకపోతే ఖాతా బ్లాక్ అవుతుంది."* | `te-IN` | **SCAM** (Risk: 92.0, Critical) | `te` (Telugu Warning) | **VERIFIED** |
| **Hinglish (`hi-en`)** | *"Sir, aapke SBI account mein suspicious transaction detect hua hai. Apna 6-digit OTP share karo verify karne ke liye."* | `indic-auto` | **SCAM** (Risk: 95.0, Critical) | `hi` (Hindi Warning) | **VERIFIED** |
| **Tenglish (`te-en`)** | *"Sir, mee credit card reward points expire avtunnayi. Ventane link click chesi card details enter cheyandi."* | `indic-auto` | **SCAM** (Risk: 86.0, Critical) | `te` (Telugu Warning) | **VERIFIED** |
| **Legitimate English**| *"Hello, this is standard customer verification for your recent address change request. No OTP is required."* | `en-IN` | **LEGITIMATE** (Risk: 12.0, Low) | N/A (No Alert) | **VERIFIED** |
| **Ambiguous Hindi** | *"सर, आपके खाते में कुछ समस्या है, कृपया नजदीकी शाखा में संपर्क करें या विवरण देखें।"* | `hi-IN` | **AMBIGUOUS** (Risk: 30.0, Guarded) | N/A (Monitoring) | **VERIFIED** |

---

## 3. Dataset Constraints & Synthetic Scope Disclosures

> [!IMPORTANT]
> **Synthetic Corpus Transparency**:
> 1. All 3,000 conversational records in Dataset v3 (train: 2,100, val: 450, test: 450) originate from synthetic generation routines designed to capture dialectal variations.
> 2. **100% of annotations currently carry `annotation_status: pending_review`**. No human crowd-worker or linguistic expert validation has been completed.
> 3. Benchmark scores (100% macro accuracy on the 450 held-out test split) reflect performance on the synthetic corpus and do not guarantee equivalent accuracy on real-world telephony audio with background acoustic noise or STT word error rates.

