import os
import json
import math
import struct
import wave
import random

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data"))
AUDIO_DIR = os.path.join(DATA_DIR, "synthetic_audio")
TRANSCRIPT_DIR = os.path.join(DATA_DIR, "transcripts")
LABELS_FILE = os.path.join(DATA_DIR, "labels", "scenarios.json")

os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)

def generate_synthetic_audio(scenario_id: str, noise_condition: str, duration_sec: float = 6.0):
    filename = f"{scenario_id.lower()}_{noise_condition}.wav"
    filepath = os.path.join(AUDIO_DIR, filename)
    
    sample_rate = 16000
    num_samples = int(duration_sec * sample_rate)
    
    # Base carrier frequency for speech-like harmonic modulation
    base_freq = 220.0
    
    with wave.open(filepath, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2) # 16-bit
        wf.setframerate(sample_rate)
        
        for i in range(num_samples):
            t = float(i) / sample_rate
            # Synthetic speech rhythm modulation
            speech_mod = 0.5 * (1.0 + math.sin(2.0 * math.pi * 3.5 * t))
            carrier = math.sin(2.0 * math.pi * base_freq * t) + 0.3 * math.sin(2.0 * math.pi * (base_freq * 2) * t)
            signal = carrier * speech_mod * 0.4
            
            # Noise conditions
            if noise_condition == "clean":
                noise = random.gauss(0, 0.005)
            elif noise_condition == "low_noise":
                noise = random.gauss(0, 0.02)
            elif noise_condition == "moderate_noise":
                noise = random.gauss(0, 0.06)
            elif noise_condition == "telephone-band":
                # Simulated telephone bandpass harmonic
                noise = 0.08 * math.sin(2.0 * math.pi * 50.0 * t) + random.gauss(0, 0.03)
            else:
                noise = 0.01
                
            sample_val = int(max(-32767, min(32767, (signal + noise) * 32767.0 * 0.6)))
            wf.writeframesraw(struct.pack('<h', sample_val))
            
    return filepath

def main():
    if not os.path.exists(LABELS_FILE):
        print(f"Error: {LABELS_FILE} not found!")
        return
        
    with open(LABELS_FILE, "r", encoding="utf-8") as f:
        scenarios = json.load(f)
        
    print(f"Generating synthetic audio and transcripts for {len(scenarios)} scenarios...")
    
    for item in scenarios:
        sid = item["scenario_id"]
        noise = item.get("noise_condition", "clean")
        audio_path = generate_synthetic_audio(sid, noise)
        
        # Save transcript
        transcript_file = os.path.join(TRANSCRIPT_DIR, f"{sid.lower()}.txt")
        with open(transcript_file, "w", encoding="utf-8") as tf:
            tf.write(item["script"])
            
        print(f"[OK] Created {sid} ({item['language']}) -> {os.path.basename(audio_path)}")
        
    print(f"\nSynthetic dataset generation complete! ({len(scenarios)} files generated in data/)")

if __name__ == "__main__":
    main()
