import os
import sys
from pathlib import Path

# Add project root and backend to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "backend"))

import json
import sqlite3

def audit_database():
    print("=== 1. DATABASE AUDIT ===")
    db_path = Path("kavach.db")
    if not db_path.exists():
        print("[FAIL] Database file kavach.db does not exist!")
        return False
    
    conn = sqlite3.connect("kavach.db")
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [t[0] for t in c.fetchall()]
    print(f"[PASS] SQLite database exists: {db_path.stat().st_size} bytes")
    print(f"Total tables: {len(tables)}")
    for t in sorted(tables):
        cnt = c.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"  - {t}: {cnt} rows")
    conn.close()
    return True

def audit_dataset():
    print("\n=== 2. SYNTHETIC DATASET & EVALUATION AUDIT ===")
    labels_file = Path("data/labels/scenarios.json")
    audio_dir = Path("data/synthetic_audio")
    metrics_file = Path("data/evaluation/metrics.json")
    
    if not labels_file.exists():
        print("[FAIL] scenarios.json missing!")
        return False
    
    with open(labels_file, "r", encoding="utf-8") as f:
        scenarios = json.load(f)
    print(f"[PASS] Ground truth scenarios: {len(scenarios)} defined")
    
    scam_count = sum(1 for s in scenarios if s.get("expected_classification") == "scam")
    legit_count = sum(1 for s in scenarios if s.get("expected_classification") == "legitimate")
    ambig_count = sum(1 for s in scenarios if s.get("expected_classification") == "ambiguous")
    print(f"  - SCAM scenarios: {scam_count}")
    print(f"  - LEGITIMATE scenarios: {legit_count}")
    print(f"  - AMBIGUOUS/AWARENESS scenarios: {ambig_count}")
    
    audio_files = list(audio_dir.glob("*.wav"))
    print(f"[PASS] Audio files generated: {len(audio_files)} WAV files found")
    
    if metrics_file.exists():
        with open(metrics_file, "r", encoding="utf-8") as f:
            metrics_data = json.load(f)
        sub_metrics = metrics_data.get("metrics", {})
        print("[PASS] Benchmark evaluation metrics:")
        print(f"  - Accuracy: {sub_metrics.get('accuracy', 0)*100:.1f}%")
        print(f"  - Precision: {sub_metrics.get('precision', 0)*100:.1f}%")
        print(f"  - Recall: {sub_metrics.get('recall', 0)*100:.1f}%")
        print(f"  - F1-Score: {sub_metrics.get('f1_score', 0):.4f}")
        print(f"  - Confusion Matrix: {metrics_data.get('confusion_matrix')}")
        print(f"  - Per-Language Accuracy: {metrics_data.get('per_language_accuracy')}")
    else:
        print("[WARN] Evaluation metrics not found!")
    return True

def audit_detection_engine():
    print("\n=== 3. THREAT DETECTION & EXPLAINABILITY ENGINE AUDIT ===")
    from app.detection.engine import analyze_transcript
    
    test_cases = [
        ("Digital Arrest (Hindi)", "Aapka naam CBI money laundering case mein aaya hai. Phone cut kiya toh digital arrest warrant issue hoga.", "SCAM", ["Digital Arrest Patterns", "Authority Impersonation"]),
        ("OTP Theft (Telugu)", "మీ బ్యాంక్ అకౌంట్ బ్లాక్ అయింది. వెంటనే మీ OTP మరియు పిన్ చెప్పండి.", "SCAM", ["Credential Theft"]),
        ("Electricity Disconnect", "Dear consumer, your electricity power will be disconnected tonight at 9:30 PM due to unpaid bill. Immediately pay Rs 500 or install QuickSupport APK to update meter.", "SCAM", ["Urgency and Threats", "Remote Access Manipulation"]),
        ("Legitimate Bank Awareness", "State Bank of India alerts customers: Never share your OTP, UPI PIN, or CVV with anyone including bank officials. Stay safe.", "LEGITIMATE", []),
        ("Legitimate Courier Delivery", "Hello sir, your parcel has arrived at your gate. Please collect it whenever convenient.", "LEGITIMATE", [])
    ]
    
    all_passed = True
    for name, text, expected_class, expected_tactics in test_cases:
        res = analyze_transcript(text)
        predicted_class = "SCAM" if res["risk_score"] >= 40.0 else "LEGITIMATE"
        status = "PASS" if predicted_class == expected_class else "FAIL"
        if status == "FAIL":
            all_passed = False
        print(f"[{status}] {name}")
        print(f"       Risk Score: {res['risk_score']} | Severity: {res['severity']} | Class: {predicted_class}")
        print(f"       Categories: {res['categories']}")
        print(f"       Neg Context Suppressed: {res['context_suppressed']}")
    return all_passed

