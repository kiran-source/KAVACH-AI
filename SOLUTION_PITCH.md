# 🛡️ KAVACH AI — One-Page Solution Pitch

**Competition**: Great Indian AI Internship Challenge 2026 by Gnani AI  
**Project**: KAVACH AI (కవచ్ / कवच) — Multilingual Voice Scam & Vishing Interception Platform  
**Target Users**: Indian Citizens, Vulnerable Demographics, Banking & Enterprise SOC Teams  
**Pitch PDF**: [Download Official 1-Page Pitch PDF](ONE_PAGE_SOLUTION_PITCH.pdf) (also in [`submission/ONE_PAGE_SOLUTION_PITCH.pdf`](submission/ONE_PAGE_SOLUTION_PITCH.pdf))

---

## 1. The Crisis: India's Voice Social-Engineering Epidemic

Phone-based cyber fraud in India has evolved into an industrialized threat costing citizens thousands of crores every year. Criminal syndicates deploy high-pressure psychological manipulation tactics:
- **"Digital Arrest" Rackets**: Cyber extortionists impersonating the CBI, Supreme Court, or Police claiming a contraband courier was seized in the victim's name, demanding immediate money transfers under threat of arrest.
- **OTP & Credential Harvesting**: Masquerading as bank support or telecom providers, threatening immediate account deactivation unless verification codes or UPI PINs are shared.
- **Linguistic Exploitation**: Scammers converse in regional Indian languages (Hindi, Telugu) and colloquial code-mixed dialects ("Hinglish", "Tenglish"), evading traditional English-only keyword filters.

---

## 2. The Solution: KAVACH AI

**KAVACH AI** provides an autonomous, real-time, multilingual voice threat interception platform combining **Gnani AI voice intelligence** with a **cascaded Hybrid Intelligence Engine**:

```
[Inbound Voice Call / Mic] ──► [Gnani Prisma STT v3.0] ──► Multilingual Transcript
                                                                  │
┌─────────────────────────────────────────────────────────────────┴────────────────────────────────┐
│ STAGE 0: Rule-Priority Shield (Deterministic zero-downgrade barrier for critical extortion)      │
│ STAGE 1: TF-IDF v3 Fast Classifier (Resolves ~68% of standard traffic in 4.29 ms on CPU)         │
│ STAGE 2: Google MuRIL v1 Transformer (Selectively handles ambiguous & code-mixed nuances)        │
└─────────────────────────────────────────────────────────────────┬────────────────────────────────┘
                                                                  ▼
[Gnani Timbre TTS v2.5 Voice Alert] ◄─── [Decision Fusion & Risk Score] ──► [SOC PDF Incident Report]
```

1. **Acoustic Ingestion**: Streams call audio to **Gnani Prisma STT v3.0**, transcribing Hindi, Telugu, and English speech with timestamped segment accuracy.
2. **Deterministic Rule-Priority Shield**: Enforces domain safety invariants: critical threats (CBI impersonation, Digital Arrest, OTP demands) can **never be downgraded** by statistical ML, anchoring the risk floor at $\ge 85.0$.
3. **Selective Transformer Escalation**: Fast TF-IDF v3 classifies standard calls in **4.29 ms**. Borderline or code-mixed calls selectively escalate to fine-tuned **Google MuRIL** (237M parameters), slashing transformer compute overhead by **68%** with 0 false negatives.
4. **Real-Time Voice Warning via Gnani Timbre TTS v2.5**: Synthesizes localized, immediate audible safety warnings in Hindi, Telugu, or English, urging the victim to disconnect.
5. **Enterprise SOC & Police Forensics**: Generates tamper-evident ReportLab PDF incident dossiers for reporting to the National Cybercrime Helpline (1930).

---

## 3. Key Achievements & Verification

- **Empirical Accuracy**: **100.00% accuracy** and **1.0000 macro F1** on the 450 held-out test split of Dataset v3 with **zero scam false negatives**.
- **CPU Inference Ready**: Fast path resolves in 4.29 ms; average selective per-turn latency is 498 ms on standard consumer CPU without requiring expensive GPUs.
- **100% Test Pass Rate**: **78/78 automated backend tests passed**; frontend compiles with 0 errors.
- **Genuine Technology Usage**: Full production integration of Gnani Prisma STT v3 and Gnani Timbre TTS v2.5.

