-- 트랜잭션(Transaction)은 여러 SQL 작업을 하나의 작업 단위로 묶어 처리하는 것. 
-- 단위별 데이처 처리를 의미한다.
-- 예를 들어 '계좌이체'처럼
-- - A 계좌 출금
-- - B 계좌 입금
-- 두 작업이 모두 성공해야 하나의 정상 처리된다. 중간에 실패라면 원래의 작업으로 복귀.
-- 트랜잭션은 여러 SQL 문을 하나의 논리적인 작업 단위로 처리하며, 
-- 모두 성공하면 COMMIT, 문제가 생기면 ROLLBACK 한다.
-- INSERT, UPDATE, DELETE 같은 DML 문이 실행되면 트랜잭션이 시작되며, 
-- 명시적 트랜잭션에서는 COMMIT 또는 ROLLBACK을 만나면 종료된다.

-- MaiaDB는 묵시적으로 INSERT, UPDATE, DELETE 하면 자동 commit 된다. 
-- 즉, client의 자료를 근거로 db-server의 자료를 갱신한다.
-- 현재 설정 확인:  SELECT @@autocommit;   결과가 1이면 자동 커밋 상태임

CREATE TABLE jiktab AS SELECT * FROM jikwon;
SELECT * FROM jiktab;

SELECT @@autocommit;	-- 1
SET autocommit = FALSE;	-- 트랜젝션을 수동으로
SELECT @@autocommit;	-- 0
SELECT * FROM jiktab;
DELETE FROM jiktab WHERE jikwonno >= 6;
SELECT * FROM jiktab;

UPDATE jiktab SET jikwonjik='주임' WHERE jikwonno=4;
SELECT * FROM jiktab WHERE jikwonno=4;	-- deadlock
COMMIT;	 -- deadlock 해제
SELECT * FROM jiktab WHERE jikwonno=4;
SET autocommit = TRUE;

-- view 파일 (객체):
-- 실제 데이터(물리적 테이블)를 별도로 저장하는 파일이 아니라,
-- select 문을 저장하여 ㅔ이블처럼 사용할 수 있게 만든 데이터베이스 객체이다. 가상의 테이블.
-- 실제 데이터를 별도로 복사해 저장하는 일반 테이블은 아님
-- 원본 테이블의 데이터를 기준으로 조회 결과를 보여줌
-- 복잡한 select 문을 단순학 ㅔ재사용할 수 있음
-- 필요한 컬럼만 보여줘 보안에도 활용 가능

-- view 기본 형식: create view 뷰이름 as select 컬럼명1, 컬럼명2, ... from 테이블명 where 조건;
-- 조회 형식: select * from 뷰이름;
-- 삭제 형식: drop view 뷰이름;


SELECT jikwonno,jikwonname, jikwonpay FROM jikwon WHERE jikwonibsail < '2010-12-31'

SHOW TABLES;
SELECT * FROM v_a;
DESC v_a;
SELECT sum(jikwonpay)FROM v_a;

DROP VIEW v_b;
CREATE VIEW v_b AS
SELECT * FROM jikwon WHERE jikwonname LIKE '김%' OR jikwonname LIKE '박%';
SELECT * FROM v_b;
SELECT * FROM v_a;

ALTER TABLE jikwon RENAME kbs;
SELECT * FROM jikwon;	-- Table 'test.jikwon' doesn't exist
SELECT * FROM v_b;	-- err
SELECT * FROM v_a;	-- err

ALTER TABLE kbs RENAME jikwon;
SELECT * FROM v_b;	-- good
SELECT * FROM v_a;	-- good

CREATE VIEW v_c AS SELECT * FROM jikwon ORDER BY jikwonpay DESC;	-- 정렬
SELECT * FROM v_c;

CREATE VIEW v_d AS SELECT jikwonname, jikwonpay * 10000 AS ypay FROM jikwon;	-- 계산 컬럼 적용
SELECT * FROM v_d;

CREATE VIEW v_e AS SELECT * FROM v_d WHERE ypay >= 50000000;	-- view로 view를 생성
SELECT * FROM v_e;
RENAME TABLE v_e TO mbc;	-- view 객체 이름 변경
SELECT * FROM mbc;

CREATE VIEW v_f AS SELECT * FROM jikwon WHERE jikwonpay >= 5000;
SELECT * FROM v_f;
UPDATE v_f SET jikwonname='사오정' WHERE jikwonname='홍길동';
SELECT * FROM v_f;
UPDATE v_f SET jikwonname='저팔계' WHERE jikwonno=30;	-- viewdp 30번이 존재하지 않으므로 원본에 영향x
SELECT * FROM v_f;
SELECT * FROM jikwon;
DELETE FROM v_f WHERE jikwonno=22;

CREATE VIEW v_g AS SELECT jikwonno,jikwonname,busernum,jikwonpay FROM jikwon;
SELECT * FROM v_g;
INSERT INTO v_g VALUES(31,'손오공',10,7000);	-- view를 이용해 원본 ㅔ이블에 자료를 저장
SELECT * FROM v_g;
SELECT * FROM jikwon;

CREATE VIEW v_h AS
SELECT jikwonjik,SUM(jikwonpay) AS hap, AVG(jikwonpay) AS ave FROM jikwon
GROUP BY jikwonjik;	-- group by 도 view 작성 가능
SELECT * FROM v_h;

-- join 도 가능