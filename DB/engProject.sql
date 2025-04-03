ALTER SESSION SET "_ORACLE_SCRIPT" = true;
-- 계정 생성 계정명: java, 비번: oracle
CREATE USER eng IDENTIFIED BY eng;
-- 권한 부여 (접속 & 리소스 생성 및 접근)
GRANT CONNECT, RESOURCE TO eng;
-- 테이블 스페이스 접근권한(물리적인 저장 차일)
GRANT UNLIMITED TABLESPACE TO eng;

CREATE TABLE word_list(
    word_num NUMBER PRIMARY KEY
    ,word_list VARCHAR2(1000)
    ,word_mean VARCHAR2(2000)
    ,etymology VARCHAR2(4000)
    ,ipk VARCHAR2(50)
    ,phonetics VARCHAR2(1000)
);

SELECT *
FROM word_list
ORDER BY word_num ASC;


