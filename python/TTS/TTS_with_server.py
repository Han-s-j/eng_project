# 프론트에서 텍스트를 입력받고 TTS 반영하고 프론트에서 음성 재생하게 하기
from flask import Flask, request, send_file
from gtts import gTTS
import io
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://127.0.0.1:3000"])

@app.route('/tts', methods=['POST', 'OPTIONS'])
def tts():
    if request.method == 'OPTIONS':
        # CORS preflight 요청 응답
        response = app.make_default_options_response()
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        response.headers.add("Access-Control-Allow-Origin", "http://127.0.0.1:3000")
        return response

    data = request.json
    text = data.get("text", "")
    if not text:
        return "No text provided", 400

    tts = gTTS(text, lang='en')
    audio_fp = io.BytesIO()
    tts.write_to_fp(audio_fp)
    audio_fp.seek(0)

    response = send_file(audio_fp, mimetype="audio/mpeg")
    response.headers.add("Access-Control-Allow-Origin", "http://127.0.0.1:3000")
    return response

if __name__ == '__main__':
    app.run(debug=True)
