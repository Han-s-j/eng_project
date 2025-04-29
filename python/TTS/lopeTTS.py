import matplotlib.pyplot as plt
import numpy as np
import librosa

# 1. 오디오 불러오기
file_path = "english_output.mp3"
y, sr = librosa.load(file_path)

# 2. Envelope 계산 (자동 쪼개기 방식 사용)
frame_size = 1000  # 프레임 크기 조절 가능
y_split = np.array_split(np.abs(y), len(y) // frame_size)
y_envelope = np.array([np.mean(chunk) for chunk in y_split])
times = np.linspace(0, len(y) / sr, len(y_envelope))

# 3. 시각화
plt.figure(figsize=(10, 2))
plt.plot(times, y_envelope, color='pink', linewidth=3)
plt.fill_between(times, y_envelope, alpha=0.3, color='#add8e6')
plt.title('Waveform Envelope (Simplified)')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.tight_layout()
plt.axis('off')
plt.show()
