import matplotlib.pyplot as plt
import numpy as np
import librosa
import whisper

# 1. Whisper 모델 로드
model = whisper.load_model("base")

# 2. 오디오 + 자막 추출
file_path = "english_output.mp3"
result = model.transcribe(file_path)
segments = result["segments"]

# 3. 오디오 불러오기 및 Envelope 계산
y, sr = librosa.load(file_path)
frame_size = 1000
y_split = np.array_split(np.abs(y), len(y) // frame_size)
y_envelope = np.array([np.mean(chunk) for chunk in y_split])
times = np.linspace(0, len(y) / sr, len(y_envelope))

# 4. 시각화
plt.figure(figsize=(13, 3))
plt.plot(times, y_envelope, color='gray', linewidth=2)
plt.fill_between(times, y_envelope, alpha=0.3, color='#cceeff')

# 5. 자막 + 강세 위치
for i, segment in enumerate(segments):
    start = segment['start']
    end = segment['end']
    text = segment['text'].strip()

    # segment 내 파형 분석
    start_sample = int(start * sr)
    end_sample = int(end * sr)
    if end_sample > len(y):
        continue

    segment_y = np.abs(y[start_sample:end_sample])
    segment_times = np.linspace(start, end, len(segment_y))

    # 가장 강한 부분 (강세 peak)
    min_idx = np.argmin(segment_y)
    min_time = segment_times[min_idx]
    min_amp = segment_y[min_idx]

    # 자막 표시
    y_pos = min_amp * 0.9

    plt.text(min_time, y_pos, text,
             fontsize=10,
             ha='center',
             va='top',
             weight='bold',
             color='black',
             bbox=dict(facecolor='white', edgecolor='blue', boxstyle='round,pad=0.3', alpha=0.6))

# 마무리
plt.axis('off')
plt.title("Follow the Stress: Speak with the Wave!", fontsize=13, weight='bold')
plt.tight_layout()
plt.show()
