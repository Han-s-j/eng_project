# 강세 분석 시각화
import librosa
import numpy as np
import matplotlib.pyplot as plt

# MP3 파일 로드
file_path = "english_output.mp3"
y, sr = librosa.load(file_path)

# 강세 계산을 위한 파형 분할
frame_size = 1000
y_split = np.array_split(np.abs(y), len(y) // frame_size)
y_envelope = np.array([np.mean(chunk) for chunk in y_split])
times = np.linspace(0, len(y) / sr, len(y_envelope))

# 강세 시각화
plt.figure(figsize=(12, 3))
plt.plot(times, y_envelope, color='black', linewidth=1)
plt.fill_between(times, y_envelope, alpha=0.3, color='white')
plt.title('Waveform Envelope')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.tight_layout()
plt.show()
