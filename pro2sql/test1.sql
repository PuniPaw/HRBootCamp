-- 주석
-- crud(create/insert, read/select, update, delete) 잠깐 연습
CREATE TABLE good(NO INT PRIMARY key, NAME VARCHAR(10) NOT NULL, tel VARCHAR(10),
inwon INT, addr TEXT);

-- 자료 추가
-- 형식: insert into 테이블명(컬럼 명 타입, ...) values(자료, ...)
INSERT INTO good(NO, NAME, tel, inwon, addr) VALUES(1, '인사과', '123-1234', 5, '삼성1동');

INSERT INTO good VALUES(2, '영업과', '223-2234', 15, '삼성2동');

INSERT INTO good(NO, NAME, inwon) VALUES ('3', '자재과', '7'); -- 순서가 다르다면 칼럼 명을 반드시 지정해 줘야 함

SELECT * FROM good;

-- 오류인 경우
INSERT INTO good(NO, NAME) VALUES(3, '자재3과') -- no 중복 err: Duplicate entry '3' for key 'PRIMARY'
INSERT INTO good(NO, tel) VALUES(5, '자재3과') -- err: not null - 반드시 입력
INSERT INTO good(NAME, NO) VALUES(5, '자재3과') -- err: 입력 자료와 컬럼의 순서가 불일치
INSERT INTO good(NO, NAME) VALUES('오', '자재3과') -- err: 입력자료 타입 불일치
INSERT INTO good(NAME, NO) VALUES(5, '우리회사에서 가장 매출이 좋은 부러운 부서') -- err: 컬럼에서 지정된 길이를 초과


-- 자료 수정
-- 형식: update 테이블명 set 칼럼명=수정값, ... where 조건
UPDATE good SET inwon=100 WHERE NO=1;
UPDATE good SET inwon=70, tel='777-7777' WHERE NO=2;
UPDATE good SET inwon=2, tel=null WHERE NO=3;

-- 오류인 경우
UPDATE good SET NAME=NULL WHERE NO=2;	-- name은 not null이라 null을 부여할 수 없다
UPDATE good SET NO=2 WHERE NO=1;	-- no (primary key) 중복 오류

-- 자료 삭제
-- 형식: delete from 테이블명 where 조건	- 부분적으로 행 삭제
DELETE FROM good WHERE NO=2;

-- 형식2: truncate table 테이블명	- where 조건 없음. 행 모두 삭제. 구조만 남음
TRUNCATE TABLE good;

DROP TABLE good; 	- 테이블 삭제

SHOW TABLES;	- 테이블 조회