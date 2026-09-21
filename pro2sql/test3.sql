-- 인덱스(index): 책의 목차나 색인과 비슷하다. 검색 속도 향상이 목표
-- 인덱스 없음 -> 처음부터 끝까지 데이터를 확인
-- 인덱스 있음 -> 위치를 빠르게 찾아서 데이터 접근

CREATE TABLE aa(id INT AUTO_INCREMENT PRIMARY KEY, NAME VARCHAR(20), age INT, city VARCHAR(30));

INSERT INTO aa(NAME, age, city) VALUES
('홍길동', 25, '서울'),
('김철수', 30, '부산'),
('이영희', 27, '서울'),
('박민수', 35, '대전'),
('최영희', 23, '인천'),
('강호동', 40, '서울'),
('유재석', 38, '부산'),
('신동엽', 42, '서울'),
('홍길동', 29, '수원'),
('김민지', 31, '대구')

SELECT * FROM aa;

SELECT * FROM aa WHERE NAME='강호동';	-- 인덱스가 없으므로 처음부터 찾아야함

-- 실행 계획 확인
EXPLAIN SELECT * FROM aa WHERE NAME='강호동';	-- type: ALL - Full Table Scan

-- 검색을 자주하는 name에 인덱스 생성 - 인덱스 테이블 별도 생성
CREATE INDEX idx_aa_name ON aa(NAME);	-- 이미 테이블이 있는 경우
SHOW INDEX FROM aa;	-- idx_aa_name과 pk(인덱스 자동생성) 인덱스 확인 가능
SHOW KEYS FROM aa;	-- 상동

-- 테이블 생성 시 인덱스 부여
CREATE TABLE aa(id INT AUTO_INCREMENT PRIMARY KEY, NAME VARCHAR(20), age INT, city VARCHAR(30), INDEX idx_aa_name(NAME));

-- 참고: 인덱스가 여러 개인 경우 '옵티마이저'가 적당한 인덱스를 선택해 실행

DESC aa;

-- idx_aa_name 테이블 생성
-- 강호동 -> 위치(pointer - pk값)pk가 없으면 내부적으로 row id 를 만듬
-- 이영희 -> 위치

-- index 삭제
DROP INDEX idx_aa_name ON aa;
SHOW INDEX FROM aa;

-- index는 특정 칼럼의 검색속도 증진이 목적이나 단점도 있다.
-- insert, update, delete 등이 빈번한 경우에는 인덱스 재설정 비용이 든다.

-- 참고: 내장함수 now(), sysdate()의 차이
SELECT NOW(), SLEEP(2), NOW(); -- 결과가 같다
SELECT NOW(), SLEEP(2), SYSDATE();	-- 결과가 다르다
-- sysdate()는 동인 sql 문장 내에서 호출되는 시점에 따라 결과값을 바로 반환

-- 테이블 관련 명령
-- create table 테이블명 ~ 생성
-- alter table 테이블명 ~ 구조를 수정
-- drop table 테이블명 ~ 삭제

CREATE TABLE aa(irum CHAR(10), juso VARCHAR(50));
ALTER TABLE aa RENAME kbs;	-- 테이블 이름 변경
SELECT * FROM aa;	-- X
SELECT * FROM kbs;	-- O

-- 칼럼 관련 명령
ALTER TABLE aa ADD (job_id INT DEFAULT 10);	-- 칼럼 추가
DESC aa;
INSERT INTO aa VALUES('tom', 'seoul', 20);
INSERT INTO aa(irum, juso) VALUES('tom2', 'jeju');
SELECT * FROM aa;

ALTER TABLE aa CHANGE job_id job_number INT;	-- 칼럼 명 변경
SELECT * FROM aa;

ALTER TABLE aa MODIFY job_number VARCHAR(10);	-- 칼럼 타입 변경
DESC aa;

ALTER TABLE aa DROP COLUMN job_number;	-- 칼럼 삭제
DESC aa;
SELECT FROM aa;

DROP TABLE aa;

