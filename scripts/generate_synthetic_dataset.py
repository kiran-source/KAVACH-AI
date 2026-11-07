import os
import json
import asyncio
import tempfile
import numpy as np
import soundfile as sf
import scipy.signal as signal
import edge_tts

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data"))
AUDIO_DIR = os.path.join(DATA_DIR, "synthetic_audio")
TRANSCRIPT_DIR = os.path.join(DATA_DIR, "transcripts")
LABELS_FILE = os.path.join(DATA_DIR, "labels", "scenarios.json")

os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)

VOICE_MAP = {
    "hi": "hi-IN-SwaraNeural",
    "te": "te-IN-MohanNeural",
    "en": "en-IN-NeerjaNeural"
}

FALLBACK_VOICE = "en-IN-NeerjaNeural"
TARGET_SAMPLE_RATE = 16000

def apply_acoustic_condition(audio_data: np.ndarray, sample_rate: int, condition: str) -> np.ndarray:
    """
    Applies realistic acoustic modeling to synthesized speech:
    - clean: baseline audio
    - low_noise: mild room ambiance
    - moderate_noise: street/cafeteria ambiance
    - telephone-band: 300-3400 Hz 4th-order bandpass filter mimicking cellular/PSTN voice codecs
    """
    if len(audio_data.shape) > 1:
        audio_data = np.mean(audio_data, axis=1)
        
    audio = audio_data.astype(np.float32)
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val

    if condition == "clean":
        return audio
        
    elif condition == "low_noise":
        noise = np.random.normal(0, 0.015, size=len(audio))
        audio_noisy = audio + noise
        return audio_noisy / np.max(np.abs(audio_noisy))
        
    elif condition == "moderate_noise":
        noise = np.random.normal(0, 0.045, size=len(audio))
        audio_noisy = audio + noise
        return audio_noisy / np.max(np.abs(audio_noisy))
        
    elif condition == "telephone-band":
        # 300 Hz to 3400 Hz Butterworth bandpass
        nyquist = 0.5 * sample_rate
        low = 300.0 / nyquist
        high = 3400.0 / nyquist
        b, a = signal.butter(4, [low, high], btype='band')
        filtered = signal.filtfilt(b, a, audio)
        
        # Add slight line hum (50 Hz and white noise)
        t = np.arange(len(filtered)) / sample_rate
        hum = 0.02 * np.sin(2 * np.pi * 50.0 * t)
        line_noise = np.random.normal(0, 0.025, size=len(filtered))
        tel_audio = filtered + hum + line_noise
        return tel_audio / np.max(np.abs(tel_audio))
        
    return audio

async def generate_speech_audio(script: str, language: str, output_path: str, condition: str):
    """
    Generates genuine neural spoken audio using official regional neural voices,
    resamples to 16kHz mono, and applies authentic acoustic filters.
    """
    voice = VOICE_MAP.get(language, FALLBACK_VOICE)
    
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        tmp_mp3 = tmp.name
        
    try:
        communicate = edge_tts.Communicate(script, voice)
        await communicate.save(tmp_mp3)
        
        # Read back synthesized audio
        data, sr = sf.read(tmp_mp3)
        if len(data.shape) > 1:
            data = np.mean(data, axis=1)
            
        # Resample to 16,000 Hz if needed
        if sr != TARGET_SAMPLE_RATE:
            num_target_samples = int(len(data) * TARGET_SAMPLE_RATE / sr)
            data = signal.resample(data, num_target_samples)
            sr = TARGET_SAMPLE_RATE
            
        # Apply acoustic noise/filter condition
        processed_data = apply_acoustic_condition(data, sr, condition)
        
        # Save as 16-bit PCM WAV
        sf.write(output_path, processed_data, sr, subtype='PCM_16')
        
    finally:
        if os.path.exists(tmp_mp3):
            try:
                os.remove(tmp_mp3)
            except OSError:
                pass

async def main_async():
    if not os.path.exists(LABELS_FILE):
        print(f"Error: {LABELS_FILE} not found!")
        return
        
    with open(LABELS_FILE, "r", encoding="utf-8") as f:
        scenarios = json.load(f)
        
    print(f"Generating genuine neural spoken audio for {len(scenarios)} scenarios...")
    
    provenance = {
        "dataset_name": "KAVACH-AI Synthetic Speech Evaluation Benchmark",
        "voice_engine": "Microsoft Neural TTS (hi-IN-SwaraNeural, te-IN-MohanNeural, en-IN-NeerjaNeural)",
        "sample_rate_hz": TARGET_SAMPLE_RATE,
        "format": "16-bit PCM mono WAV",
        "languages": ["hi", "te", "en"],
        "scenarios_count": len(scenarios),
        "acoustic_conditions": ["clean", "low_noise", "moderate_noise", "telephone-band"],
        "items": []
    }
    
    for idx, item in enumerate(scenarios, start=1):
        sid = item["scenario_id"]
        lang = item.get("language", "en")
        noise = item.get("noise_condition", "clean")
        script = item["script"]
        
        filename = f"{sid.lower()}_{noise}.wav"
        audio_path = os.path.join(AUDIO_DIR, filename)
        
        print(f"[{idx}/{len(scenarios)}] Generating {sid} ({lang}, {noise}) with {VOICE_MAP.get(lang, FALLBACK_VOICE)}...")
        await generate_speech_audio(script, lang, audio_path, noise)
        
        # Save exact transcript
        transcript_file = os.path.join(TRANSCRIPT_DIR, f"{sid.lower()}.txt")
        with open(transcript_file, "w", encoding="utf-8") as tf:
            tf.write(script)
            
        provenance["items"].append({
            "scenario_id": sid,
            "filename": filename,
            "language": lang,
            "voice": VOICE_MAP.get(lang, FALLBACK_VOICE),
            "condition": noise,
            "duration_samples": len(sf.read(audio_path)[0]),
            "expected_classification": item.get("expected_classification", "scam")
        })
        
    provenance_path = os.path.join(DATA_DIR, "DATASET_PROVENANCE.json")
    with open(provenance_path, "w", encoding="utf-8") as pf:
        json.dump(provenance, pf, indent=2)
        
    print(f"\n[SUCCESS] All {len(scenarios)} spoken speech samples generated!")
    print(f"Provenance saved to: {provenance_path}")

def main():
    asyncio.run(main_async())

if __name__ == "__main__":
    main()