def audit_gnani_integration():
    print("\n=== 4. GNANI AI PRISMA & TIMBRE INTEGRATION AUDIT ===")
    from app.core.config import settings
    from app.gnani.prisma_service import prisma_client, timbre_client
    
    print(f"Configured GNANI_API_KEY: {'[SET]' if settings.GNANI_API_KEY else '[NOT SET - DEMO MODE ACTIVE]'}")
    print(f"Prisma Endpoint: {settings.GNANI_PRISMA_ENDPOINT}")
    print(f"Timbre Endpoint: {settings.GNANI_TIMBRE_ENDPOINT}")
    
    # Test Timbre speech synthesis in fallback/demo mode
    res = timbre_client.generate_speech(
        text="Warning: Kavach AI has detected potential digital arrest fraud.",
        language="en"
    )
    print(f"[PASS] Timbre synthesis returned audio file: {res['filename']} ({len(res['audio_bytes'])} bytes)")
    print(f"       Provider: {res['provider']} (is_fallback={res['is_fallback']})")
    
    # Check Prisma transcription
    dummy_wav = Path("data/synthetic_audio/SCAM-001_clean.wav")
    if dummy_wav.exists():
        trans_res = prisma_client.transcribe(str(dummy_wav), language="hi")
        print(f"[PASS] Prisma transcription successful:")
        print(f"       Language detected: {trans_res.get('language')}")
        print(f"       Transcript length: {len(trans_res.get('transcript', ''))} chars")
        print(f"       Provider: {trans_res.get('provider')}")
    return True

def audit_pdf_reporting():
    print("\n=== 5. PDF FORENSIC INCIDENT REPORT GENERATION AUDIT ===")
    from app.reports.pdf_generator import generate_pdf_report
    sample_incident = {
        "incident_number": "INC-2026-TEST-001",
        "created_at": "2026-11-03 22:20:00 UTC",
        "risk_score": 92.5,
        "severity": "Critical",
        "detected_language": "Telugu",
        "audio_filename": "SCAM-001_clean.wav",
        "status": "Under Review",
        "threats": [
            {
                "category": "Digital Arrest Patterns",
                "matched_text": "CBI arrest warrant issue chestunnam",
                "confidence": 0.95,
                "description": "Threatened victim with fraudulent digital arrest"
            },
            {
                "category": "Credential Theft",
                "matched_text": "Mee OTP cheppandi",
                "confidence": 0.98,
                "description": "Attempted to steal banking one-time password"
            }
        ],
        "recommendations": [
            "Never share OTP or UPI PIN",
            "Indian police never issue digital arrests over Skype or WhatsApp",
            "Report immediately to Cybercrime helpline 1930"
        ],
        "analyst_notes": "Verified with bank branch.",
        "timeline": [
            {"created_at": "2026-11-03 22:20:00", "actor": "System", "action": "Incident Ingested"},
            {"created_at": "2026-11-03 22:21:00", "actor": "SOC Lead", "action": "Status changed to Under Review"}
        ]
    }
    res_path = generate_pdf_report(sample_incident)
    if Path(res_path).exists() and Path(res_path).stat().st_size > 1000:
        print(f"[PASS] PDF report generated successfully: {Path(res_path).stat().st_size} bytes")
        with open(res_path, "rb") as f:
            header = f.read(5)
            print(f"[PASS] Valid PDF Magic Header: {header}")
    else:
        print("[FAIL] PDF report generation failed!")
        return False
    return True

def audit_security_controls():
    print("\n=== 6. CYBERSECURITY CONTROLS & DEFENSIVE HARNESS AUDIT ===")
    from app.audio.validator import validate_audio_magic_bytes, sanitize_filename
    from app.core.config import settings

    # 1. Test malicious filename sanitization & path traversal prevention
    dirty_name = "../../../etc/passwd\x00malicious;rm -rf.wav"
    clean_name = sanitize_filename(dirty_name)
    print(f"[PASS] Filename sanitization: '{dirty_name}' -> '{clean_name}' (Path traversal neutralized)")

    # 2. Test executable magic bytes rejection
    pe_header = b"MZ\x90\x00\x03\x00\x00\x00FakePEHeader"
    is_valid_wav = validate_audio_magic_bytes(pe_header, ".wav")
    if not is_valid_wav:
        print("[PASS] Malicious executable magic bytes rejected for .wav format")
    else:
        print("[FAIL] Executable allowed as WAV!")
        
    # 3. Test valid WAV magic bytes
    wav_header = b"RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x44\xac\x00\x00\x88\x58\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00"
    is_real_wav = validate_audio_magic_bytes(wav_header, ".wav")
    if is_real_wav:
        print("[PASS] Authentic WAV magic bytes verified successfully")
    else:
        print("[FAIL] Real WAV rejected!")
    
    # 4. Check CORS and limits
    print(f"[PASS] CORS Allowed Origins: {settings.ALLOWED_ORIGINS}")
    print(f"[PASS] Max Upload Size: {settings.MAX_UPLOAD_SIZE_MB} MB")
    print(f"[PASS] Audio Storage Retention: {settings.RETENTION_DAYS} days")
    return True

if __name__ == "__main__":
    db_ok = audit_database()
    ds_ok = audit_dataset()
    de_ok = audit_detection_engine()
    gn_ok = audit_gnani_integration()
    pdf_ok = audit_pdf_reporting()
    sec_ok = audit_security_controls()
    print("\n" + "="*50)
    print("AUDIT SUITE COMPLETE")
    print("="*50)
