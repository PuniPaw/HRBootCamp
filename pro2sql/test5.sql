-- 주석
-- C(insert), R(select), U(update), D(delete) 잠깐 연습 

-- 테이블 생성
CREATE TABLE good(no INT PRIMARY key, name VARCHAR(10) NOT NULL, tel VARCHAR(10),
inwon INT, addr TEXT);

DESC good;

-- 자료 추가
-- 형식 : insert into 테이블명(칼럼명 타입, ...) values(자료,...)
INSERT INTO good(no, name, tel, inwon, addr) VALUES(1, '인사과', '123-1234', 5, '삼성1동');
INSERT INTO good VALUES(2, '영업과', '123-2222', 12, '역삼2동');
INSERT INTO good(no, name, inwon) VALUES('3','자재과','7');
INSERT INTO good(addr, no, name, inwon) VALUES('역삼3동','4','자재2과','7');

SELECT * FROM good;

-- 오류인 경우
INSERT INTO good(no, NAME) VALUES(3, '자재3과');   -- no(PRIMARY key) 중복 에러
INSERT INTO good(no, tel) VALUES(5, '자재3과');    -- name은 not null : 반드시 입력
INSERT INTO good(NAME, no) VALUES(5, '자재3과');   -- 입력자료와 칼럼의 수서가 불일치
INSERT INTO good(no, NAME) VALUES('오', '자재3과'); -- 입력자료 타입 불일치
INSERT INTO good(no, NAME) VALUES(5, '우리회사에서 가장 매출이 좋은 부러운 부서');  -- 입력자료 크기 오류


-- 자료 수정
-- 형식 : update 테이블명 set 칼럼명=수정값, ... where 조건
UPDATE good SET inwon=100 WHERE NO=1;
UPDATE good SET inwon=70, tel='777-7777' WHERE NO=2;
UPDATE good SET inwon=2, tel=null WHERE NO=2;

SELECT * FROM good;

-- 오류인 경우
UPDATE good SET name=null WHERE NO=2;   -- name은 not null : 반드시 입력
UPDATE good SET NO=2 WHERE NO=1;        -- no 중복 오류


-- 자료 삭제
-- 형식 : delete from 테이블명 where 조건  - 부분적으로 행 삭제
DELETE FROM good WHERE NO=2;
SELECT * FROM good;

-- 형식2 : truncate table 테이블명   - where 조건 없음. 행 모두 삭제. 구조만 남음
truncate TABLE good;
SELECT * FROM good;


DROP TABLE good;   -- 테이블 삭제

SHOW TABLES;


-- -----------------------
-- 데이터베이스 무결성(Database Integrity)은 저장된 데이터가 정확하고 일관되며, 
-- 손상되지 않고 신뢰할 수 있는 상태를 유지하는 것을 뜻합니다.  
-- 잘못된 자료 입력 장지를 위한 제약 조건 부여.
-- 데이터의 품질을 지키고 오류를 막기 위해 데이터베이스 관리 시스템(DBMS)이 지키는 핵심 규칙.

-- 주요 무결성 제약조건
--  - 개체 무결성 (Entity Integrity): 모든 테이블은 기본 키(Primary Key)를 가져야 합니다. 
--    기본 키는 빈 값(NULL)이나 중복 값을 가질 수 없습니다.
--  - 도메인 무결성 (Domain Integrity): 필드에 들어가는 값이 지정된 자료형, 범위, 조건(Check 등)에 맞아야 합니다.
--  - 사용자 정의 무결성 (User-Defined Integrity): 업무 규칙에 맞게 사용자가 직접 만든 조건이나 트리거(Trigger)로 데이터를 제한합니다.
--  - 참조 무결성 (Referential Integrity): 테이블 간의 관계를 뜻합니다. 
--    외래 키(Foreign KEY) 값은 참조하는 테이블의 기본 키와 일치하거나 빈 값이어야 합니다.
 
--  무결성이 중요한 이유중복 데이터나 
--   - 잘못된 입력 값을 막습니다.
--   - 부모와 자식 데이터의 연결이 끊어지지 않게 돕습니다.
--   - 시스템 오류를 줄이고 데이터 신뢰도를 높입니다.

-- 기본키(primary key, pk) 제약 조건 - Entity Integrity
-- 기본 키는 빈 값(NULL)이나 중복 값을 가질 수 없다. 자동으로 인덱스가 생성됨.

