ALTER SESSION SET "_ORACLE_SCRIPT" = true;
-- ���� ���� ������: java, ���: oracle
CREATE USER eng IDENTIFIED BY eng;
-- ���� �ο� (���� & ���ҽ� ���� �� ����)
GRANT CONNECT, RESOURCE TO eng;
-- ���̺� �����̽� ���ٱ���(�������� ���� ����)
GRANT UNLIMITED TABLESPACE TO eng;

CREATE TABLE word_list(
    word_num NUMBER PRIMARY KEY
    ,word_eng VARCHAR2(1000)
);

CREATE TABLE audio_list(
    word_num NUMBER
    ,audio_num NUMBER PRIMARY KEY
    ,audio_file VARCHAR2(100)
    ,ipk_eng VARCHAR2(50)
    ,CONSTRAINT fk_audio FOREIGN KEY (word_num) REFERENCES word_list(word_num) 
);

CREATE TABLE def_list(
    word_num NUMBER
    ,def_num NUMBER PRIMARY KEY
    ,def_eng VARCHAR2(1000)
    ,CONSTRAINT fk_def FOREIGN KEY (word_num) REFERENCES word_list(word_num)
);

CREATE TABLE ex_list(
    def_num NUMBER
    ,ex_num NUMBER PRIMARY KEY
    ,ex_eng VARCHAR2(1000)
    ,CONSTRAINT fk_ex FOREIGN KEY (def_num) REFERENCES def_list(def_num)
);

SELECT *
FROM word_list;
SELECT *
FROM audio;

SELECT a.word_eng, def_eng, ex_eng
FROM word_list a
JOIN def_list b ON a.word_num = b.word_num
JOIN ex_list c ON b.def_num = c.def_num;


