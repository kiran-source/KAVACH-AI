# KAVACH AI — Project Description

**Project Title**: KAVACH AI — Multilingual Voice Scam Detection & Incident Response Platform  
**Competition**: Great Indian AI Internship Challenge 2026 by Gnani AI  
**Track**: Voice AI / Cyber Threat Detection / Social Engineering Defense  

---

## 1. Problem Statement & Background

Voice fraud ("vishing") and phone-based social engineering have reached epidemic proportions in India. According to national cybercrime statistics, citizens lose thousands of crores annually to sophisticated telephone rackets. Prominent attack vectors include:
- **"Digital Arrest" Rackets**: Cybercriminals posing as CBI, Enforcement Directorate (ED), or state cyber police, coercing victims into continuous video surveillance and extorting "bail" or "asset verification" deposits.
- **OTP & Credential Harvesting**: Fraudsters masquerading as bank customer service or telecom agents threatening immediate account freezing unless a one-time password or UPI PIN is disclosed.
- **Urgent Utility Blackmail**: Extortion calls threatening immediate power cut-off at 9:30 PM unless a private UPI payment is completed.
- **Remote Access Exploitation**: Directing victims to install remote desktop tools (AnyDesk, TeamViewer) or malicious sideloaded APK files under the guise of customer support.

These scams succeed because they exploit **psychological coercion, fear, and linguistic familiarity**. Scammers frequently converse in regional Indian languages (Hindi, Telugu) and colloquial code-mixed dialects ("Hinglish", "Tenglish"), bypassing traditional English-only keyword filters.

---

## 2. Target Users

1. **Individual Citizens & Vulnerable Demographics**: Senior citizens, gig workers, and everyday banking customers who require real-time defensive guidance during suspicious phone calls.
2. **Enterprise & Banking SOC Teams**: Security Operations Centers monitoring fraud patterns, corporate helpdesks, and customer relationship centers.
3. **Law Enforcement & Fraud Investigators**: Cyber crime cells requiring tamper-evident, timestamped forensic dossiers and evidence logs to pursue criminal rackets.

---

## 3. The KAVACH AI Solution

KAVACH AI provides a unified, multilingual, privacy-preserving defense platform that pairs **Gnani AI voice technologies** with a **cascaded Hybrid Intelligence Engine**:
- **Speech-to-Text via Gnani Prisma v3.0**: Real-time multilingual transcription supporting Indic dialects, automatic language identification, and timestamped speech segment extraction.
- **Multi-Paradigm Scam Detection**:
  - *Stage 0 (Rule-Priority Shield)*: Zero-latency deterministic rules that enforce non-downgradable scam classifications for explicit cyber extortion.
  - *Stage 1 (TF-IDF v3 Fast Path)*: Calibrated statistical n-gram classifier resolving standard calls in **4.29 ms** on CPU.
  - *Stage 2 (Google MuRIL v1 Deep Path)*: 237M-parameter multilingual transformer selectively invoked for ambiguous or code-mixed calls, cutting transformer compute overhead by **68%**.
- **Real-Time Voice Advisory via Gnani Timbre v2.5**: Synthesizes localized, clear defensive voice alerts (in Hindi, Telugu, or English) warning victims not to share credentials.
- **Forensic SOC Console**: Incident tracking, evidence custody logging, and automated ReportLab PDF dossier generation for police reporting.

---

## 4. Practical Impact & Societal Value

- **Democratizing Cyber Defense**: Protects non-English-speaking citizens by delivering voice alerts in their native mother tongue.
- **Zero Downgrade Guarantee**: The deterministic Rule-Priority Shield ensures that AI models never accidentally dismiss an active extortion call as "legitimate".
- **Hardware Accessibility**: Designed to execute smoothly on standard consumer CPUs without requiring multi-thousand dollar GPUs, ensuring widespread deployment readiness.