-- 참고 : 테이블 작성시 칼럼의 이름, 타입은 중요. 순서는 마음대로. 
--        계산에 의해 처리될 수있는 값은 칼럼으로 작성X   
--        예) 국어, 영어 따위는 칼럼으로 작성. 총점, 평균은 칼럼으로 작성X

-- 방법1) 칼럼 레벨
CREATE TABLE aa(bun INT PRIMARY KEY, irum CHAR(10));
DESC aa;
INSERT INTO aa VALUES(1,'tom');
INSERT INTO aa VALUES(2,'tom');
INSERT INTO aa VALUES(2,'tom');      -- pk err : 중복 불가
INSERT INTO aa(irum) VALUES('tom');  -- pk err : not null
SELECT * FROM aa;

-- 제약 조건 확인
SELECT * FROM information_schema.TABLE_CONSTRAINTS WHERE TABLE_NAME='aa';

DROP TABLE aa;

-- 방법2) 테이블 레벨
CREATE TABLE aa(bun INT, irum CHAR(10), CONSTRAINT aa_bun_pk PRIMARY KEY(bun)); -- oracle용
DESC aa;
SELECT * FROM information_schema.TABLE_CONSTRAINTS WHERE TABLE_NAME='aa';

alter TABLE aa DROP CONSTRAINT aa_bun_pk;   -- pk 제약조건 삭제. oracle에서 유효
alter TABLE aa DROP PRIMARY KEY;            -- pk 제약조건 삭제
DROP TABLE aa;


-- check 제약 조건 - Domain Integrity : 입력 값 조건 부여
CREATE TABLE aa(bun INT, irum CHAR(10), nai INT CHECK(nai >= 20));
SELECT * FROM information_schema.TABLE_CONSTRAINTS WHERE TABLE_NAME='aa';
INSERT INTO aa VALUES(1,'tom', 25);
INSERT INTO aa VALUES(2,'tom', 15);    -- chk err : nai 조건 불만족

ALTER TABLE aa ADD constraint ck_name CHECK(irum IN('tom','john'));  -- check 조건 추가
INSERT INTO aa VALUES(2,'john', 25);
INSERT INTO aa VALUES(3,'james', 25);  -- chk err : irum 조건 불만족
SELECT * FROM aa;

DROP TABLE aa;


-- unique 제약 조건 - Domain Integrity : 동일값 입력 불허
CREATE TABLE aa(bun INT, irum CHAR(10) UNIQUE);  
CREATE TABLE aa(bun INT, irum CHAR(10), CONSTRAINT aa_irum_uk UNIQUE(irum));  -- 얘도 가능
INSERT INTO aa VALUES(1,'john');
INSERT INTO aa VALUES(2,'tom');
INSERT INTO aa VALUES(3,'tom');    -- unique err : 중복 불가
DROP TABLE aa;


-- Referential Integrity(참조키, foreign key, fk, 외래키)  제약 조건
-- 다른 테이블의 칼럼값을 참조 (fk의 대상은 다른 테이블의 pk 또는 unique 가능)
-- 직원 테이블
CREATE TABLE jikwon(bun INT PRIMARY KEY, irum VARCHAR(10) NOT NULL, buser CHAR(10));
INSERT INTO jikwon VALUES(1, '한송이','인사과');
INSERT INTO jikwon VALUES(2, '박치기','인사과');
INSERT INTO jikwon VALUES(3, '한송이','총무과');
SELECT * FROM jikwon;

-- 가족 테이블
CREATE TABLE gajok(CODE INT PRIMARY KEY, NAME VARCHAR(10), birth DATETIME, jikwon_bun INT,
FOREIGN KEY(jikwon_bun) REFERENCES jikwon(bun));

CREATE TABLE gajok(CODE INT PRIMARY KEY, NAME VARCHAR(10), birth DATETIME, jikwon_bun INT,
FOREIGN KEY(jikwon_bun) REFERENCES jikwon(bun) ON DELETE RESTRICT ON UPDATE RESTRICT);  -- 위와 동일
-- 부모 데이터를 자식이 참조하고 있으면 부모의 삭제나 키 변경을 막는다.

