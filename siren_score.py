"""Chấm điểm độ giống 'Siren - Deelite, Wise Amechi' theo công thức đo được.
Dùng: python3 siren_score.py file1.mp3 file2.mp3 ...
"""
import sys, warnings
import numpy as np
import librosa

warnings.filterwarnings("ignore")

# Công thức đo từ file gốc
REF = dict(bpm=89.1, key="D major", hp=34.1, low=98.7, voiced=0.79, f0=333.5, onset=2.69)
NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
MAJ = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
MIN = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])


def measure(path, seconds=120):
    y, sr = librosa.load(path, duration=seconds)
    oenv = librosa.onset.onset_strength(y=y, sr=sr)
    bpm = float(np.atleast_1d(librosa.beat.beat_track(onset_envelope=oenv, sr=sr)[0])[0])
    # chuẩn hoá về khoảng 70-140 để tránh half/double-time
    while bpm < 70:
        bpm *= 2
    while bpm > 140:
        bpm /= 2
    prof = librosa.feature.chroma_cqt(y=y, sr=sr).mean(axis=1)
    cands = [(np.corrcoef(np.roll(MAJ, i), prof)[0, 1], NAMES[i] + " major") for i in range(12)]
    cands += [(np.corrcoef(np.roll(MIN, i), prof)[0, 1], NAMES[i] + " minor") for i in range(12)]
    key = max(cands)[1]
    H, P = librosa.effects.hpss(y)
    hp = float(np.sum(H ** 2) / (np.sum(P ** 2) + 1e-9))
    S = np.abs(librosa.stft(y)) ** 2
    fr = librosa.fft_frequencies(sr=sr)
    low = float(S[fr < 2000].sum() / S.sum() * 100)
    f0, _, _ = librosa.pyin(y, fmin=librosa.note_to_hz('C3'), fmax=librosa.note_to_hz('C6'), sr=sr)
    v = f0[~np.isnan(f0)]
    voiced = len(v) / len(f0)
    med = float(np.median(v)) if len(v) else 0.0
    onset = len(librosa.onset.onset_detect(onset_envelope=oenv, sr=sr)) / (len(y) / sr)
    return dict(bpm=bpm, key=key, hp=hp, low=low, voiced=voiced, f0=med, onset=onset)


def score(m):
    s = {}
    s["bpm"] = max(0, 1 - abs(m["bpm"] - REF["bpm"]) / 20) * 20
    s["key"] = 10 if m["key"] == REF["key"] else (5 if m["key"].split()[0] == "D" else 0)
    s["hp"] = min(m["hp"], REF["hp"]) / REF["hp"] * 20          # ít bộ gõ
    s["low"] = max(0, 1 - abs(m["low"] - REF["low"]) / 10) * 20  # tối/ấm
    s["voiced"] = max(0, 1 - abs(m["voiced"] - REF["voiced"]) / 0.4) * 15
    s["f0"] = max(0, 1 - abs(m["f0"] - REF["f0"]) / 200) * 10    # dải giọng nữ
    s["onset"] = max(0, 1 - abs(m["onset"] - REF["onset"]) / 3) * 5
    return sum(s.values()), s


if __name__ == "__main__":
    rows = []
    for p in sys.argv[1:]:
        try:
            m = measure(p)
            tot, _ = score(m)
            rows.append((tot, p, m))
        except Exception as e:
            print("LỖI", p, e)
    for tot, p, m in sorted(rows, reverse=True):
        print(f"{tot:5.1f}/100  {p.split('/')[-1]}\n        bpm={m['bpm']:.0f} key={m['key']} h/p={m['hp']:.1f} "
              f"<2kHz={m['low']:.1f}% voiced={m['voiced']:.2f} f0={m['f0']:.0f}Hz onset/s={m['onset']:.2f}")
