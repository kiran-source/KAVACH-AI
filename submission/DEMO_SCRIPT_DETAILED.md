# KAVACH AI — Detailed 2–3 Minute Video Demonstration Script

**Target Duration**: 2 Minutes 30 Seconds  
**Format**: Comprehensive technical walkthrough for jury evaluators  
**Tone**: Authoritative, professional, cybersecurity and AI-focused

---

## 1. Introduction & Problem Architecture (0:00 – 0:35)

**Visuals**:
- Open on KAVACH AI Landing Page and transition to SOC Dashboard (`http://localhost:5173/dashboard`).
- Cursor points to real-time incident severity breakdown, language distribution charts, and provider health badges.

**Spoken Narration**:
> *"Hello evaluators. Welcome to KAVACH AI, an enterprise-grade voice scam interception and incident response platform developed for the Great Indian AI Internship Challenge by Gnani AI. In India today, voice-based social engineering has evolved beyond simple phishing. Criminal syndicates now execute psychological extortion using Digital Arrest threats, CBI impersonation, electricity bill cutoff blackmail, and fake customs seizures—frequently conversing in regional languages like Hindi and Telugu or code-mixed dialects like Hinglish and Tenglish. KAVACH AI solves this by combining Gnani AI's state-of-the-art speech intelligence with a multi-paradigm hybrid threat detection engine."*

---

## 2. Ingestion & Gnani Prisma STT v3.0 (0:35 – 1:10)

**Visuals**:
- Navigate to `Audio Analysis` page (`http://localhost:5173/analysis`).
- Select audio file: `scam-001_telephone-band.wav` (A CBI Digital Arrest extortion call in Hindi-English).
- Click `Start Analysis`. Show loading progress indicator.
- Display timestamped transcription rendered segment by segment.

**Spoken Narration**:
> *"Let's test an active extortion scenario: a caller impersonating a police inspector alleging money laundering in an intercepted courier. The user uploads the audio recording. KAVACH AI immediately validates the file's binary magic bytes to prevent file-injection attacks and transmits the audio to Gnani Prisma STT v3.0. As you can see, Prisma accurately transcribes the rapid code-mixed speech, preserves the Devanagari and Romanized phrases, and timestamps each conversational turn."*

---

## 3. The Cascaded Hybrid Threat Engine (1:10 – 1:50)

**Visuals**:
- Zoom into Threat Intelligence Card.
- Highlight:
  - `Verdict: SCAM`
  - `Risk Score: 95.0 / 100 (Severity: Critical)`
  - `Rule-Priority Shield: ACTIVE`
  - Threat taxonomy pills: `Digital Arrest`, `Authority Impersonation`, `Financial Coercion`.
- Open Multi-Stage Telemetry Drawer showing Stage 0, Stage 1 (TF-IDF v3), and Stage 2 (Google MuRIL v1).

**Spoken Narration**:
> *"Once transcribed, the conversation passes through our three-stage cascaded intelligence pipeline. First, Stage 0—our deterministic Rule-Priority Shield—scans for high-stakes cyber extortion keywords. Under our zero-downgrade safety invariant, critical extortion triggers like Digital Arrest are permanently locked to SCAM with a risk score of at least 85, ensuring statistical AI models can never downgrade an active scam to legitimate. For standard calls, Stage 1 TF-IDF v3 executes in just 4.29 milliseconds. For ambiguous or code-mixed phrases, the engine selectively escalates to our fine-tuned 237-million parameter Google MuRIL transformer. This selective architecture cuts transformer compute overhead by 68 percent while delivering zero false negatives."*

---

## 4. Real-Time Defensive Voice Warning via Gnani Timbre (1:50 – 2:10)

**Visuals**:
- Click `Play Voice Warning` on the audio card.
- Play the audible synthesized voice warning through speakers.
- Show localized warning text displayed on screen: *"Warning! Law enforcement agencies never arrest citizens over video calls..."*

**Spoken Narration**:
> *"Detection alone is insufficient if the victim remains on the line. KAVACH AI immediately invokes Gnani Timbre TTS v2.5 to synthesize an audible defensive warning in the victim's language. Timbre's clear voice warns the user not to transfer funds and prompts them to terminate the call immediately."*

---

## 5. SOC Incident Management & Forensic PDF Export (2:10 – 2:30)

**Visuals**:
- Navigate to `Incidents` page. Show new auto-generated incident `INC-XXXXX`.
- Click into `Incident Detail`. Show chronological timeline log and evidence audit trail.
- Click `Generate Forensic PDF`. Open generated tamper-evident ReportLab PDF report.

**Spoken Narration**:
> *"Finally, KAVACH AI automatically logs the incident into the SOC console, complete with risk score history, matched regex indicators, and evidence checksums. With a single click, analysts can generate a tamper-evident forensic PDF dossier ready for immediate submission to the National Cybercrime Helpline at 1930."*

---

## 6. Closing (2:30 – 2:40)

**Visuals**:
- Return to Dashboard. Display Gnani AI logo and project credentials.

**Spoken Narration**:
> *"Tested across 78 automated regression tests with 100 percent pass rate, KAVACH AI demonstrates how Gnani AI's voice technology can actively protect Indian citizens from voice fraud. Thank you."*