CREATE TABLE gajok(CODE INT PRIMARY KEY, NAME VARCHAR(10), birth DATETIME, jikwon_bun INT,
FOREIGN KEY(jikwon_bun) REFERENCES jikwon(bun) ON DELETE CASCADE ON UPDATE SET NULL); 
-- CASCADE : 부모 삭제시 자식도 삭제
-- SET NULL : 부모 참조키 변경시 자식의 FK 칼럼 값은 null이됨
-- 대개의 경우 부모의 pk는 변경이 흔하지 않으므로 SET NULL은 자주 사용되지 않는다.

DESC gajok;
INSERT INTO gajok VALUES(10, '가나다', NOW(), 1);
INSERT INTO gajok VALUES(20, '이겨라', '2000-5-5', 2);
INSERT INTO gajok VALUES(30, '한국인', '2010-5-15', 1);
SELECT * FROM gajok;

INSERT INTO gajok VALUES(40, '지구인', '2010-5-15', 5);  -- fk err : 5번 직원없음

-- 직원 자료 삭제
DELETE FROM jikwon WHERE bun = 3;
DELETE FROM jikwon WHERE bun = 2;   -- err : 2번직원의 가족이 있기 때문
DELETE FROM gajok WHERE CODE = 20;  -- 2번직원의 가족 삭제
DELETE FROM jikwon WHERE bun = 2;   -- 성공 : 가족이 없기 때문

SELECT * FROM jikwon;

DROP TABLE jikwon;   -- err 테이블 삭제 불가 - 참조되고 있는 자식 테이블 때문
DROP TABLE gajok;
DROP TABLE jikwon;   -- 성공

SHOW TABLES;


-- default : 특정 칼럼에 초기값 부여 - null 방지 목적
CREATE TABLE aa(bun INT AUTO_INCREMENT PRIMARY KEY, irum CHAR(10), 
juso VARCHAR(50) DEFAULT '역삼동');   
-- AUTO_INCREMENT :번호 자동 증가
-- Oracle은 AUTO_INCREMENT X : SEQUENCE를 사용
DESC aa;

INSERT INTO aa(irum,juso) VALUES('길동','서초동');  -- AUTO_INCREMENT 초기값 1
INSERT INTO aa(irum,juso) VALUES('나라','익선동');
INSERT INTO aa(irum) VALUES('국가');  -- juso는 DEFAULT 값으로 채움

ALTER TABLE aa AUTO_INCREMENT=100;    -- AUTO_INCREMENT 값 변경
INSERT INTO aa(irum,juso) VALUES('순신','필동');
INSERT INTO aa(irum,juso) VALUES('철수','대치동');
SELECT * FROM aa;

DROP TABLE aa;


-- 연습문제
CREATE TABLE 교수(교수코드 INT PRIMARY KEY, 교수명 VARCHAR(20) NOT null, 
연구실 INT CHECK(연구실 BETWEEN 100 AND 500));
DESC 교수;

CREATE TABLE 과목(과목코드 INT AUTO_INCREMENT PRIMARY KEY, 
과목명 VARCHAR(20) UNIQUE, 교재명 VARCHAR(20), 담당교수 INT, 
FOREIGN KEY(담당교수) REFERENCES 교수(교수코드));
DESC 과목;

CREATE TABLE 학생(학번 INT PRIMARY KEY, 학생명 VARCHAR(20) NOT null, 수강과목 INT, 
학년 INT DEFAULT 1 CHECK(학년 IN (1,2,3,4)), FOREIGN KEY(수강과목) REFERENCES 과목(과목코드));
DESC 과목;

-- 실행 예시
INSERT INTO 교수 VALUES(1,'홍길동', 100);
INSERT INTO 교수 VALUES(2,'고길동', 110);
INSERT INTO 교수 VALUES(3,'홍길동', 120);
SELECT * FROM 교수;

INSERT INTO 과목(과목명,교재명,담당교수) VALUES('SQL','SQL의 이해',1);
INSERT INTO 과목(과목명,교재명,담당교수) VALUES('파이썬','실무 파이썬',2);
INSERT INTO 과목(과목명,교재명,담당교수) VALUES('파이썬2','실무 파이썬2',7);  -- fk err
INSERT INTO 과목(과목명,교재명,담당교수) VALUES('파이썬','실무 파이썬2',2);   -- unique err
SELECT * FROM 과목;

