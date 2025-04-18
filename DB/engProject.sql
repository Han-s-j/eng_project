ALTER SESSION SET "_ORACLE_SCRIPT" = true;
-- ���� ���� ������: java, ���: oracle
CREATE USER eng IDENTIFIED BY eng;
-- ���� �ο� (���� & ���ҽ� ���� �� ����)
GRANT CONNECT, RESOURCE TO eng;
-- ���̺� �����̽� ���ٱ���(�������� ���� ����)
GRANT UNLIMITED TABLESPACE TO eng;

CREATE TABLE az_list(
    az_num NUMBER PRIMARY KEY
    ,az_eng VARCHAR2(1)
);

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

CREATE TABLE members (
     mem_id VARCHAR2(50)      PRIMARY KEY           --ȸ�� ID(�⺻ Ű)
    ,mem_pw VARCHAR2(1000)    NOT NULL              -- ȸ�� ��й�ȣ(�� ������)
    ,mem_nm VARCHAR2(100)                           -- ȸ�� �̸�
    ,mem_addr VARCHAR2(1000)                        -- ȸ�� �ּ�
    ,profile_img VARCHAR2(1000)                     -- ������ �̹��� URL �Ǵ� ���
    ,use_yn  VARCHAR2(1)       DEFAULT 'Y'          
    ,update_dt  DATE           DEFAULT SYSDATE      
    ,create_dt DATE            DEFAULT SYSDATE          
);

CREATE TABLE my_sent_list(
    word_num NUMBER                        -- �ܾ���� ��ȣ        
    ,sent_num NUMBER PRIMARY KEY           -- ���� ���� ��ȣ
    ,my_sent VARCHAR2(1000)                -- �ۼ� ���� ����
    ,mem_id VARCHAR2(100)                  -- �ۼ��� ID
    ,sent_reg_date DATE DEFAULT SYSDATE    
    ,use_yn VARCHAR2(1) DEFAULT 'Y'        
    ,CONSTRAINT fk_sent_wordnum FOREIGN KEY (word_num) REFERENCES word_list(word_num)
    ,CONSTRAINT fk_sent_memid FOREIGN KEY (mem_id) REFERENCES members(mem_id)
);

CREATE SEQUENCE sent_seq
INCREMENT BY 1
START WITH 1
NOCACHE
NOCYCLE;

ALTER TABLE word_list ADD CONSTRAINT uq_word_eng UNIQUE (word_eng);

CREATE TABLE user_word (
    mem_id VARCHAR(100) NOT NULL                            -- ����� ID (members ���̺��� mem_id�� ����)
    ,word_eng VARCHAR2(1000) NOT NULL                       -- �ܾ� ID (word_list ���̺��� word_eng�� ����)
    ,study_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP         -- �н� ��¥ (���� ����)
    ,PRIMARY KEY (mem_id, word_eng)                         -- ���� �⺻Ű
    ,FOREIGN KEY (mem_id) REFERENCES members(mem_id)        -- member ���̺��� mem_id ����
    ,FOREIGN KEY (word_eng) REFERENCES word_list(word_eng)  -- word_list ���̺��� word_eng ����
);
---------------------------------------------------
SELECT *
FROM user_word
WHERE mem_id = 'su';

SELECT mem_id, word_eng, study_date
FROM user_word
WHERE mem_id = 'su';

INSERT INTO user_word (mem_id, word_eng)
VALUES ('su', 'address');

SELECT *
FROM members;

DELETE 
FROM members;

SELECT *
FROM word_list;
-- @�� �����ϴ� �ܾ�
SELECT word_eng
FROM word_list
WHERE word_eng LIKE 'a%';

SELECT a.word_eng, b.az_eng
FROM az_list b
JOIN word_list a ON LOWER(a.word_eng) LIKE CONCAT(LOWER(b.az_eng),'%')
ORDER BY b.az_eng, a.word_eng;

INSERT INTO members (mem_id, mem_pw, mem_nm)
VALUES ('test', '1234', 'test');

