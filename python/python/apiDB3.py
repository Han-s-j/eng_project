import cx_Oracle
import requests
import json
import pandas as pd
import os
import logging

# ====== 설정 ======
app_id = "your_app_id"       # ← 너의 Oxford API app_id
app_key = "your_app_key"     # ← 너의 Oxford API app_key
language_code = "en-us"
endpoint = "entries"
save_dir = "output"
os.makedirs(save_dir, exist_ok=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====== 누적 저장 리스트 ======
def_list = []
ex_list = []
audio_list = []

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
    logger.info(f"📨 '{word}' 요청 → 응답 코드: {response.status_code}")
    if response.status_code == 200:
        return response.json()
    else:
        logger.warning(f"❌ '{word}' 요청 실패: {response.status_code}")
        return None


# ====== 응답 데이터 처리 ======
def process_data(data, word, word_num, def_counter):
    lexical_entries = data.get('results', [])[0].get('lexicalEntries', [])
    audio_num = 0

    for lexical_entry in lexical_entries:
        entries = lexical_entry.get('entries', [])
        for entry in entries:
            senses = entry.get('senses', [])

            for sense in senses:
                defs = sense.get("definitions", [])
                examples = [ex.get("text") for ex in sense.get("examples", [])]

                if defs:
                    def_counter += 1
                    def_list.append({
                        'word_num': word_num,
                        'def_num': def_counter,
                        'def_eng': defs[0]
                    })

                    for ex_idx, ex in enumerate(examples, start=1):
                        ex_list.append({
                            'def_num': def_counter,
                            'ex_num': ex_idx,
                            'ex_eng': ex
                        })

                for subsense in sense.get("subsenses", []):
                    sub_defs = subsense.get("definitions", [])
                    sub_examples = [ex.get("text") for ex in subsense.get("examples", [])]

                    if sub_defs:
                        def_counter += 1
                        def_list.append({
                            'word_num': word_num,
                            'def_num': def_counter,
                            'def_eng': sub_defs[0]
                        })

                        for ex_idx, ex in enumerate(sub_examples, start=1):
                            ex_list.append({
                                'def_num': def_counter,
                                'ex_num': ex_idx,
                                'ex_eng': ex
                            })

            for pron in entry.get("pronunciations", []):
                if 'audioFile' in pron:
                    audio_num += 1
                    audio_list.append({
                        'word_num': word_num,
                        'audio_num': audio_num,
                        'audio_file': pron.get('audioFile'),
                        'ipk_ENG': pron.get('phoneticSpelling', '')
                    })
    return def_counter


# ====== 실행 ======
def main():
    word_list = fetch_words_from_db()
    word_num = 0
    def_counter = 0

    for word in word_list:
        word_num += 1
        data = query_oxford_api(word)
        if data:
            def_counter = process_data(data, word, word_num, def_counter)

    # 💾 누적된 데이터를 엑셀로 저장
    pd.DataFrame(def_list).to_excel(os.path.join(save_dir, 'def_list.xlsx'), index=False, engine='openpyxl')
    pd.DataFrame(ex_list).to_excel(os.path.join(save_dir, 'ex_list.xlsx'), index=False, engine='openpyxl')
    pd.DataFrame(audio_list).to_excel(os.path.join(save_dir, 'audio_list.xlsx'), index=False, engine='openpyxl')

    print("\n✅ 모든 단어의 데이터가 엑셀로 저장되었습니다!")


if __name__ == "__main__":
    main()
