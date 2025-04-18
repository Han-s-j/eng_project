import cx_Oracle
import requests
import json
import pandas as pd
import logging

# ====== 설정 ======
app_id = "your_app_id"       # Oxford API ID
app_key = "your_app_key"     # Oxford API Key
language_code = "en-us"
endpoint = "entries"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ====== DB 연결 클래스 ======
class DBManager:
    def __init__(self):
        self.conn = None

    def get_connection(self):
        try:
            if self.conn is None:
                self.conn = cx_Oracle.connect("eng", "eng", "localhost:1521/xe")
                logger.info("✅ DB 연결 성공")
            return self.conn
        except Exception as e:
            logger.error(f"❌ DB 연결 오류: {e}")
            return None

    def close(self):
        if self.conn:
            self.conn.close()
            logger.info("🔌 DB 연결 종료")

    def __del__(self):
        self.close()


# ====== DB에서 'a'로 시작하는 단어 조회 ======
def fetch_words_from_db():
    db = DBManager()
    conn = db.get_connection()
    if conn is None:
        return []

    try:
        cursor = conn.cursor()
        sql = "SELECT word_eng FROM word_list WHERE LOWER(word_eng) LIKE 'a%'"
        cursor.execute(sql)
        words = [row[0] for row in cursor.fetchall()]
        logger.info(f"🔍 'a'로 시작하는 단어 {len(words)}개 조회됨")
        return words
    except Exception as e:
        logger.error(f"쿼리 오류: {e}")
        return []
    finally:
        cursor.close()
        db.close()


# ====== Oxford API 요청 ======
def query_oxford_api(word):
    url = f"https://od-api-sandbox.oxforddictionaries.com/api/v2/{endpoint}/{language_code}/{word.lower()}"
    headers = {"app_id": app_id, "app_key": app_key}

    response = requests.get(url, headers=headers)
    print(f"\n📨 '{word}' 요청 → 응답 코드: {response.status_code}")
    if response.status_code == 200:
        return response.json()
    else:
        logger.warning(f"❌ '{word}' 요청 실패: {response.status_code}")
        return None


# ====== 응답 데이터 처리 & 엑셀 저장 ======
def process_data(data, word):
    results = data.get('results', [])
    if not results:
        logger.warning(f"⚠️ '{word}'의 results 없음")
        return

    lexical_entries = results[0].get('lexicalEntries', [])

    definitions_data = []
    examples_data = []
    audio_files_data = []

    for lexical_entry in lexical_entries:
        entries = lexical_entry.get('entries', [])
        for entry in entries:
            senses = entry.get('senses', [])

            for sense in senses:
                defs = sense.get("definitions", [])
                exs = [ex.get("text") for ex in sense.get("examples", [])]

                if defs:
                    definitions_data.append({'word': word, 'definition': defs[0]})
                if exs:
                    examples_data.append({'word': word, 'example': exs[0]})

                for subsense in sense.get("subsenses", []):
                    sub_defs = subsense.get("definitions", [])
                    sub_exs = [ex.get("text") for ex in subsense.get("examples", [])]

                    if sub_defs:
                        definitions_data.append({'word': word, 'definition': sub_defs[0]})
                    if sub_exs:
                        examples_data.append({'word': word, 'example': sub_exs[0]})

            for pron in entry.get("pronunciations", []):
                if 'audioFile' in pron:
                    audio_files_data.append({'word': word, 'audio_url': pron['audioFile']})

    # 데이터프레임 생성 및 엑셀 저장
    if definitions_data:
        pd.DataFrame(definitions_data).to_excel(f'definitions_{word}.xlsx', index=False, engine='openpyxl')
    if examples_data:
        pd.DataFrame(examples_data).to_excel(f'examples_{word}.xlsx', index=False, engine='openpyxl')
    if audio_files_data:
        pd.DataFrame(audio_files_data).to_excel(f'audio_{word}.xlsx', index=False, engine='openpyxl')

    logger.info(f"📁 '{word}' 관련 데이터 저장 완료")


# ====== 실행 ======
def main():
    word_list = fetch_words_from_db()
    for word in word_list:
        data = query_oxford_api(word)
        if data:
            process_data(data, word)

if __name__ == "__main__":
    main()
