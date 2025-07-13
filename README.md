# 📘 예문 중심 영어 학습 웹사이트

Oxford Dictionary API를 활용하여 단어의 정의, 예문, 발음 정보를 제공하고  
TTS(음성 합성) 기능을 통해 사용자 발음 분석까지 가능한 영어 학습 웹서비스입니다.

---

## 💡 주요 기능

- 📖 단어 정의 / 예문 제공 (Oxford API)
- 🔊 발음기호 / 음성 출력 / 발음 분석 (Flask + TTS)
- 📒 사용자 단어장 저장
- 🎒 문장 주머니 기능 (사용자 입력 문장 모음)
- 📂 엑셀 파일로 예문 데이터 정리

---

## 🛠 기술 스택

| 구분       | 기술/도구                             |
|------------|----------------------------------------|
| 프론트엔드 | HTML, CSS, JavaScript, Thymeleaf       |
| 백엔드     | Spring Boot, Python (Flask - TTS 분석) |
| DB         | Oracle DB                              |
| 기타       | Figma, VSCode                      |

---

## 📷 화면 예시

### 🏠 홈 화면
> 사용자가 처음 접하는 기본 페이지 UI

![home](./images/home.png)

---

### 🎯 주요 기능 시연
> 예문 보기 → 발음 듣기 → 발음 분석

![demo](./images/demo.gif)

---

## ⚙️ 실행 방법

### 🔽 1. Flask 서버 실행 (TTS 분석용)
```bash
cd flask_server/
python app.py
