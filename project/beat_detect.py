import librosa
import json
import numpy as np

# Load audio
y, sr = librosa.load('/workspace/assets/bgm.wav', sr=44100, mono=True)
duration = len(y) / sr

# Tempo and beat detection
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
beat_times = librosa.frames_to_time(beat_frames, sr=sr)

# Onset detection (stronger hits / accents)
onset_env = librosa.onset.onset_strength(y=y, sr=sr)
onset_frames = librosa.onset.onset_detect(y=y, sr=sr, onset_envelope=onset_env)
onset_times = librosa.frames_to_time(onset_frames, sr=sr)
onset_strengths = onset_env[onset_frames]

# Get top onsets by strength (strongest beats for cut points)
top_indices = np.argsort(onset_strengths)[::-1][:60]  # top 60 strongest
top_indices = sorted(top_indices)  # sort by time
top_onsets = [(float(onset_times[i]), float(onset_strengths[i])) for i in top_indices]

# Also detect "clicks" - short percussive onsets for tighter beat sync
click_frames = librosa.onset.onset_detect(y=y, sr=sr, onset_envelope=onset_env,
                                            units='frames', backtrack=True)
click_times = librosa.frames_to_time(click_frames, sr=sr)

bpm_val = float(tempo[0]) if hasattr(tempo, '__len__') else float(tempo)
result = {
    "bpm": bpm_val,
    "duration": float(duration),
    "total_beats": len(beat_times),
    "beat_times": [round(float(t), 3) for t in beat_times],
    "onset_count": len(onset_times),
    "top_onsets": [{"time": round(t, 3), "strength": round(s, 3)} for t, s in top_onsets],
    "click_times": [round(float(t), 3) for t in click_times[:80]],
}

with open('/workspace/project/evidence/beats.json', 'w') as f:
    json.dump(result, f, indent=2)

print(f"BPM: {bpm_val:.1f}")
print(f"Duration: {duration:.1f}s")
print(f"Total beats: {len(beat_times)}")
print(f"Onset count: {len(onset_times)}")
print(f"Top onsets (strongest): {len(top_onsets)}")
print(f"Beat times (first 30): {[round(t,2) for t in beat_times[:30]]}")
print(f"\nSaved to evidence/beats.json")
