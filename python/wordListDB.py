import cx_Oracle
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
                    logger.warning("⚠️ 기존 연결 끊김, 재연결 시도")
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


def get_word_list():
    db = DBManager()
    conn = db.get_connection()

    if conn is None:
        print("DB 연결 실패")
        return

    try:
        cursor = conn.cursor()
        sql = "SELECT word_num, word_eng FROM word_list"
        cursor.execute(sql)

        rows = cursor.fetchall()
        print("📋 word_list 테이블 데이터:")
        for row in rows:
            print(f"NUM: {row[0]}, ENG: {row[1]}")

    except Exception as e:
        print(f"쿼리 실행 중 오류 발생: {e}")
    finally:
        cursor.close()
        db.close()


# 실행 예시
if __name__ == "__main__":
    get_word_list()
