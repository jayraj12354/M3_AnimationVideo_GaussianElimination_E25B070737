"""
generate_music.py – Synthesizes a soft, royalty-free ambient pad track
for background music beneath voice-over narration.
"""

import wave
import numpy as np


def generate_ambient_pad(output_wav: str, duration_sec: float = 250.0, sr: int = 44100):
    """Synthesize a soft, royalty-free ambient chord pad WAV file."""
    if duration_sec <= 0 or sr <= 0:
        raise ValueError("duration_sec and sr must be positive")

    n_samples = int(round(sr * duration_sec))
    t = np.linspace(0, duration_sec, n_samples, endpoint=False)

    # Warm, calm chord progression: Cmaj7 -> Am7 -> Fmaj7 -> G6 (8 sec per chord)
    chords = [
        [130.81, 196.00, 246.94, 329.63],  # Cmaj7
        [110.00, 196.00, 261.63, 329.63],  # Am7
        [87.31,  174.61, 220.00, 329.63],  # Fmaj7
        [98.00,  196.00, 246.94, 329.63],  # G6
    ]
    chord_len = 8.0
    fade_edge = 1.5

    audio = np.zeros_like(t)
    num_chords = int(np.ceil(duration_sec / chord_len))

    for i in range(num_chords):
        start_s = i * chord_len
        end_s = min((i + 1) * chord_len, duration_sec)
        idx0 = int(start_s * sr)
        idx1 = min(int(end_s * sr), n_samples)
        seg_t = t[idx0:idx1] - start_s
        n_seg = len(seg_t)
        if n_seg == 0:
            continue

        freqs = chords[i % len(chords)]
        seg = np.zeros(n_seg)
        for f in freqs:
            # Soft fundamental + gentle warm octave/2nd harmonic
            seg += 0.75 * np.sin(2 * np.pi * f * seg_t)
            seg += 0.15 * np.sin(2 * np.pi * (2 * f) * seg_t)

        # Smooth crossfade envelope per chord
        env = np.ones(n_seg)
        f_samples = min(int(fade_edge * sr), n_seg // 2)
        if f_samples > 0:
            env[:f_samples] = np.linspace(0.0, 1.0, f_samples)
            env[-f_samples:] = np.linspace(1.0, 0.0, f_samples)

        audio[idx0:idx1] += seg * env

    # Global fade-in (3s) and fade-out (4s), clamped for short durations
    fade_in = min(int(3.0 * sr), n_samples // 2)
    fade_out = min(int(4.0 * sr), n_samples // 2)
    if fade_in > 0:
        audio[:fade_in] *= np.linspace(0.0, 1.0, fade_in)
    if fade_out > 0:
        audio[-fade_out:] *= np.linspace(1.0, 0.0, fade_out)

    # Normalize to soft background level (-24 dBFS peak ~ 0.063)
    peak = np.max(np.abs(audio))
    if peak > 0:
        audio = audio / peak * 0.065

    pcm = np.int16(np.clip(audio, -1.0, 1.0) * 32767)
    with wave.open(output_wav, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(pcm.tobytes())


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/soft_ambient.wav"
    dur = float(sys.argv[2]) if len(sys.argv) > 2 else 250.0
    generate_ambient_pad(out, dur)
    print(f"Generated soft ambient track: {out} ({dur:.1f}s)")
