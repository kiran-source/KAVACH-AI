"""
KAVACH AI — Sample Audio Generator & Catalog Builder
Generates realistic, crystal-clear spoken WAV audio files for testing KAVACH AI
across Scam, Legitimate, and Ambiguous scenarios. Also organizes multilingual samples.
"""

import os
import shutil
import win32com.client
import soundfile as sf

def main():
    out_dir = os.path.abspath("sample_audios")
    os.makedirs(out_dir, exist_ok=True)
    multilingual_dir = os.path.join(out_dir, "multilingual")
    os.makedirs(multilingual_dir, exist_ok=True)

    samples = [
        {
            "filename": "01_scam_digital_arrest_cbi.wav",
            "title": "CBI Digital Arrest Extortion",
            "category": "SCAM",
            "expected_risk": "Critical (95-100)",
            "threat_type": "Authority Impersonation & Digital Arrest",
            "text": (
                "Namaste. I am Inspector Sharma calling from Central Bureau of Investigation "
                "CBI headquarters New Delhi. A courier parcel containing fake passports and "
                "contraband narcotics was seized in Mumbai registered under your Aadhaar number. "
                "Supreme Court has issued an immediate non-bailable warrant. You are placed under "
                "Digital Arrest right now. Do not disconnect this video call or inform your family, "
                "otherwise a police team will arrest you within one hour."
            )
        },
        {
            "filename": "02_scam_bank_kyc_otp_fraud.wav",
            "title": "Bank KYC Suspension & OTP Theft",
            "category": "SCAM",
            "expected_risk": "Critical (90-98)",
            "threat_type": "Credential Harvesting (OTP & UPI PIN)",
            "text": (
                "Good morning sir, this is Rajesh calling from State Bank of India KYC verification desk. "
                "Your net banking access and debit card are suspended due to pending biometric KYC update. "
                "To unfreeze your account immediately, share the six digit OTP received on your mobile "
                "and confirm your UPI PIN right now."
            )
        },
        {
            "filename": "03_scam_anydesk_electricity_threat.wav",
            "title": "Electricity Cutoff & AnyDesk Remote Access",
            "category": "SCAM",
            "expected_risk": "Critical (90-95)",
            "threat_type": "Remote Access APK Sideloading",
            "text": (
                "Dear consumer, your electricity meter bill payment has failed and power supply will be "
                "disconnected tonight at eight pm. Open Google Play Store immediately and install AnyDesk "
                "QuickSupport application. Share the nine digit code with our support agent to update "
                "your payment status."
            )
        },
        {
            "filename": "04_scam_customs_contraband_courier.wav",
            "title": "Customs Contraband Narcotics Extortion",
            "category": "SCAM",
            "expected_risk": "Critical (92-96)",
            "threat_type": "Customs Contraband & Financial Redirection",
            "text": (
                "This is Customs and Border Protection officer at Mumbai International Airport. "
                "A DHL courier consigned to your name containing fifty grams of illegal narcotics "
                "has been intercepted. Transfer ninety thousand rupees to the RBI safe verification "
                "account immediately to avoid criminal detention."
            )
        },
        {
            "filename": "05_legit_broadband_customer_support_safe.wav",
            "title": "Customer Support Ticket Resolution",
            "category": "LEGITIMATE",
            "expected_risk": "Safe / Low (5-15)",
            "threat_type": "None (Routine Business)",
            "text": (
                "Hello, thank you for reaching out to customer care regarding your fiber broadband speed issue. "
                "Our technician has resolved the fiber line attenuation at your local node, and ticket number "
                "4819 is now closed. Please let us know if your internet connection is working smoothly. "
                "Have a pleasant day."
            )
        },
        {
            "filename": "06_legit_bank_security_awareness_advisory.wav",
            "title": "Bank Security Awareness Advisory",
            "category": "LEGITIMATE",
            "expected_risk": "Safe / Zero (0-10)",
            "threat_type": "None (Educational Precedence Guard)",
            "text": (
                "Dear customer, this is an official security awareness announcement from your bank. "
                "Please remember that bank officials and police never ask for your confidential OTP, "
                "UPI PIN, or passwords over the phone. Stay safe from scam calls and beware of fake "
                "digital arrest threats. Report cyber fraud on helpline 1930."
            )
        },
        {
            "filename": "07_ambiguous_courier_delivery_verification.wav",
            "title": "Courier Chequebook Delivery Inquiry",
            "category": "AMBIGUOUS",
            "expected_risk": "Moderate (30-50)",
            "threat_type": "Borderline / Escalates to MuRIL",
            "text": (
                "Hello, am I speaking with the account holder? This is DTDC courier dispatch team "
                "regarding a speed post parcel from HDFC Bank containing your renewed checkbook. "
                "Nobody was available at your registered address this afternoon. Could you please "
                "confirm if you will be available tomorrow between ten am and two pm for delivery?"
            )
        }
    ]

    print("[*] Initializing SAPI Speech Synthesizer...")
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    stream = win32com.client.Dispatch("SAPI.SpFileStream")
    speaker.Rate = -1  # Measured rate for optimal acoustic clarity and STT fidelity

    generated_list = []
    for s in samples:
        filepath = os.path.join(out_dir, s["filename"])
        stream.Open(filepath, 3)  # SSFMCreateForWrite = 3
        speaker.AudioOutputStream = stream
        speaker.Speak(s["text"])
        stream.Close()

        info = sf.info(filepath)
        s["duration"] = round(info.duration, 2)
        s["size_kb"] = round(os.path.getsize(filepath) / 1024, 1)
        generated_list.append(s)
        print(f"  [+] Created: {s['filename']} ({s['duration']}s, {s['size_kb']} KB)")

    # Copy representative multilingual samples from existing synthetic dataset
    print("[*] Organizing Indian regional language samples...")
    regional_sources = [
        ("data/kavach_synthetic_v1/audio/hindi/kav-synth-pilot-002.wav", "hindi_cbi_digital_arrest_scam.wav", "Hindi Scam"),
        ("data/kavach_synthetic_v1/audio/telugu/kav-synth-pilot-003.wav", "telugu_bank_kyc_otp_scam.wav", "Telugu Scam"),
        ("data/kavach_synthetic_v1/audio/hindi_english/kav-synth-pilot-005.wav", "hinglish_customs_parcel_scam.wav", "Hinglish Code-Mixed Scam"),
        ("data/kavach_synthetic_v1/audio/telugu_english/kav-synth-pilot-004.wav", "tenglish_lottery_prize_scam.wav", "Tenglish Code-Mixed Scam"),
        ("data/synthetic_audio/legit-001_clean.wav", "regional_legit_utility_bill_confirmation.wav", "Utility Bill Confirmation (Legit)"),
        ("data/synthetic_audio/ambig-001_clean.wav", "regional_ambiguous_loan_inquiry.wav", "Loan Inquiry (Ambiguous)")
    ]

    for src, dst_name, desc in regional_sources:
        if os.path.exists(src):
            dst_path = os.path.join(multilingual_dir, dst_name)
            shutil.copyfile(src, dst_path)
            sz = round(os.path.getsize(dst_path) / 1024, 1)
            print(f"  [+] Regional: {dst_name} ({sz} KB) - {desc}")

    # Build comprehensive README.md in sample_audios directory
    readme_path = os.path.join(out_dir, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("# 🎧 KAVACH AI — Testing Audio Library\n\n")
        f.write("This directory contains pre-generated, validated audio test files (`.wav`) specifically calibrated for testing the **KAVACH AI** voice threat detection pipeline.\n\n")
        f.write("You can test these files either by:\n")
        f.write("1. **Frontend Web UI**: Drag and drop any `.wav` file into the upload zone at `/` or `/analysis`.\n")
        f.write("2. **FastAPI Swagger / cURL**: POST to `/api/v1/audio/upload` followed by `/api/v1/transcription/{audio_id}`.\n\n")
        f.write("---\n\n")
        f.write("## 1. Core Evaluation Audio Files\n\n")
        f.write("| File Name | Scenario | Expected Verdict | Expected Risk | Key Indicators Tested |\n")
        f.write("| :--- | :--- | :---: | :---: | :--- |\n")
        for s in generated_list:
            f.write(f"| `{s['filename']}` | **{s['title']}** | `{s['category']}` | **{s['expected_risk']}** | {s['threat_type']} |\n")
        f.write("\n---\n\n")
        f.write("## 2. Spoken Audio Transcripts\n\n")
        for s in generated_list:
            f.write(f"### 🔊 `{s['filename']}`\n")
            f.write(f"- **Verdict**: `{s['category']}` | **Risk**: {s['expected_risk']}\n")
            f.write(f"- **Duration**: {s['duration']}s | **Size**: {s['size_kb']} KB\n")
            f.write(f"- **Transcript**:\n> *\"{s['text']}\"*\n\n")
        f.write("---\n\n")
        f.write("## 3. Multilingual Regional Audio Files (`sample_audios/multilingual/`)\n\n")
        f.write("| File Name | Language / Dialect | Category | Description |\n")
        f.write("| :--- | :--- | :---: | :--- |\n")
        f.write("| `hindi_cbi_digital_arrest_scam.wav` | Hindi (`hi-IN`) | `SCAM` | Fake police officer extortion in colloquial Hindi |\n")
        f.write("| `telugu_bank_kyc_otp_scam.wav` | Telugu (`te-IN`) | `SCAM` | Bank KYC suspension threat in Telugu |\n")
        f.write("| `hinglish_customs_parcel_scam.wav` | Hindi-English Code-Mixed | `SCAM` | Narcotics courier extortion in Hinglish |\n")
        f.write("| `tenglish_lottery_prize_scam.wav` | Telugu-English Code-Mixed | `SCAM` | Telecom prize claim fee in Tenglish |\n")
        f.write("| `regional_legit_utility_bill_confirmation.wav` | English / Multilingual | `LEGITIMATE` | Standard utility receipt confirmation |\n")
        f.write("| `regional_ambiguous_loan_inquiry.wav` | English / Multilingual | `AMBIGUOUS` | Preliminary non-coercive personal loan inquiry |\n\n")
        f.write("---\n\n")
        f.write("## 4. How to Test via cURL\n\n")
        f.write("```bash\n")
        f.write("# Step 1: Upload audio\n")
        f.write('AUDIO_ID=$(curl -X POST "http://127.0.0.1:8000/api/v1/audio/upload" \\\n')
        f.write('  -F "file=@sample_audios/01_scam_digital_arrest_cbi.wav" | jq -r .audio_id)\n\n')
        f.write("# Step 2: Transcribe via Gnani Prisma v3 STT\n")
        f.write('curl -X POST "http://127.0.0.1:8000/api/v1/transcription/${AUDIO_ID}"\n')
        f.write("```\n")

    print(f"[✓] Successfully written documentation to {readme_path}")

if __name__ == "__main__":
    main()
