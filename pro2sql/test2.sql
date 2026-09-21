-- 데이터베이스 무결성(Database Integrity)은 저장된 데이터가 정확하고 일관되며,
-- 손상되지 않고 신뢰할 수 있는 상태를 유지하는 것을 뜻합니다. 잘못된 자료 입력 방지를 위한 제약 조건 부여
-- 데이터의 품질을 지키고 오류를 막기 위해 데이터 베이스 관리 시스템(DBMS)이 지키는 핵심 규칙

-- 주요 무결성 제약조건
-- - 개체 무결성(Entity Integrity): 모든 테이블은 기본 키(primary key)를 가져야 합니다.
-- - 기본 키는 빈 값(null)이나 중복 값을 가질 수 없습니다.
-- - 도메인 무결성(Domain Integrity): 필드에 들어가는 값이 지정된 자료형, 범위, 조견(Check 등) 에


-- 기본 키(Primary key, pk) 제약 조건 - Entity Integrity
-- 기본 키는 빈 값(null)이나 중복 값을 가질 수 없다. 자동으로 인덱스가 생성됨.


-- 참고: 테이블 작성 시 컬럼의 이름, 타입은 중요. 순서는 마음대로.
-- 계산에 의해 처리될 수 있는 값은 칼럼으로 작성X ex) 국어, 영어
-- 방법 1) 컬럼 레벨
CREATE TABLE aa(bun INT PRIMARY KEY, irum CHAR(10));
DESC aa;
INSERT INTO aa VALUES(1, 'tom');
INSERT INTO aa VALUES(2, 'tom');
-- INSERT INTO aa VALUES(2, 'tom');	-- pk err: 중복 불가
-- INSERT INTO aa(irum) VALUES('tom');	-- pk err: not null

SELECT * FROM aa;

-- 제약 조건 확인
SELECT * FROM information_schema.table_constraints WHERE TABLE_NAME='aa';

DROP TABLE aa;

-- 방법 2) 테이블 레벨
CREATE TABLE aa(bun INT, irum CHAR(10), CONSTRAINT aa_bun_pk PRIMARY KEY(bun));
DESC aa;
SELECT * FROM information_schema.table_constraints WHERE TABLE_NAME='aa';
ALTER TABLE aa DROP CONSTRAINT aa_bun_pk; -- pk 제약조건 삭제
ALTER TABLE aa DROP;								-- pk 제약조건 삭제. 상동

DROP TABLE aa;

-- check 제약 조건 - Domain Integrity: 입력 값 조건에 따른 검사
CREATE TABLE aa(bun INT, irum CHAR(10), nai INT CHECK(nai >= 20));
SELECT * FROM information_schema.table_constraints WHERE TABLE_NAME='aa';
INSERT INTO aa VALUES(1, 'tom', 25);
INSERT INTO aa VALUES(1, 'tom', 15);	-- chk err: 조건 불만족

ALTER TABLE aa ADD CONSTRAINT ck_name CHECK(irum IN('tom', 'john'));	-- check 조건 추가
INSERT INTO aa VALUES(2, 'john', 25);
INSERT INTO aa VALUES(3, 'james', 25);		-- chk err: irum 조건 불만족

DROP TABLE aa;

-- unique 제약 조건 - Domain Integrity: 동일 값 입력 불허
CREATE TABLE aa(bun INT, irum CHAR(10) UNIQUE);
CREATE TABLE aa(bun INT, irum CHAR(10) CONSTRAINT aa_irum_uk UNIQUE(irum));	-- 상동
INSERT INTO aa VALUES(1, 'john');
INSERT INTO aa VALUES(2, 'tom');
INSERT INTO aa VALUES(3, 'tom'); 	-- unique err: 중복 불가

-- 참조키, 왜래키(foreign key, fk) 제약 조건 - Referential Integrity
-- 다른 테이블의 칼럼 값을 참조(fk의 대상은 다른 테이블의 pk 또는 uk)
-- 직원 테이블
CREATE TABLE jikwon(bun INT PRIMARY KEY, irum VARCHAR(10) NOT null, buser CHAR(10));
INSERT INTO jikwon VALUES(1, '한송이', '인사과');
INSERT INTO jikwon VALUES(2, '박치기', '인사과');
INSERT INTO jikwon VALUES(3, '한송이', '총무과');

SELECT * FROM jikwon

-- 가족 테이블
CREATE TABLE gajok(CODE INT PRIMARY KEY, NAME VARCHAR(10), birth DATETIME, jikwon_bun INT, FOREIGN KEY(jikwon_bun) REFERENCES jikwon(bun));
CREATE TABLE gajok(CODE INT PRIMARY KEY, NAME VARCHAR(10), birth DATETIME, jikwon_bun INT, FOREIGN KEY(jikwon_bun) REFERENCES jikwon(bun) ON DELETE RESTRICT ON UPDATE RESTRICT);	-- 상동
-- 부모 데이터를 자식이 참조하고 있으면 부모의 삭제나 키 변경을 막는다.

CREATE TABLE gajok(CODE INT PRIMARY KEY, NAME VARCHAR(10), birth DATETIME, jikwon_bun INT, FOREIGN KEY(jikwon_bun) REFERENCES jikwon(bun) ON DELETE CASCADE ON UPDATE SET NULL);
-- CASCADE: 부모 삭제 시 자식도 삭제
-- SET NULL: 부모 참조키 변경 시 자식의 fk 칼럼 값은 null이 됨
-- 대개의 경우 부모의 pk 는 변경이 흔하지 않으므로 set null은 자주 사용되지 않음
DESC gajok;
INSERT INTO gajok VALUES(10, '가나다', NOW(), 1);
INSERT INTO gajok VALUES(20, '이겨라', '2000-5-5', 2);
INSERT INTO gajok VALUES(30, '한국인', '2010-5-15', 1);
INSERT INTO gajok VALUES(40, '지구인', '2010-5-15', 5);	-- fk err: 5번 직원은 없음
SELECT * FROM gajok;

-- 직원 자료 삭제
DELETE FROM jikwon where bun = 3;
DELETE FROM jikwon where bun = 2;		-- err: 2번 직원의 가족이 있기 때문
DELETE FROM gajok where CODE = 20;	-- 2번 직원의 가족 삭제
DELETE FROM jikwon where bun = 2;		-- 성공: 가족이 없기 때문

DROP TABLE jikwon; 	-- err 테이블 삭제 불가 - 참조되고 있는 자식 테이블이 존재하기 때문
DROP TABLE gajok;
DROP TABLE jikwon;	-- 성공

SHOW TABLES;

-- default: 특정 칼럼에 초기값 부여 - null 방지 목적
CREATE TABLE aa(bun INT AUTO_INCREMENT PRIMARY KEY, irum CHAR(10), juso VARCHAR(50) DEFAULT '역삼동');		-- AUTO_INCREMENT: 자동 증가
-- oracle은 AUTO_INCREMENT X: SEQUENCE를 사용
DESC aa;

INSERT INTO aa(irum,juso) VALUES('길동', '서초동');
INSERT INTO aa(irum,juso) VALUES('나라', '익선동');
INSERT INTO aa(irum) VALUES('국가');
ALTER TABLE aa AUTO_INCREMENT=100;
INSERT INTO aa(irum,juso) VALUES('순신', '필동');
INSERT INTO aa(irum,juso) VALUES('철수', '대치동동');

SELECT * FROM aa;