INSERT INTO 학생 VALUES('1111', '한국인', 1, 1);
INSERT INTO 학생 VALUES('1112', '한송이', 2, 3);
INSERT INTO 학생 VALUES('1113', '한송이', 20, 3);   -- fk err
INSERT INTO 학생 VALUES('1113', '한송이', 2, 6);    -- check err

SELECT * FROM 학생;

DELETE FROM 교수 WHERE 교수코드= 1;   -- err : 자식이 참조
DELETE FROM 과목 WHERE 과목코드= 1;   -- err : 자식이 참조
DELETE FROM 학생 WHERE 학번= 1111;    -- 삭제 성공
DELETE FROM 과목 WHERE 과목코드= 1;   -- 삭제 성공
DELETE FROM 교수 WHERE 교수코드= 1;   -- 삭제 성공

SELECT * FROM 교수;

DROP TABLE 교수;  -- err : 자식이 참조
DROP TABLE 과목;  -- err : 자식이 참조
DROP TABLE 학생;  -- 테이블 삭제 성공
DROP TABLE 과목;  -- 테이블 삭제 성공
DROP TABLE 교수;  -- 테이블 삭제 성공

SHOW TABLES;


-- 인덱스(index) : 쉽게 말하면 책의 목차나 색인과 비슷하다. 건색 속도 향상이 목표
-- 인덱스 없음 → 처음부터 끝까지 데이터를 확인
-- 인덱스 있음 → 위치를 빠르게 찾아서 데이터 접근

CREATE TABLE aa (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(20), 
age INT, city VARCHAR(30));

INSERT INTO aa(name, age, city) VALUES
('홍길동', 25, '서울'),
('김철수', 30, '부산'),
('이영희', 27, '서울'),
('박민수', 35, '대전'),
('최영희', 23, '인천'),
('강호동', 40, '서울'),
('유재석', 38, '부산'),
('신동엽', 42, '서울'),
('홍길동', 29, '수원'),
('김민지', 31, '대구');

SELECT * FROM aa;

SELECT * FROM aa WHERE NAME='강호동';  -- 인덱스가 없으므로 전체 테이블 검색. 속도 느림

-- 실행 계획 확인
explain SELECT * FROM aa WHERE NAME='강호동';  -- type : ALL - Full Table Scan

-- 검색을 자주하는 name에 인덱스 생성 - 인덱스 테이블 별도 생성
CREATE INDEX idx_aa_name ON aa(name);  -- 이미 테이블이 있는 경우
SHOW INDEX FROM aa;  -- idx_aa_name와 pk(인덱스 자동생성) 인덱스 확인 가능
SHOW KEYS FROM aa;   -- 이 것도 가능

-- 테이블 생성시 인덱스 부여
CREATE TABLE aa (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(20), 
age INT, city VARCHAR(30), INDEX idx_aa_name (name));

-- 참고 : 인덱스가 여러 개인 경우 '옵티마이저'가 적당한 인덱스를 선택해 실행

DESC aa;

-- idx_aa_name 테이블 생성
-- 강호동 -> 위치(pointer - pk값) pk가 없으면 내부적으로 ROW id를 만듦
-- 이영희 -> 위치

-- index 삭제
DROP INDEX idx_aa_name ON aa;
SHOW INDEX FROM aa;

-- index는 특정 칼럼의  검색 속도 증진이 목적이나 단점도 있다.
-- insert, update, delete 등이 빈번한 경우에는 인덱스 재설정 비용이 든다.

DROP TABLE aa;


-- 참고 : 내장함수 now(), sysdate()의 차이
SELECT NOW(), SLEEP(2), NOW();          -- 결과가 같다.
SELECT SYSDATE(), SLEEP(2), SYSDATE();  -- 결과가 다르다.
-- SYSDATE()는 동일 SQL 문장 내에서 호출되는 시점에 따라 결과값을 바로 반환


-- 테이블 관련 명령
-- create table 테이블명 ~   생성 
-- alter table 테이블명 ~    구조를 수정
-- drop table 테이블명 ~     삭제

CREATE TABLE aa(irum CHAR(10), juso VARCHAR(50));
ALTER TABLE aa RENAME kbs;   -- 테이블 이름 변경
SELECT * FROM aa;    -- X
SELECT * FROM kbs;   -- O
ALTER TABLE kbs RENAME aa;

