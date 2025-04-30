# TTS 음성 생성
# Whisper로 단어별 타임스탬프 추출
# 각 단어에 대해 RMS, Pitch, Duration 자동 계산
# 분석 데이터를 JSON으로 반환
# + TTS 파일을 클라이언트에 전달

from flask import Flask, request, jsonify
from gtts import gTTS
from pydub import AudioSegment
import whisper_timestamped as whisper
import librosa
import numpy as np
import tempfile
import os
from flask_cors import CORS
import shutil

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=[
    "http://127.0.0.1:3000",  # 이전 React 개발 주소
    "http://localhost:8080"   # JSP(Spring) 주소
                                              ])
model = whisper.load_model("base")  # whisper-timestamped

@app.route('/analyze', methods=['POST', 'OPTIONS'])
def analyze_text():
    origin = request.headers.get('Origin', '')
    allowed_origins = ["http://localhost:8080", "http://127.0.0.1:3000"]
    if request.method == 'OPTIONS':
        # CORS preflight 요청 응답
        response = app.make_default_options_response()
        if origin in allowed_origins:
            response.headers.add("Access-Control-Allow-Origin", origin)
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response
    data = request.json
    text = data.get('text', '')
    if not text:
        return jsonify({"error": "No text provided"}), 400

    # --- TTS 생성 ---
    tts = gTTS(text, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as mp3_fp:
        tts.save(mp3_fp.name)
        mp3_path = mp3_fp.name

    # static 디렉토리에 복사
    tts_filename = "tts_output.mp3"
    static_path = os.path.join("static", tts_filename)
    os.makedirs("static", exist_ok=True)
    shutil.copy(mp3_path, static_path)

    # --- mp3 → wav 변환 ---
    wav_path = mp3_path.replace(".mp3", ".wav")
    AudioSegment.from_mp3(mp3_path).export(wav_path, format="wav")

    # --- Whisper로 단어별 타임스탬프 추출 ---
    result = whisper.transcribe(model, wav_path)
    y, sr = librosa.load(wav_path)

    word_data = []
    for segment in result['segments']:
        print(segment['words'])
        for word in segment['words']:
            word_text = word['text'].strip()
            start = word['start']
            end = word['end']

            if end > start:
                # 해당 단어의 음성 영역 추출
                start_sample = int(start * sr)
                end_sample = int(end * sr)
                y_segment = y[start_sample:end_sample]

                # 강세 계산
                rms = float(np.mean(librosa.feature.rms(y=y_segment)))
                pitch_values = librosa.yin(y_segment, fmin=50, fmax=400, sr=sr)
                pitch = float(np.nanmean(pitch_values)) if np.any(~np.isnan(pitch_values)) else 0.0
                duration = float(end - start)

                word_data.append({
                    "word": word_text,
                    "start": round(start, 2),
                    "end": round(end, 2),
                    "rms": round(rms, 5),
                    "pitch": round(pitch, 2),
                    "duration": round(duration, 3)
                })

    # --- 정리된 데이터 반환 ---
    os.remove(mp3_path)
    os.remove(wav_path)

    return jsonify({
        "words": word_data,
        "original_text": text,
        "audio_url": "http://localhost:5000/static/tts_output.mp3"
    })

if __name__ == '__main__':
    app.run(debug=True)
