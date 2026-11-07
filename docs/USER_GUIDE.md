# KAVACH AI — Operator & User Guide

## 1. Introduction
Welcome to **KAVACH AI** (కవచ్ / कवच), a multilingual voice scam and social-engineering detection platform featuring a Security Operations Center (SOC) incident investigation interface.

This guide provides end-to-end instructions for launching the application, analyzing audio recordings, handling live microphone input, conducting SOC investigations, and training deep learning models.

---

## 2. Quick Start & Launch

### Prerequisites
- Python 3.10 to 3.13 (64-bit)
- Node.js 18+ LTS and npm
- Windows PowerShell, macOS zsh, or Linux bash

### Step 1: Configure Environment
Ensure `backend/.env` contains your configuration:
```bash
GNANI_API_KEY=your_actual_gnani_api_key_here
GNANI_PRISMA_ENDPOINT=https://api.vachana.ai/stt/v3
GNANI_TIMBRE_ENDPOINT=https://api.vachana.ai/api/v1/tts/inference
DEMO_MODE=false
DATABASE_URL=sqlite:///./kavach.db
MAX_UPLOAD_SIZE_MB=25
```

### Step 2: Launch Backend & Frontend
Using the automated PowerShell launch script:
```powershell
.\scripts\start.ps1
```

Or start manually in two terminals:
**Terminal 1 (Backend):**
```powershell
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

**Terminal 2 (Frontend):**
```powershell
cd frontend
npm run dev
```
Open your browser to `http://localhost:5173`.

---

## 3. Workflow 1: Audio Analysis (Upload)
1. Navigate to the **Audio Analysis** page (`/audio`).
2. Drag and drop or browse to select an audio file (`.wav`, `.mp3`, `.m4a`, `.ogg`, `.webm`).
3. Select the primary spoken language:
   - Auto Detect
   - English (`en`)
   - Hindi (`hi`)
   - Telugu (`te`)
   - Telugu-English (`te-en`)
   - Hindi-English (`hi-en`)
4. Click **Analyze Audio**.
5. The system performs:
   - Magic-byte container validation
   - Multilingual transcription via Gnani Prisma v3.0
   - Hybrid Threat Analysis (8-Pillar Rules + Calibrated ML Model)
   - Real-time display of Risk Score (0–100), Threat Categories, and Multilingual Audio Warning.

---

## 4. Workflow 2: Near-Realtime Live Microphone Analysis
1. Navigate to the **Live Analysis** page (`/live`).
2. Read the **Operator Consent Disclosure**:
   > *"I explicitly consent to microphone capture and near-real-time audio processing for suspicious voice pattern detection."*
3. Check the consent box to unlock the microphone interface.
4. Click **Start Live Monitoring**. Speak into the microphone.
5. Audio chunks are transmitted for near-real-time batch analysis.
6. Detected threat patterns, active risk levels, and defensive advisories appear in the live feed.
7. Click **Stop Monitoring** to conclude the session and generate an incident summary.

---

## 5. Workflow 3: SOC Incident Investigation
1. Navigate to the **SOC Dashboard** (`/incidents` or `/`).
2. View real-time security operational metrics:
   - Total Analyzed Calls
   - Critical & High Threats Flagged
   - Open Incidents Requiring Action
   - Threat Breakdown by Category (Authority Impersonation, Digital Arrest, Credential Theft, etc.)
3. Click on any incident to open the **Forensic Investigation Workbench**:
   - Inspect the verbatim transcript with highlighted threat evidence.
   - Review the **Hybrid Analysis Result** (Detection Mode: `HYBRID`, Rule Score vs. ML Score, ML Predicted Class and Confidence).
   - Check the **Audit Timeline** for historical actions taken.
   - Add **Analyst Investigation Notes**.
   - Update incident status (`OPEN`, `INVESTIGATING`, `CONFIRMED_FRAUD`, `FALSE_POSITIVE`, `RESOLVED`).

---

## 6. Workflow 4: PDF Forensic Report Export
1. On the incident details page, click **Export Forensic PDF**.
2. KAVACH AI renders a formal ReportLab PDF dossier containing:
   - Incident Reference ID and UTC Timestamps
   - Detection Mode: `HYBRID` or `RULE_ONLY`
   - Overall Risk Score & Severity Gauge
   - Rule-Pillar Match Details and Snippet Evidence
   - Calibrated ML Prediction Breakdown
   - Actionable Mitigation Guidance
3. The PDF is downloaded directly for legal preservation or cybercrime escalation.

---

## 7. Workflow 5: Deep Learning Training on Google Colab (Future Research)
To train advanced transformer models (`xlm-roberta-base` or `google/muril-base-cased`):
1. Open Google Colab: `https://colab.research.google.com/`
2. Upload the notebook from `notebooks/KAVACH_AI_Multilingual_Training.ipynb`.
3. Set runtime to **GPU (T4 or A100)**: *Runtime → Change runtime type → T4 GPU*.
4. Run all cells sequentially:
   - Uses the expanded 500-sample dataset (`kavach_synthetic_v2`).
   - Evaluates TF-IDF baseline.
   - Fine-tunes PyTorch transformer with weighted cross-entropy.
   - Evaluates on the held-out 75-sample test set.
   - Exports trained model weights and evaluation plots.
*(Note: The Colab notebook is prepared as a future research workflow; transformer training has not been executed locally and no transformer weights are claimed).*

---

## 8. Running Automated Tests
Run the entire backend test suite to verify system integrity:
```powershell
pytest backend/tests/ -v
```
All 52 tests verify API routing, audio format parsing, Gnani Prisma STT, Gnani Timbre TTS, 8-pillar threat detection, rule-priority shields (against both `LEGITIMATE` and `AMBIGUOUS`), educational context precedence, adversarial disclaimer override, ML inference & abstention, and SOC workflows.
