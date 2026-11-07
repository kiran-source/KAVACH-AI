# KAVACH AI — Demonstration Scenarios & Validation Scripts

**Purpose**: Standardized walkthrough scenarios for competition evaluators, live jury demonstrations, and video screen recordings.  
**Provenance Disclosure**: Scenarios are derived from synthetic generation archetypes. All records carry `annotation_status: pending_review`. They illustrate real-world scam structures but do not contain actual victim PII.

---

## Scenario 1: High-Stakes "Digital Arrest" Coercion (English)

- **Type**: Cyber Extortion / Law Enforcement Impersonation
- **Language**: English (`en`)
- **Provenance**: Synthetic Archetype `scam_digital_arrest_cbi_01` (`pending_review`)
- **Dialogue Transcript**:
  > *"I am Inspector Raman from CBI Headquarters New Delhi. Your Aadhaar number has been found registered in a high-profile narcotics trafficking and money laundering courier intercepted at Mumbai Customs. An immediate non-bailable arrest warrant has been issued against you by the Supreme Court. You are placed under digital arrest right now. Do not disconnect this video call, do not inform family members, and stay in your room. To verify your assets and avoid physical arrest, transfer a refundable verification deposit of 50,000 rupees to the designated RBI safe custody account immediately."*
- **KAVACH AI Detection Telemetry**:
  - **Verdict**: **SCAM**
  - **Risk Score**: `95.0 / 100` (Severity: `Critical`)
  - **Stage 0 Rule Shield**: `ACTIVE` (Critical match: Digital Arrest, Law Enforcement Impersonation, Coercive Demand)
  - **Zero-Downgrade Invariant**: Enforced (Risk floor $\ge 85.0$)
  - **Generated Voice Warning (Gnani Timbre)**: *"Warning! Law enforcement agencies never arrest citizens over video calls or demand money transfers. Disconnect immediately."*

---

## Scenario 2: Urgent Electricity Disconnection Extortion (Hindi)

- **Type**: Public Utility Extortion
- **Language**: Hindi (`hi`)
- **Provenance**: Synthetic Archetype `scam_electricity_urgency_02` (`pending_review`)
- **Dialogue Transcript**:
  > *"नमस्ते महोदय, मैं राज्य बिजली बोर्ड मुख्यालय से बात कर रहा हूँ। आपके मीटर का पिछला बिल 4,850 रुपये अभी तक अपडेट नहीं हुआ है। यदि आपने तुरंत भुगतान नहीं किया, तो आज रात ठीक 9:30 बजे आपके घर का बिजली कनेक्शन स्थायी रूप से काट दिया जाएगा। लाइनमैन पहले ही आपके इलाके में रवाना हो चुका है। कनेक्शन कटने से बचाने के लिए तुरंत हमारे अधिकारी के यूपीआई नंबर पर पैसे भेजें और व्हाट्सएप पर रसीद दिखाएं।"*
- **KAVACH AI Detection Telemetry**:
  - **Verdict**: **SCAM**
  - **Risk Score**: `90.0 / 100` (Severity: `Critical`)
  - **Stage 0 Rule Shield**: `ACTIVE` (Matched: Urgency & Threats, Fake Utility Cutoff)
  - **Generated Voice Warning (Gnani Timbre)**: *"सावधान! बिजली विभाग कभी भी फोन पर तुरंत यूपीआई भुगतान करने के लिए नहीं कहता। यह एक फ्रॉड कॉल हो सकती है।"*

---

## Scenario 3: Code-Mixed Banking KYC & OTP Harvesting (Hinglish)

- **Type**: Credential Harvesting & Banking Fraud
- **Language**: Hinglish (`hi-en`)
- **Provenance**: Synthetic Archetype `scam_banking_otp_codemixed_03` (`pending_review`)
- **Dialogue Transcript**:
  > *"Hello sir, good afternoon. Main State Bank customer care head office se call kar raha hoon. Sir aapke account ka mandatory KYC verification pending hai aur RBI ke new circular ke mutabiq aapka debit card agle 2 ghante me permanently block ho jayega. Maine aapke registered mobile par ek verification code bheja hai. Please apna 6-digit OTP share karein taaki main system me aapka account activate kar sakun."*
- **KAVACH AI Detection Telemetry**:
  - **Verdict**: **SCAM**
  - **Risk Score**: `95.0 / 100` (Severity: `Critical`)
  - **Stage 1 (TF-IDF)**: Detects code-mixed terms; confidence drops to 0.74.
  - **Stage 2 (MuRIL)**: Selectively escalated with reason `LOW_CONFIDENCE_0.74_BELOW_0.85`. MuRIL confirms `SCAM` with 0.98 probability.
  - **Decision Fusion**: Fused SCAM verdict with credential harvesting alert.

---

## Scenario 4: Routine Banking Service Advisory (Legitimate)

- **Type**: Non-Malicious Customer Service
- **Language**: English (`en`)
- **Provenance**: Synthetic Archetype `legitimate_customer_service_01` (`pending_review`)
- **Dialogue Transcript**:
  > *"Good morning Mr. Sharma, this is Priya calling from HDFC Bank customer relations. We noticed you recently submitted an online request to update your mailing address for your savings account. I am just calling to verify if you initiated this request and to inform you that your new checkbook will arrive within five business days. We do not require any password, PIN, or confidential details for this confirmation."*
- **KAVACH AI Detection Telemetry**:
  - **Verdict**: **LEGITIMATE**
  - **Risk Score**: `10.0 / 100` (Severity: `Low`)
  - **Stage 1 (TF-IDF Fast Path)**: `LEGITIMATE` (Confidence: 0.96; Latency: 4.2 ms).
  - **Stage 2 (MuRIL)**: Bypassed (Fast path saves compute).
  - **Voice Warning**: None (Clean status).

---

## Scenario 5: Borderline Telemarketing with Pushy Pitch (Ambiguous)

- **Type**: Gray-Area Ambiguity / Suspicious Telemarketing
- **Language**: English (`en`)
- **Provenance**: Synthetic Archetype `ambiguous_telemarketing_01` (`pending_review`)
- **Dialogue Transcript**:
  > *"Hello sir, you have been specially pre-selected for a pre-approved personal loan of five lakh rupees with zero documentation. This special interest rate of 8.5 percent is strictly valid only for the next thirty minutes. If you want to claim this exclusive offer, please confirm your date of birth and company name so I can forward your application to our credit manager right now."*
- **KAVACH AI Detection Telemetry**:
  - **Verdict**: **AMBIGUOUS**
  - **Risk Score**: `40.0 / 100` (Severity: `Guarded` / `Elevated`)
  - **Stage 1 (TF-IDF)**: Outputs `AMBIGUOUS` (Confidence: 0.62).
  - **Stage 2 (MuRIL)**: Escalated due to ambiguous classification. MuRIL classifies as `AMBIGUOUS`.
  - **Analyst Advisory**: Marked for monitoring; user advised: *"Proceed with caution. Do not reveal sensitive details to unverified cold callers."*

