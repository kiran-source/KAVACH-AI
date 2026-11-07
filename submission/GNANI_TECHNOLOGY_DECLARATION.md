# KAVACH AI — Gnani AI Technology Declaration

**Competition**: Great Indian AI Internship Challenge 2026 by Gnani AI  
**Mandate**: Genuine usage of at least one Gnani AI model/API. (All three are NOT required).

---

## 1. Official Declaration of Gnani Technologies Used

KAVACH AI genuinely integrates and demonstrates **two core Gnani AI voice technologies**:

### 1. Gnani Prisma STT v3.0 (Speech-to-Text)
- **Role in System**: Primary acoustic ingestion engine for multilingual voice call transcription.
- **Official Endpoint**: `POST https://api.vachana.ai/stt/v3`
- **Authentication**: `X-API-Key-ID: <GNANI_API_KEY>` (injected securely on server side; 0% exposure to browser clients).
- **Supported Languages**: English (`en-IN`), Hindi (`hi-IN`), Telugu (`te-IN`), and auto-detected Indic speech (`indic-auto`).
- **Verified Capabilities**: Multipart form delivery, timestamped segment parsing, language identification, and automatic fallback handling in testing.

### 2. Gnani Timbre TTS v2.5 (Text-to-Speech, Beta)
- **Role in System**: Real-time defensive voice warning synthesis for active call victims.
- **Official Endpoint**: `POST https://api.vachana.ai/api/v1/tts/inference`
- **Authentication**: `X-API-Key-ID: <GNANI_API_KEY>`
- **Voices Utilized**: `Nalini` (Hindi / English) and `Chitra` (Telugu).
- **Synthesis Mode**: Standard non-streaming batch synthesis (Request-Response). Delivers localized audible safety guidance (e.g., *"Warning: Police never demand money transfers over video calls"*).

---

## 2. Declaration on Gnani Evon v3.3

- **Status**: **EVALUATED BUT UNINTEGRATED (OPTIONAL)**.
- **Technical Disclosure**: Evaluation requests to `https://api.vachana.ai/v1/chat/completions` returned `403 SCOPE_NOT_ALLOWED` under our competition API key credentials.
- **Ethical Integrity**: In strict adherence to challenge rules, no unauthorized access was attempted, and no fake integration was claimed. Text scenario generation was executed through the local Domain-Curated Multilingual Scenario Engine.
- **Compliance Confirmation**: The challenge requires at least one Gnani AI model. KAVACH AI exceeds this requirement by integrating both Prisma STT and Timbre TTS.

