ALTER SESSION SET "_ORACLE_SCRIPT" = true;
-- ���� ���� ������: java, ���: oracle
CREATE USER eng IDENTIFIED BY eng;
-- ���� �ο� (���� & ���ҽ� ���� �� ����)
GRANT CONNECT, RESOURCE TO eng;
-- ���̺� �����̽� ���ٱ���(�������� ���� ����)
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


