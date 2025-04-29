# 강세가 있는 부분을 단어별로 색상 다르게 지정하기
import librosa
import numpy as np
import matplotlib.pyplot as plt
import whisper

# 1. Whisper 모델 로드
model = whisper.load_model("base")

# 2. 오디오 자막 추출
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
plt.figure(figsize=(12, 3))
plt.plot(times, y_envelope, color='black', linewidth=1)
plt.fill_between(times, y_envelope, alpha=0.3, color='white')

# 자막을 파형 아래 일정한 위치에 배치
y_text_position = -0.1  # 자막을 파형 바로 아래에 고정

font_size = 12  # 자막 글씨 크기 조정
for segment in segments:
    start = segment['start']
    end = segment['end']
    text = segment['text']

    # 자막이 나타날 시간대의 중간값 계산
    mid_time = (start + end) / 2

    # 자막을 단어별로 분리해서 처리
    words = text.split()  # 자막을 단어로 분리
    word_duration = (end - start) / len(words)  # 각 단어의 지속 시간

    for i, word in enumerate(words):
        word_start = start + i * word_duration  # 각 단어의 시작 시간
        word_end = word_start + word_duration  # 각 단어의 끝 시간
        word_mid_time = (word_start + word_end) / 2  # 단어의 중간 시간

        # 각 단어를 해당 시간대에 표시
        plt.text(word_mid_time, y_text_position, word, fontsize=font_size, ha='center', va='center',
                bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.2'))

# 그래프 마무리
plt.title('Waveform with Word-Level Stress Highlight')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.tight_layout()
plt.show()