-- 칼럼 관련 명령
ALTER TABLE aa ADD (job_id INT DEFAULT 10);  -- 칼럼 추가
DESC aa;
INSERT INTO aa VALUES('tom', 'seoul', 20);
INSERT INTO aa(irum, juso) VALUES('tom2', 'jeju');
SELECT * FROM aa;

ALTER TABLE aa CHANGE job_id job_number INT;  -- 칼럼명 변경
SELECT * FROM aa;
DESC aa;

ALTER TABLE aa MODIFY job_number VARCHAR(10); -- 칼럼 타입 변경
DESC aa;

ALTER TABLE aa DROP COLUMN job_number;   -- 칼럼 삭제
DESC aa;
SELECT * FROM aa;

DROP TABLE aa;



-- 본격 실습 ---------------------------------------
create table sangdata(code int primary key,sang varchar(20),su int,dan INT);
insert into sangdata values(1,'장갑',3,10000);
insert into sangdata values(2,'벙어리장갑',2,12000);
insert into sangdata values(3,'가죽장갑',10,50000);
insert into sangdata values(4,'가죽점퍼',5,650000);
select * from sangdata;

create table buser(
buserno int primary key, 
busername varchar(10) not null,
buserloc varchar(10),
busertel varchar(15));

insert into buser values(10,'총무부','서울','02-100-1111');
insert into buser values(20,'영업부','서울','02-100-2222');
insert into buser values(30,'전산부','서울','02-100-3333');
insert into buser values(40,'관리부','인천','032-200-4444');
select * from buser;

create table jikwon(
jikwonno int primary key,
jikwonname varchar(10) not null,
busernum int not null,
jikwonjik varchar(10) default '사원', 
jikwonpay int,
jikwonibsail date,
jikwongen varchar(4),
jikwonrating char(3),
CONSTRAINT ck_jikwongen check(jikwongen='남' or jikwongen='여'));

insert into jikwon values(1,'홍길동',10,'이사',9900,'2008-09-01','남','a');
insert into jikwon values(2,'한송이',20,'부장',8800,'2010-01-03','여','b');
insert into jikwon values(3,'이순신',20,'과장',7900,'2010-03-03','남','b');
insert into jikwon values(4,'이미라',30,'대리',4500,'2014-01-04','여','b');
insert into jikwon values(5,'이순라',20,'사원',3000,'2017-08-05','여','b');
insert into jikwon values(6,'김이화',20,'사원',2950,'2019-08-05','여','c');
insert into jikwon values(7,'김부만',40,'부장',8600,'2009-01-05','남','a');
insert into jikwon values(8,'김기만',20,'과장',7800,'2011-01-03','남','a');
insert into jikwon values(9,'채송화',30,'대리',5000,'2013-03-02','여','a');
insert into jikwon values(10,'박치기',10,'사원',3700,'2016-11-02','남','a');
insert into jikwon values(11,'김부해',30,'사원',3900,'2016-03-06','남','a');
insert into jikwon values(12,'박별나',40,'과장',7200,'2011-03-05','여','b');
insert into jikwon values(13,'박명화',10,'대리',4900,'2013-05-11','남','a');
insert into jikwon values(14,'박궁화',40,'사원',3400,'2016-01-15','여','b');
insert into jikwon values(15,'채미리',20,'사원',4000,'2016-11-03','여','a');
insert into jikwon values(16,'이유가',20,'사원',3000,'2016-02-01','여','c');
insert into jikwon values(17,'한국인',10,'부장',8000,'2006-01-13','남','c');
insert into jikwon values(18,'이순기',30,'과장',7800,'2011-11-03','남','a');
insert into jikwon values(19,'이유라',30,'대리',5500,'2014-03-04','여','a');
insert into jikwon values(20,'김유라',20,'사원',2900,'2019-12-05','여','b');
insert into jikwon values(21,'장비',20,'사원',2950,'2019-08-05','남','b');
insert into jikwon values(22,'김기욱',40,'대리',5850,'2013-02-05','남','a');
insert into jikwon values(23,'김기만',30,'과장',6600,'2015-01-09','남','a');
insert into jikwon values(24,'유비',20,'대리',4500,'2014-03-02','남','b');
insert into jikwon values(25,'박혁기',10,'사원',3800,'2016-11-02','남','a');
insert into jikwon values(26,'김나라',10,'사원',3500,'2016-06-06','남','b');
insert into jikwon values(27,'박하나',20,'과장',5900,'2012-06-05','여','c');
insert into jikwon values(28,'박명화',20,'대리',5200,'2013-06-01','여','a');
insert into jikwon values(29,'박가희',10,'사원',4100,'2016-08-05','여','a');
insert into jikwon values(30,'최미숙',30,'사원',4000,'2015-08-03','여','b');
select * from jikwon;

