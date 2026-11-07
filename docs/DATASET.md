# KAVACH AI — Synthetic Evaluation Dataset Specification & Provenance

## 1. Ethical Dataset Charter
In accordance with ethical AI standards and cyber privacy guidelines, **no recordings or transcripts from real scam victims or unauthorized phone intercepts were used**.

The dataset consists of **20 fully synthetic, scripted scenarios** created specifically for research, development, and benchmarking in the Great Indian AI Internship Challenge.

---

## 2. Dataset Composition & Provenance

| Category | Scenario Count | Languages Represented | Neural Voice Engine | Purpose |
| :--- | :---: | :--- | :--- | :--- |
| **Scam Attacks** | 10 | Telugu, Hindi, English (Code-mixed) | `te-IN-MohanNeural`, `hi-IN-SwaraNeural`, `en-IN-NeerjaNeural` | Measure detection recall across 8 social engineering tactics |
| **Legitimate Calls** | 5 | Telugu, Hindi, English | `te-IN-MohanNeural`, `hi-IN-SwaraNeural`, `en-IN-NeerjaNeural` | Verify true negative rate on benign everyday interactions |
| **Ambiguous / Advisories (Held-Out)** | 5 | Telugu, Hindi, English | `te-IN-MohanNeural`, `hi-IN-SwaraNeural`, `en-IN-NeerjaNeural` | Test negative context suppression on bank security notices and false-positive resilience |
| **Total** | **20** | **Telugu, Hindi, English** | **Microsoft Regional Neural TTS** | **Balanced evaluation of precision, recall, and F1** |

Full machine-readable metadata and sample properties are archived in `data/DATASET_PROVENANCE.json`.

---

## 3. Acoustic Environmental Conditions & Audio Specs
Each synthetic audio file (`data/synthetic_audio/*.wav`) is synthesized at **16 kHz, 16-bit PCM mono** with authentic digital signal processing filters:
1. **Clean Speech**: Baseline neural audio with zero additive background noise.
2. **Low Background Noise**: Ambient room murmur and subtle acoustic noise (~30 dB SNR).
3. **Moderate Noise**: Urban/traffic rumble and background acoustic chatter (~18 dB SNR).
4. **Telephone Bandpass**: 300 Hz – 3400 Hz 4th-order Butterworth bandpass filter with calibrated 50 Hz power-line hum and channel noise simulating GSM/VoLTE cellular compression.

---

## 4. Evaluation Integrity & Benchmarking Separation

To ensure scientific honesty and prevent overclaiming:

1. **Benchmark Layer 1 — Rule & Pattern Matching Engine (Text Ground-Truth)**:
   - Evaluates the core multi-layer threat detector, urgency weighting, authority impersonation, and suppression logic against canonical transcripts.
   - Result: 100% precision and recall on the 20 benchmark scenarios.

2. **Benchmark Layer 2 — Automatic Speech Recognition (Gnani Prisma STT)**:
   - Evaluates word-error-rate (WER) and phrase fidelity when transcribing regional spoken audio under varying SNR and telephony codecs.
   - Gnani Prisma accurately transcribes clean and code-mixed inputs; telephone-band noise introduces slight word substitutions on rare terms.

3. **Benchmark Layer 3 — End-to-End Audio-to-Detection Pipeline**:
   - Audio is ingested -> transcribed via Prisma V3.0 -> normalized -> analyzed via the threat engine -> incident generated -> Timbre audio advisory triggered.
   - Held-Out Scenarios (`AMBIG-001` to `AMBIG-005`) evaluate false-positive resistance on security advisories (e.g., bank warning letters mentioning "do not share OTP").

> **Notice on Real-World Generalization**: The 100% metrics reported in the evaluation dashboard apply strictly to the 20 calibrated benchmark scenarios. Real-world scam calls exhibit open-vocabulary dialect variations, heavy regional accents, emotional vocal stress, and unpredictable packet loss. Real-world efficacy requires continuous adaptation and human-in-the-loop incident triage.

---

## 5. Scenario Catalog

### 5.1 Scam Scenarios (10 Scenarios)
1. `SCAM-001` (Hindi/Code-mixed): **Digital Arrest CBI Narcotics Threat** (Urgency, Authority Impersonation, Isolation, Digital Arrest)
2. `SCAM-002` (English): **SBI KYC Verification and OTP Theft** (Credential Theft, Urgency)
3. `SCAM-003` (Telugu/Code-mixed): **Telugu Bank Account Block and PIN Demand** (Credential Theft, Threats)
4. `SCAM-004` (Hindi/Code-mixed): **Electricity Disconnection QuickSupport APK** (Remote Access, Urgency, Financial Fraud)
5. `SCAM-005` (English): **FedEx Customs Narcotics Seizure** (Courier Fraud, Authority Impersonation, Financial Fraud)
6. `SCAM-006` (Hindi/Code-mixed): **AnyDesk Remote Banking Access** (Remote Access, Credential Theft)
7. `SCAM-007` (Telugu/Code-mixed): **Telugu Police Cyber Cell Arrest Threat** (Authority Impersonation, Financial Fraud, Isolation)
8. `SCAM-008` (English): **Supreme Court Warrant & Continuous Skype Monitoring** (Digital Arrest, Authority Impersonation)
9. `SCAM-009` (Hindi/Code-mixed): **Fake Income Tax Refund with CVV Request** (Credential Theft, Authority Impersonation)
10. `SCAM-010` (Telugu/Code-mixed): **Telugu Remote APK Install for Loan Approval** (Remote Access, Credential Theft)

### 5.2 Legitimate Scenarios (5 Scenarios)
11. `LEGIT-001` (English): **Broadband Customer Service Resolution**
12. `LEGIT-002` (English): **Doctor Appointment Rescheduling**
13. `LEGIT-003` (Hindi/Code-mixed): **E-Commerce Delivery Confirmation**
14. `LEGIT-004` (Telugu/Code-mixed): **Telugu College Admission Certificate Follow-up**
15. `LEGIT-005` (English): **Airline Flight Schedule Delay Advisory**

### 5.3 Ambiguous & Security Advisory Scenarios (Held-Out Evaluation Set)
16. `AMBIG-001` (English): **HDFC Bank Security Awareness Campaign** (Tests negative context suppression)
17. `AMBIG-002` (English): **Family Emergency Hospital Bill Request** (Tests non-fraud urgency distinction)
18. `AMBIG-003` (Hindi/Code-mixed): **Personal Loan Branch Inquiry** (Legitimate financial discussion)
19. `AMBIG-004` (Telugu/Code-mixed): **Telugu Cyber Police Awareness Announcement** (Negative context suppression)
20. `AMBIG-005` (Hindi/Code-mixed): **Friend Requesting Transit Fare Assistance** (Distinguishes social favors from scams)
