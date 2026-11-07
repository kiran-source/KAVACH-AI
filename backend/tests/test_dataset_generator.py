import os
import sys
import json
import pytest
from pathlib import Path

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.dataset_generator import (
    StorageMonitor,
    ApiUsageLedger,
    DatasetValidator,
    GnaniTimbreAdapter,
    GnaniPrismaAdapter,
    GnaniEvonAdapter,
    StorageExceededException
)

def test_storage_monitor():
    free_mb = StorageMonitor.get_free_disk_space_mb()
    assert free_mb > 0
    # Should not raise exception on standard system with >= 500 MB free
    StorageMonitor.check_storage_safety()

def test_api_usage_ledger(tmp_path):
    ledger_file = tmp_path / "test_ledger.json"
    ledger = ApiUsageLedger(ledger_path=ledger_file)
    assert ledger.data["total_requests"] == 0

    ledger.record_call(
        model="timbre-v2.5-test",
        call_type="tts",
        success=True,
        duration_sec=3.5,
        status_code=200,
        details="Unit test call"
    )

    assert ledger.data["total_requests"] == 1
    assert ledger.data["successful_requests"] == 1
    assert ledger.data["total_audio_seconds"] == 3.5
    assert ledger_file.exists()

def test_dataset_validator_turn_and_pii_checks():
    valid_convo = {
        "conversation_id": "KAV-SYNTH-001",
        "language": "hi-en",
        "primary_label": "SCAM",
        "scenario": "Electricity Disconnection Threat",
        "dialogue": [
            {"speaker": "caller", "text": "Sir, electricity bill unpaid hai. Aaj raat power cut ho jayega."},
            {"speaker": "recipient", "text": "Maine to bill pay kar diya tha online."},
            {"speaker": "caller", "text": "Server update nahi hua hai sir. QuickSupport app download kijiye."},
            {"speaker": "recipient", "text": "Konsa app? PlayStore pe milega kya?"},
            {"speaker": "caller", "text": "Hum link bhej rahe hain WhatsApp par, turant install karke 10 rupaye pay karein."},
            {"speaker": "recipient", "text": "Nahi, main bijli office jaake check karunga."}
        ],
        "scam_tactics": ["URGENCY_OR_THREAT", "REMOTE_ACCESS_MANIPULATION", "MALICIOUS_LINK_OR_APP"],
        "risk_indicators": ["power cut threat", "apk installation link", "urgency"],
        "explanation": "Threatens immediate disconnection to force remote APK installation.",
        "synthetic_source": "KAVACH-AI Pilot Scenario",
        "generation_model": "pilot-curated",
        "review_status": "pending_review"
    }

    errors = DatasetValidator.validate_conversation(valid_convo)
    assert len(errors) == 0

    # Invalidate by adding real PII card number
    invalid_convo = dict(valid_convo)
    invalid_convo["dialogue"] = list(valid_convo["dialogue"]) + [
        {"speaker": "caller", "text": "Tell me your card number 4532 0123 4567 8901 right now."}
    ]
    errs = DatasetValidator.validate_conversation(invalid_convo)
    assert any("card number" in e for e in errs)

def test_timbre_adapter_mock_synthesis(tmp_path):
    output_wav = tmp_path / "test_synth.wav"
    adapter = GnaniTimbreAdapter(mock_mode=True)
    success, duration, msg = adapter.synthesize_dialogue(
        text="Hello, this is a test.",
        language="en",
        output_path=output_wav
    )
    assert success is True
    assert duration > 0.0
    assert output_wav.exists()
    assert output_wav.stat().st_size > 44 # Valid RIFF WAV header size

def test_prisma_adapter_mock_validation(tmp_path):
    test_audio = tmp_path / "dummy.wav"
    test_audio.write_bytes(b"RIFF....WAVEfmt ....data....")
    adapter = GnaniPrismaAdapter(mock_mode=True)
    success, transcript, msg = adapter.validate_audio(test_audio, "en")
    assert success is True
    assert "Mock" in transcript

def test_run_pilot_stage2_mock(tmp_path, monkeypatch):
    from scripts import dataset_generator
    monkeypatch.setattr(dataset_generator, "DATASET_ROOT", tmp_path)
    monkeypatch.setattr(dataset_generator, "METADATA_DIR", tmp_path / "metadata")
    monkeypatch.setattr(dataset_generator, "TRANSCRIPTS_DIR", tmp_path / "transcripts")
    monkeypatch.setattr(dataset_generator, "AUDIO_DIR", tmp_path / "audio")
    monkeypatch.setattr(dataset_generator, "REPORTS_DIR", tmp_path / "reports")

    report = dataset_generator.run_pilot_stage2(live_gnani=False)
    assert report["stage"] == "STAGE_2_PILOT"
    assert report["pilot_samples_count"] == 5
    assert report["dataset_validation"]["is_valid"] is True
    assert len(report["audio_synthesis"]) == 5
    assert len(report["stt_validation"]) == 5

def test_stage3_bulk_generation_mock(tmp_path, monkeypatch):
    from scripts import execute_stage3_bulk_generation, dataset_generator
    monkeypatch.setattr(dataset_generator, "METADATA_DIR", tmp_path / "metadata")
    monkeypatch.setattr(execute_stage3_bulk_generation, "DATASET_ROOT", tmp_path)
    monkeypatch.setattr(execute_stage3_bulk_generation, "METADATA_DIR", tmp_path / "metadata")
    monkeypatch.setattr(execute_stage3_bulk_generation, "TRANSCRIPTS_DIR", tmp_path / "transcripts")
    monkeypatch.setattr(execute_stage3_bulk_generation, "AUDIO_DIR", tmp_path / "audio")
    monkeypatch.setattr(execute_stage3_bulk_generation, "SPLITS_DIR", tmp_path / "splits")
    monkeypatch.setattr(execute_stage3_bulk_generation, "REPORTS_DIR", tmp_path / "reports")

    manifest = execute_stage3_bulk_generation.run_stage3_bulk_generation(live_timbre=False)
    assert manifest["total_conversations"] == 100
    assert manifest["total_audio_samples"] == 20
    assert manifest["class_distribution"]["SCAM"] == 40
    assert manifest["class_distribution"]["LEGITIMATE"] == 35
    assert manifest["class_distribution"]["AMBIGUOUS"] == 25
    assert manifest["splits"]["train"] == 70
    assert manifest["splits"]["validation"] == 15
    assert manifest["splits"]["test"] == 15



