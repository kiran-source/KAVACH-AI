# KAVACH AI — Known Technical Limitations & Responsible AI Disclosures

## 1. Prototype Scope & Research Status
KAVACH AI is developed as an advanced research prototype and submission for the **Great Indian AI Internship Challenge 2026 by Gnani AI**. It is designed as an **AI-assisted decision-support platform** for Security Operations Center (SOC) analysts, enterprise fraud investigators, and citizen protection.

- **Non-Judicial Determination**: Automated risk scores and threat classifications do not constitute legally binding judicial findings. Allegations of criminal fraud must always be independently investigated and verified by certified law enforcement authorities.
- **Prototype Status — Not Commercial Production**: Model and system evaluation is conducted strictly on domain-curated synthetic data. **High synthetic benchmark accuracy does not establish or guarantee real-world telephony accuracy in commercial deployments.** Real-world telephony introduces unconstrained acoustic distortion, varying packet loss, non-standard codecs (AMR 8kHz), ambient street noise, multiple simultaneous speakers, and emergent regional slang absent from synthetic corpora.

---

## 2. Dataset & Label Limitations
- **Synthetic Data**: Datasets v1 (100 conversations), v2 (500 conversations), and v3 (3,000 conversations) are domain-curated synthetic datasets. Evaluation metrics reflect performance on domain scenario archetypes, not wild telephony audio.
- **Unverified Labels (`pending_review`)**: 100% of records in Dataset v3 carry `annotation_status: "pending_review"`. The labels reflect automated domain curation rather than certified human ground-truth annotation.
- **Cross-Split Lexical Similarity**: Domain-specific synthetic dialogues in banking, courier, and telecom naturally share institutional terminology. Split isolation is enforced via 0% scenario-family overlap, 0% exact dialogue text hash, and 0% CID overlap across train, validation, and test splits.
- **Adversarial Disclaimer Robustness**: Scammers frequently weaponize institutional disclaimers ("RBI guidelines state..."). The hybrid engine overrules educational suppression when active coercion or credential extraction is present, but novel adversarial phrasing will always require ongoing defense updates.
- **Acoustic Dataset Scope**: Synthesized audio files exist in `data/synthetic_audio/`. Full audio synthesis for all 3,000 multi-turn text conversations would exceed workstation storage limits and was not required for textual NLP classification.

---

## 3. External API Dependencies & Scope Restrictions
- **Gnani Evon v3.3 Scope**: Probed and returned `403 SCOPE_NOT_ALLOWED` under current challenge API credentials. In strict compliance with guidelines, Evon was not integrated and is transparently documented as optional.
- **Gnani Prisma v3.0 & Timbre v2.5**: Both endpoints are genuine and integrated. Network latency or external provider maintenance may occasionally cause ASR or TTS latency spikes; the system includes automatic backoff retries and graceful fallback.
- **TTS Synthesis Mode**: Timbre v2.5 integration uses standard non-streaming request-response batch synthesis. Streaming audio synthesis is not claimed or implemented.

---

## 4. Telephony Interception & Audio Capture Boundaries
- **Zero Carrier Interception**: KAVACH AI does **not** tap, wiretap, or intercept cellular carrier networks (GSM, LTE, 5G, PSTN). It operates strictly on audio voluntarily uploaded by users or recorded through authorized browser microphone permissions.
- **Near-Real-Time Batch Audio**: Browser Web Audio APIs do not natively support full-duplex socket-level telephony interception. Live microphone analysis is conducted via chunked batch processing with explicit user consent.
- **Acoustic Degradation**: Low-bitrate telephony codecs (e.g. AMR-NB 8 kHz), severe acoustic reverberation, loud background street traffic, or overlapping speaker babble can increase Automatic Speech Recognition (ASR) Word Error Rate (WER), indirectly affecting downstream classification.

---

## 5. Machine Learning Latencies & Hardware Profiles
- **Production Baseline v1**: Calibrated TF-IDF + Logistic Regression model with measured CPU inference latency of **Mean: 11.68 ms, P50: 10.27 ms, P95: 23.06 ms** (~553 KB artifact footprint).
- **TF-IDF v3**: Calibrated TF-IDF + Logistic Regression on Dataset v3 with measured CPU inference latency of **Mean: 4.29 ms, P50: 4.22 ms, P95: 5.74 ms** (~566 KB artifact footprint).
- **Google MuRIL v1 Transformer**: Fine-tuned 237M parameter transformer (`google/muril-base-cased`) with measured CPU inference latency of **Mean: 1,543.21 ms, P50: 1,454.09 ms, P95: 2,289.55 ms** (~950 MB footprint).
- **Selective Hybrid Engine**: Evaluates Stage 0 rules and Stage 1 TF-IDF for 100% of calls, selectively invoking MuRIL for only ~32% of ambiguous or code-mixed calls. Measured CPU latency: **Mean: 498.12 ms, P50: 4.29 ms, P95: 1,547.50 ms**, reducing transformer compute overhead by **68.0%**.
- **CPU Inference Disclosure**: While MuRIL inference is fully functional on standard CPU without requiring CUDA, per-turn latency is ~1.5s. Quantization (INT8/ONNX) is recommended for commercial high-concurrency telephony deployments.

---

## 6. Emergency Incident Reporting
In any scenario involving active extortion, kidnapping threats, digital arrest coercion, or immediate financial loss:
- **Disconnect the call immediately.**
- **Dial 1930** (Indian National Cyber Crime Helpline).
- Register a report on the official portal: **https://cybercrime.gov.in**.