create table gogek(
gogekno int primary key,
gogekname varchar(10) not null,
gogektel varchar(20),
gogekjumin char(14),
gogekdamsano int,
CONSTRAINT FK_gogekdamsano foreign key(gogekdamsano) references jikwon(jikwonno));

insert into gogek values(1,'이나라','02-535-2580','850612-1156777',5);
insert into gogek values(2,'김혜순','02-375-6946','700101-1054777',3);
insert into gogek values(3,'최부자','02-692-8926','890305-1065777',3);
insert into gogek values(4,'김해자','032-393-6277','770412-2028777',13);
insert into gogek values(5,'차일호','02-294-2946','790509-1062777',2);
insert into gogek values(6,'박상운','032-631-1204','790623-1023777',6);
insert into gogek values(7,'이분','02-546-2372','880323-2558777',2);
insert into gogek values(8,'신영래','031-948-0283','790908-1063777',5);
insert into gogek values(9,'장도리','02-496-1204','870206-2063777',4);
insert into gogek values(10,'강나루','032-341-2867','780301-1070777',12);
insert into gogek values(11,'이영희','02-195-1764','810103-2070777',3);
insert into gogek values(12,'이소리','02-296-1066','810609-2046777',9);
insert into gogek values(13,'배용중','02-691-7692','820920-1052777',1);
insert into gogek values(14,'김현주','031-167-1884','800128-2062777',11);
insert into gogek values(15,'송운하','02-887-9344','830301-2013777',2);
select * from gogek;

SELECT * FROM sangdata;

DESC buser;
DESC jikwon;
DESC gogek;


-- select 출발
-- SELECT [DISTINCT] db명.소유자명.테이블명.칼럼명 [AS 별명]... [INTO 테이블명 ]
-- FROM 테이블명 ...
-- WHERE 조건 ...
-- ORDER BY 기준키 ASC[DESC]

-- select 조회방법
-- 행단위 조회 : selection

-- 열단위 조회 : projection
DESC jikwon;
SELECT * FROM jikwon;   -- 모든 행, 열 읽기
SELECT jikwonno,jikwonname,jikwonpay FROM jikwon;  -- 일부 칼럼만 읽기
SELECT jikwonpay,jikwonno,jikwonname FROM jikwon;  -- 칼럼 순서 동적으로 읽기
SELECT jikwonno AS 사번,jikwonname 직원명,jikwonno '연 봉' FROM jikwon;  -- 칼럼에 별명 부여

SELECT 10,'안녕',12 / 3 AS result FROM DUAL;   -- DUAL : 가상의 테이블
SELECT 10,'안녕',12 / 3 AS result;

SELECT jikwonname AS 직원명,jikwonpay AS 연봉,jikwonpay * 0.02 AS 세금 FROM jikwon;  -- 칼럼 연산 가능
SELECT concat(jikwonname,'님') AS 이름, jikwongen AS 성별 FROM jikwon;   -- 문자열 더하기

SELECT test.jikwon.jikwonname FROM jikwon;
SELECT myjik.jikwonname FROM jikwon AS myjik;   -- 테이블에 별명을 주고 별명.칼럼명 가능

-- 정렬(sort) - 그룹별 작업이 가능해짐
SELECT * FROM jikwon ORDER BY jikwonpay ASC;   -- jikwonpay별 오름차순 정렬
SELECT * FROM jikwon ORDER BY jikwonpay;
SELECT jikwonno,jikwonname,jikwongen FROM jikwon ORDER BY jikwongen;
SELECT jikwonno,jikwonname,jikwongen FROM jikwon ORDER BY jikwongen desc;
SELECT * FROM jikwon ORDER BY busernum ASC,jikwonjik DESC,jikwonpay ASC;
SELECT jikwonname,jikwonpay / 100 * 100 AS pay FROM jikwon ORDER BY pay DESC;  -- 연산결과에 대한 절렬도 가능


