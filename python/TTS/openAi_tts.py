import openai

openai.api_key = ""  # ← 여기에 본인 API 키 입력

response = openai.audio.speech.create(
    model="tts-1",  # 또는 "tts-1-hd"
    voice="nova",   # "nova", "echo", "fable", "onyx", "shimmer"
    input="hey, What's going on!"
)

# 결과 파일 저장
with open("output.mp3", "wb") as f:
    f.write(response.content)
