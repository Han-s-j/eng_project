import matplotlib.pyplot as plt
import numpy as np
import librosa
import librosa.display

# gTTS로 저장한 파일 불러오기

file_path = "english_output.mp3"
y, sr = librosa.load(file_path)

plt.figure(figsize=(10, 3))
librosa.display.waveshow(y, sr=sr)
plt.title('Waveform (Minimal)')
plt.axis('off')  # 축 없애기
plt.tight_layout()
plt.show()


# 1. 파형 시각화

plt.figure(figsize=(10, 4))
librosa.display.waveshow(y, sr=sr)
plt.title('Waveform')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.tight_layout()
plt.show()

# 다운샘플링: 매 100개의 샘플마다 평균을 내서 간략화

hop = 100
y_simplified = np.mean(y[:len(y)//hop*hop].reshape(-1, hop), axis=1)
times = np.linspace(0, len(y)/sr, len(y_simplified))

plt.figure(figsize=(10, 3))
plt.plot(times, y_simplified)
plt.title('Simplified Waveform')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.tight_layout()
plt.show()


# 2. 스펙트로그램 시각화

plt.figure(figsize=(10, 4))
D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='log')
plt.colorbar(format='%+2.0f dB')
plt.title('Spectrogram')
plt.tight_layout()
plt.show()

# 멜 스펙트로그램

S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=64)
S_db = librosa.amplitude_to_db(S, ref=np.max)

plt.figure(figsize=(10, 4))
librosa.display.specshow(S_db, sr=sr, x_axis='time', y_axis='mel')
plt.colorbar(format='%+2.0f dB')
plt.title('Mel-Spectrogram')
plt.tight_layout()
plt.show()
