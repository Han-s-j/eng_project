import cx_Oracle
import requests
import json
import logging

# ========== 설정 ==========
app_id = "27b7e407"       #  Oxford API ID
app_key = "90833dce0340e245fa4e67934562a095"     # Oxford API Key
language_code = "en-us"
endpoint = "entries"

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ========== DB 연결 클래스 ==========
class DBManager:
    def __init__(self):
        self.conn = None

    def get_connection(self):
        try:
            if self.conn is None:
                self.conn = cx_Oracle.connect("eng", "eng", "localhost:1521/xe")
                logger.info("✅ DB 연결 성공")
            else:
                try:
                    self.conn.ping()
                except cx_Oracle.Error:
                    logger.warning("🔄 연결 끊김 → 재연결")
                    self.conn = cx_Oracle.connect("eng", "eng", "localhost:1521/xe")
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


# ========== 단어 조회 ==========
def fetch_words_from_db():
    db = DBManager()
    conn = db.get_connection()

    if conn is None:
        print("❌ DB 연결 실패")
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


# ========== Oxford API 요청 ==========
def query_oxford_api(word):
    word_id = word.lower()
    url = f"https://od-api-sandbox.oxforddictionaries.com/api/v2/{endpoint}/{language_code}/{word_id}"

    headers = {
        "app_id": app_id,
        "app_key": app_key
    }

    r = requests.get(url, headers=headers)
    print(f"\n📨 '{word}' 요청 → 응답 코드: {r.status_code}")

    if r.status_code == 200:
        try:
            data = r.json()
            print(json.dumps(data, indent=4))  # 예쁘게 출력
        except ValueError:
            print("⚠️ JSON 파싱 실패")
    else:
        print(f"❌ 오류 코드 {r.status_code}: {r.text}")


# ========== 실행 ==========
def main():
    word_list = fetch_words_from_db()

    for word in word_list:
        query_oxford_api(word)


if __name__ == "__main__":
    main()
