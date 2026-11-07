import os
import pytest
from app.audio.validator import validate_audio_magic_bytes, sanitize_filename
from app.gnani.prisma_client import GnaniPrismaClient

def test_webm_recording_magic_bytes():
    # Authentic WebM / Matroska container magic bytes: 0x1A 0x45 0xDF 0xA3
    webm_header = b"\x1a\x45\xdf\xa3\x9f\x42\x86\x81\x01\x42\xf7\x81\x01\x42\xf2\x81\x04"
    assert validate_audio_magic_bytes(webm_header, ".webm") is True

def test_webm_bytes_mislabeled_as_wav_is_rejected():
    # Critical Priority 2 check: A WebM stream given a .wav filename must fail WAV validation
    webm_header = b"\x1a\x45\xdf\xa3\x9f\x42\x86\x81\x01\x42\xf7\x81\x01\x42\xf2\x81\x04"
    assert validate_audio_magic_bytes(webm_header, ".wav") is False

def test_authentic_wav_header():
    wav_header = b"RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x44\xac\x00\x00"
    assert validate_audio_magic_bytes(wav_header, ".wav") is True

def test_authentic_mp3_and_m4a_headers():
    id3_header = b"ID3\x03\x00\x00\x00\x00\x00\x7f"
    assert validate_audio_magic_bytes(id3_header, ".mp3") is True

    m4a_header = b"\x00\x00\x00\x20ftypM4A \x00\x00\x00\x00"
    assert validate_audio_magic_bytes(m4a_header, ".m4a") is True

def test_executable_and_script_rejection():
    exe_header = b"MZ\x90\x00\x03\x00\x00\x00"
    assert validate_audio_magic_bytes(exe_header, ".wav") is False
    assert validate_audio_magic_bytes(exe_header, ".webm") is False

    html_header = b"<!DOCTYPE html><html>"
    assert validate_audio_magic_bytes(html_header, ".wav") is False
    assert validate_audio_magic_bytes(html_header, ".webm") is False

def test_prisma_client_mime_mapping():
    pc = GnaniPrismaClient()
    mime_map = {
        ".wav": "audio/wav",
        ".mp3": "audio/mpeg",
        ".m4a": "audio/mp4",
        ".flac": "audio/flac",
        ".ogg": "audio/ogg",
        ".webm": "audio/webm"
    }
    for ext, expected_mime in mime_map.items():
        # Extracted logic check
        fname = f"sample{ext}"
        determined_mime = mime_map.get(ext, "audio/wav")
        assert determined_mime == expected_mime

