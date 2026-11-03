# KAVACH AI — User Operation Guide

## 1. Quick Startup Guide
Launch KAVACH AI in under 30 seconds using the automated PowerShell scripts:

```powershell
# Step 1: Run Dependency Setup (first-time only)
.\scripts\setup.ps1

# Step 2: Start All Services (FastAPI Backend + React Frontend)
.\scripts\start.ps1
```

Once started:
- Open your browser to: **`http://localhost:5173`**
- Interactive Swagger API: **`http://127.0.0.1:8000/docs`**

To terminate all running processes:
```powershell
.\scripts\stop.ps1
```

---

## 2. Walkthrough: Analysing a Call Recording

### Step 1: Access Audio Analysis
1. Navigate to **Audio Ingestion & Scan** from the sidebar (`/analyze`).
2. You can either:
   - Click one of the **Preset Test Scenarios** (e.g. *CBI Digital Arrest*, *Bank KYC & OTP Theft*, *Telugu Account Freeze*).
   - Drag & drop a `.wav` or `.mp3` file into the upload zone.
   - Check the microphone consent box and click **Start Microphone Record**.

### Step 2: Configure & Execute Scan
1. Select the transcription language or leave it on **Auto-Detect (Prisma LID)**.
2. Click **EXECUTE KAVACH SCAN**.
3. Watch the real-time pipeline status as it validates the audio, calls **Gnani Prisma v2.5**, executes rule detection, and synthesizes localized voice advisories with **Gnani Timbre v2.5**.

### Step 3: Review Threat Score & Voice Advisory
1. Inspect the **Threat Assessment Verdict**: Risk Score (0–100) and Severity Level (*Critical*, *High*, *Medium*, *Guarded*, *Low*).
2. Listen to the synthesized **Voice Safety Advisory** in Telugu, Hindi, or English.
3. Review the **Triggered Social Engineering Tactics** table detailing each matched keyword and points contribution.

---

## 3. Investigating Incidents & Exporting PDF Reports
1. High-risk calls automatically generate an incident ticket. Click **Open Incident Investigation** or navigate to **Security Incidents** (`/incidents`).
2. In the **Incident Dossier**:
   - Change investigation status (e.g., transition from `New` to `Under Review` or `Confirmed Suspicious`).
   - Listen to the original recorded audio.
   - Read the verbatim transcript and timeline events.
   - Append analyst case notes in the investigation journal.
3. Click **Export Official SOC PDF Report**:
   - The platform will immediately render a formal cybersecurity incident PDF dossier complete with forensic timestamps, tactic tables, and Indian Cybercrime Helpline references (1930).

