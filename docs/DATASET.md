# KAVACH AI — Synthetic Evaluation Dataset Specification

## 1. Ethical Dataset Charter
In accordance with ethical AI standards and cyber privacy guidelines, **no recordings or transcripts from real scam victims or unauthorized phone intercepts were used**.

The dataset consists of **20 fully synthetic, scripted scenarios** created specifically for research, development, and benchmarking in the Great Indian AI Internship Challenge.

---

## 2. Dataset Composition

| Category | Scenario Count | Languages Represented | Purpose |
| :--- | :---: | :--- | :--- |
| **Scam Attacks** | 10 | Telugu, Hindi, English (Code-mixed) | Measure detection recall across 8 social engineering tactics |
| **Legitimate Calls** | 5 | Telugu, Hindi, English | Verify true negative rate on benign everyday interactions |
| **Ambiguous / Advisories** | 5 | Telugu, Hindi, English | Test negative context suppression on bank security notices |
| **Total** | **20** | **Telugu, Hindi, English** | **Balanced evaluation of precision, recall, and F1** |

---

## 3. Acoustic Environmental Conditions
Each synthetic audio file (`data/synthetic_audio/*.wav`) is synthesized at 16 kHz, 16-bit PCM mono with simulated real-world acoustic profiles:
1. **Clean Speech**: Minimal reverberation and zero background noise.
2. **Low Background Noise**: Ambient room murmur and keyboard typing acoustic noise.
3. **Moderate Noise**: Traffic rumble, café ambient chatter, and call-centre noise.
4. **Telephone Bandpass**: 300 Hz – 3400 Hz narrowband frequency response simulating GSM/VoLTE cellular compression.

---

## 4. Scenario Catalog

### 4.1 Scam Scenarios (10 Scenarios)
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

### 4.2 Legitimate Scenarios (5 Scenarios)
11. `LEGIT-001` (English): **Broadband Customer Service Resolution**
12. `LEGIT-002` (English): **Doctor Appointment Rescheduling**
13. `LEGIT-003` (Hindi/Code-mixed): **E-Commerce Delivery Confirmation**
14. `LEGIT-004` (Telugu/Code-mixed): **Telugu College Admission Certificate Follow-up**
15. `LEGIT-005` (English): **Airline Flight Schedule Delay Advisory**

### 4.3 Ambiguous & Security Advisory Scenarios (5 Scenarios)
16. `AMBIG-001` (English): **HDFC Bank Security Awareness Campaign** (Tests negative context suppression)
17. `AMBIG-002` (English): **Family Emergency Hospital Bill Request** (Tests non-fraud urgency distinction)
18. `AMBIG-003` (Hindi/Code-mixed): **Personal Loan Branch Inquiry** (Legitimate financial discussion)
19. `AMBIG-004` (Telugu/Code-mixed): **Telugu Cyber Police Awareness Announcement** (Negative context suppression)
20. `AMBIG-005` (Hindi/Code-mixed): **Friend Requesting Transit Fare Assistance** (Distinguishes social favors from scams)
