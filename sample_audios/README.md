# 🎧 KAVACH AI — Testing Audio Library

This directory contains pre-generated, validated audio test files (`.wav`) specifically calibrated for testing the **KAVACH AI** voice threat detection pipeline.

You can test these files either by:
1. **Frontend Web UI**: Drag and drop any `.wav` file into the upload zone at `/` or `/analysis`.
2. **FastAPI Swagger / cURL**: POST to `/api/v1/audio/upload` followed by `/api/v1/transcription/{audio_id}`.

---

## 1. Core Evaluation Audio Files

| File Name | Scenario | Expected Verdict | Expected Risk | Key Indicators Tested |
| :--- | :--- | :---: | :---: | :--- |
| `01_scam_digital_arrest_cbi.wav` | **CBI Digital Arrest Extortion** | `SCAM` | **Critical (95-100)** | Authority Impersonation & Digital Arrest |
| `02_scam_bank_kyc_otp_fraud.wav` | **Bank KYC Suspension & OTP Theft** | `SCAM` | **Critical (90-98)** | Credential Harvesting (OTP & UPI PIN) |
| `03_scam_anydesk_electricity_threat.wav` | **Electricity Cutoff & AnyDesk Remote Access** | `SCAM` | **Critical (90-95)** | Remote Access APK Sideloading |
| `04_scam_customs_contraband_courier.wav` | **Customs Contraband Narcotics Extortion** | `SCAM` | **Critical (92-96)** | Customs Contraband & Financial Redirection |
| `05_legit_broadband_customer_support_safe.wav` | **Customer Support Ticket Resolution** | `LEGITIMATE` | **Safe / Low (5-15)** | None (Routine Business) |
| `06_legit_bank_security_awareness_advisory.wav` | **Bank Security Awareness Advisory** | `LEGITIMATE` | **Safe / Zero (0-10)** | None (Educational Precedence Guard) |
| `07_ambiguous_courier_delivery_verification.wav` | **Courier Chequebook Delivery Inquiry** | `AMBIGUOUS` | **Moderate (30-50)** | Borderline / Escalates to MuRIL |

---

## 2. Spoken Audio Transcripts

### 🔊 `01_scam_digital_arrest_cbi.wav`
- **Verdict**: `SCAM` | **Risk**: Critical (95-100)
- **Duration**: 32.46s | **Size**: 1397.9 KB
- **Transcript**:
> *"Namaste. I am Inspector Sharma calling from Central Bureau of Investigation CBI headquarters New Delhi. A courier parcel containing fake passports and contraband narcotics was seized in Mumbai registered under your Aadhaar number. Supreme Court has issued an immediate non-bailable warrant. You are placed under Digital Arrest right now. Do not disconnect this video call or inform your family, otherwise a police team will arrest you within one hour."*

### 🔊 `02_scam_bank_kyc_otp_fraud.wav`
- **Verdict**: `SCAM` | **Risk**: Critical (90-98)
- **Duration**: 22.81s | **Size**: 982.2 KB
- **Transcript**:
> *"Good morning sir, this is Rajesh calling from State Bank of India KYC verification desk. Your net banking access and debit card are suspended due to pending biometric KYC update. To unfreeze your account immediately, share the six digit OTP received on your mobile and confirm your UPI PIN right now."*

### 🔊 `03_scam_anydesk_electricity_threat.wav`
- **Verdict**: `SCAM` | **Risk**: Critical (90-95)
- **Duration**: 18.55s | **Size**: 798.7 KB
- **Transcript**:
> *"Dear consumer, your electricity meter bill payment has failed and power supply will be disconnected tonight at eight pm. Open Google Play Store immediately and install AnyDesk QuickSupport application. Share the nine digit code with our support agent to update your payment status."*

### 🔊 `04_scam_customs_contraband_courier.wav`
- **Verdict**: `SCAM` | **Risk**: Critical (92-96)
- **Duration**: 20.68s | **Size**: 890.5 KB
- **Transcript**:
> *"This is Customs and Border Protection officer at Mumbai International Airport. A DHL courier consigned to your name containing fifty grams of illegal narcotics has been intercepted. Transfer ninety thousand rupees to the RBI safe verification account immediately to avoid criminal detention."*

### 🔊 `05_legit_broadband_customer_support_safe.wav`
- **Verdict**: `LEGITIMATE` | **Risk**: Safe / Low (5-15)
- **Duration**: 23.02s | **Size**: 991.2 KB
- **Transcript**:
> *"Hello, thank you for reaching out to customer care regarding your fiber broadband speed issue. Our technician has resolved the fiber line attenuation at your local node, and ticket number 4819 is now closed. Please let us know if your internet connection is working smoothly. Have a pleasant day."*

### 🔊 `06_legit_bank_security_awareness_advisory.wav`
- **Verdict**: `LEGITIMATE` | **Risk**: Safe / Zero (0-10)
- **Duration**: 24.43s | **Size**: 1052.0 KB
- **Transcript**:
> *"Dear customer, this is an official security awareness announcement from your bank. Please remember that bank officials and police never ask for your confidential OTP, UPI PIN, or passwords over the phone. Stay safe from scam calls and beware of fake digital arrest threats. Report cyber fraud on helpline 1930."*

### 🔊 `07_ambiguous_courier_delivery_verification.wav`
- **Verdict**: `AMBIGUOUS` | **Risk**: Moderate (30-50)
- **Duration**: 23.52s | **Size**: 1012.8 KB
- **Transcript**:
> *"Hello, am I speaking with the account holder? This is DTDC courier dispatch team regarding a speed post parcel from HDFC Bank containing your renewed checkbook. Nobody was available at your registered address this afternoon. Could you please confirm if you will be available tomorrow between ten am and two pm for delivery?"*

---

## 3. Multilingual Regional Audio Files (`sample_audios/multilingual/`)

| File Name | Language / Dialect | Category | Description |
| :--- | :--- | :---: | :--- |
| `hindi_cbi_digital_arrest_scam.wav` | Hindi (`hi-IN`) | `SCAM` | Fake police officer extortion in colloquial Hindi |
| `telugu_bank_kyc_otp_scam.wav` | Telugu (`te-IN`) | `SCAM` | Bank KYC suspension threat in Telugu |
| `hinglish_customs_parcel_scam.wav` | Hindi-English Code-Mixed | `SCAM` | Narcotics courier extortion in Hinglish |
| `tenglish_lottery_prize_scam.wav` | Telugu-English Code-Mixed | `SCAM` | Telecom prize claim fee in Tenglish |
| `regional_legit_utility_bill_confirmation.wav` | English / Multilingual | `LEGITIMATE` | Standard utility receipt confirmation |
| `regional_ambiguous_loan_inquiry.wav` | English / Multilingual | `AMBIGUOUS` | Preliminary non-coercive personal loan inquiry |

---

## 4. How to Test via cURL

```bash
# Step 1: Upload audio
AUDIO_ID=$(curl -X POST "http://127.0.0.1:8000/api/v1/audio/upload" \
  -F "file=@sample_audios/01_scam_digital_arrest_cbi.wav" | jq -r .audio_id)

# Step 2: Transcribe via Gnani Prisma v3 STT
curl -X POST "http://127.0.0.1:8000/api/v1/transcription/${AUDIO_ID}"
```
