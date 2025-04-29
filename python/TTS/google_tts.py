from gtts import gTTS

# 텍스트 입력 (영어)
text = "Hello! This is a test of Google Text-to-Speech in English."

# gTTS 객체 생성 (언어 선택: 영어 -> 'en')
tts = gTTS(text=text, lang='en')

# MP3 파일로 저장
tts.save("english_output.mp3")

print("저장 완료!")