INSERT INTO my_sent_list (word_num, sent_num, my_sent, mem_id)
VALUES ('1', sent_seq.NEXTVAL, 'Please note my change of address.', 'test');
INSERT INTO my_sent_list (word_num, sent_num, my_sent, mem_id)
VALUES ('1',sent_seq.NEXTVAL, 'Is that your home address?', 'test');

-- ����� ���� ��ȸ
select *
from my_sent_list
WHERE mem_id = 'su';

-- ���� ������ ����
DELETE 
FROM my_sent_list
WHERE mem_id = 'su';

DELETE 
FROM my_sent_list;




SELECT a.word_eng, b.my_sent,b.sent_num, c.mem_id
FROM word_list a
    ,my_sent_list b
    , members c
WHERE a.word_num =b.word_num
AND   b.mem_id = c.mem_id
AND  a.word_eng = 'address'
AND b.mem_id = 'su'
AND b.del_yn ='N'
ORDER BY sent_reg_date DESC;

SELECT a.word_eng, b.my_sent, b.sent_num, c.mem_id
FROM word_list a
JOIN my_sent_list b ON a.word_num = b.word_num
JOIN members c ON b.mem_id = c.mem_id
WHERE a.word_eng = 'address'
  AND b.mem_id = 'su'
  AND b.del_yn = 'N'
ORDER BY b.sent_reg_date DESC;

SELECT word_num, sent_num, my_sent, mem_id, sent_reg_date, use_yn
FROM my_sent_list;
--WHERE mem_id = 'test';

-- ���� ��ü ��ȸ
SELECT a.word_eng, b.word_num ,b.my_sent, c.mem_id, b.sent_reg_date
FROM word_list a
    ,my_sent_list b
    , members c
WHERE a.word_num =b.word_num
AND   b.mem_id = c.mem_id
--AND  b.word_num = 4;
AND  a.word_eng = 'address'
AND b.mem_id = 'test'
ORDER BY sent_reg_date DESC;


-- ���� ����
UPDATE my_sent_list
SET del_yn = 'Y'
WHERE sent_num = 60
AND mem_id = 'su';

-- �÷��� ����
ALTER TABLE my_sent_list
RENAME COLUMN use_yn TO del_yn;
-- DEFAULT �� ����
ALTER TABLE my_sent_list
MODIFY del_yn VARCHAR2(1) DEFAULT 'N';

-- word_list �н��Ϸ� �÷� �߰�
ALTER TABLE word_list ADD study_yn VARCHAR2(1) DEFAULT 'N';
-- myvoca ����
SELECT word_eng
FROM word_list
WHERE study_yn = 'Y';
    
-- �н� yn ����
UPDATE word_list
SET study_yn = 'Y'
WHERE word_eng = 'address';
        
SELECT
    word_num
    ,word_eng
FROM word_list
WHERE word_num = 1;

-- �����
SELECT a.word_eng, a.word_num, b.audio_num,b.audio_file,b.ipk_eng
FROM word_list a,audio_list b
WHERE a.word_num =b.word_num
AND  a.word_num = 4;

SELECT ipk_eng
FROM audio_list;

-- �ܾ��ȣ�� �´� ���� ���
SELECT def_eng
FROM def_list
WHERE word_num = 1;

--1	about
SELECT *
FROM word_list;

SELECT *
FROM def_list;

SELECT *
FROM ex_list;

SELECT a.word_num
        , a.word_eng
        , b.def_num
        , b.def_eng
        , c.ex_num
        , c.ex_eng
FROM word_list a
    ,def_list b
    ,ex_list c
WHERE a.word_num =b.word_num
AND   b.def_num = c.def_num
AND  a.word_eng ='about';

SELECT a.word_eng, b.my_sent, c.mem_id
FROM word_list a
    ,my_sent_list b
    , members c
WHERE a.word_num =b.word_num
AND   b.mem_id = c.mem_id
AND  a.word_eng = 'address'
AND b.mem_id = 'test'
ORDER BY sent_reg_date DESC ;
        
CREATE OR REPLACE DIRECTORY sql_dir AS 'C:\sql_backup\';
GRANT READ, WRITE ON DIRECTORY sql_dir TO eng;
