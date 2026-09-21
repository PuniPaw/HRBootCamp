-- 저장 프로시저(Stored Procedure)
-- : 자주 사용하는 sql 작업을 db 안에 이름을 붙여 저장해 두고, 필요할 때 실행하는 기능
-- : sql + programming - 절차적 프로그래밍이 가능

-- 기본 형태 확인
-- 실습 1
delimiter $$
CREATE OR REPLACE PROCEDURE sp_1()
BEGIN
	SELECT '안녕 프로시저 세상 방문을 환영합니다'AS 제목;
END $$
delimiter ;

CALL sp_1();	-- procedure 호출
SHOW PROCEDURE STATUS;	-- PROCEDURE 목록 확인
SHOW CREATE PROCEDURE sp_1;	-- 해당 procedure 정보 확인
DROP PROCEDURE sp_1;	-- procedure 삭제

-- 실습 2
delimiter $$
CREATE OR REPLACE PROCEDURE sp_2(IN a INT, IN b INT)
BEGIN
	DECLARE x, y INT DEFAULT 0;	-- 변수 선언. 대소문자 구분 없음
	SET x = 10;	-- 변수에 값 대입
	SELECT X, Y;	-- 변수 출력
	SELECT a + b AS result;
	SELECT '안녕 프로시저 세상 방문을 환영합니다'AS 제목;
END $$
delimiter ;

CALL sp_2(2, 3);

-- 실습 3ㅣ table사용
delimiter $$
CREATE OR REPLACE PROCEDURE sp_3(IN para1 INT, IN b INT)
BEGIN
    -- para1: 최소 급여, b: 부서번호(busernum)
    SELECT jikwonno AS 사번,
           jikwonname AS 직원명,
           jikwonjik AS 직급,
           jikwonpay AS 급여,
           busernum AS 부서번호
    FROM jikwon
    WHERE jikwonpay >= para1
      AND busernum = b;
END $$
delimiter ;

CALL sp_3(3000, 20);

-- 실습 4ㅣ if 사용
delimiter $$
CREATE OR REPLACE PROCEDURE sp_4(IN jik VARCHAR(20), IN num INT)
BEGIN
	SELECT jik;
	SELECT * FROM jikwon WHERE jikwonjik=jik;
	if(num = 10) then
		SELECT * FROM jikwon WHERE busernum=num;
	ELSEIF(num=20) then
		SELECT * FROM jikwon WHERE busernum=num;
	else
		SELECT * FROM jikwon WHERE busernum NOT IN(10, 20);
	END if;
END $$
delimiter ;

CALL sp_4('대리', 20);

-- 실습 5ㅣ if 사용
-- 고객번호 입력하면 고객정보 조회
-- 담당 직원번호를 입력하면 해당 직원이 관리하는 고객 출력
-- 둘 다 입력 안하면 모든 고객 출력
delimiter $$
CREATE OR REPLACE PROCEDURE sp_5(IN p_gogekno INT, IN p_damsano INT)
BEGIN
	-- 특정 직원 조회
	if p_gogekno IS NOT NULL then
		SELECT * FROM gogek WHERE gogekno=p_gogekno;
	-- 담당 직원번호를 입력하면 해당 직원이 관리하는 고객 출력
	ELSEIF p_damsano IS NOT NULL then
		SELECT * FROM gogek WHERE gogekdamsano=p_damsano;
	-- 모든 고객 출력
	ELSE
		SELECT * FROM gogek;
	END if;
END $$
delimiter ;

CALL sp_5(5, NULL);	-- 고객번호 5번 조회
CALL sp_5(NULL, 3);	-- 담당직원번호가 3인 고객 조회
CALL sp_5(NULL, NULL);

-- 실습 6: while 사용
delimiter $$
CREATE OR REPLACE PROCEDURE sp_6()
BEGIN
	DECLARE n INT;
	DECLARE str VARCHAR(255);
	SET n = 1;
	SET str = '';
	
	while n <= 5 do
		SET str = CONCAT(str, n , ',');
		SET n = n+1;
	END while;
	
	SELECT str;
	
END $$
delimiter ;

CALL sp_6()

-- 실습 7: while 사용
-- 입력한 시작번호, 끝번호까지 고객자료 출력
delimiter $$
CREATE OR REPLACE PROCEDURE sp_7(IN start_no INT, IN end_no int)
BEGIN
	DECLARE current_no INT;
	SET current_no = start_no;
	
	while current_no <= end_no do
		SELECT * FROM gogek WHERE gogekno=current_no;
		SET current_no = current_no + 1;
	END while;
END $$
delimiter ;

CALL sp_7(3, 10)

-- 실습 8: while 사용
-- jikwon 테이블을 이용해 입력한 직급의 직원수와 직원 목록 출력
delimiter $$
CREATE OR REPLACE PROCEDURE sp_8(IN p_jik VARCHAR(20))
BEGIN
	DECLARE cnt INT DEFAULT 0;
	DECLARE i INT DEFAULT 0;
	-- 해당 직급의 직원수 저장
	SELECT COUNT(*) INTO cnt FROM jikwon WHERE jikwonjik=p_jik;
	
	SELECT p_jik AS 직급, cnt AS 인원수;
	-- 직원 목록 출력
	while i < cnt do
		SELECT jikwonno, jikwonname, jikwonjik, jikwonpay FROM jikwon
		WHERE jikwonjik=p_jik ORDER BY jikwonno LIMIT i, 1;
		SET i = i + 1;
	END while;
END $$
delimiter ;

CALL sp_8('대리')

SELECT ROUND(jikwonpay*0.05) FROM jikwon	-- 내장함수
-- 사용자 정의 함수
-- bmi 지수를 구하는 함수 - 신장(cm) * 신장(cm) * 22 / 10000
delimiter $$
CREATE OR REPLACE FUNCTION fu_1(IN height INT, weight INT) RETURNS DOUBLE
BEGIN
	RETURN weight * 10000 / height^2;
END $$
delimiter ;

SELECT fu_1(175, 70);

-- 사용자 정의 함수 2
-- 전체 직원의 연봉 평균 반환
delimiter $$
CREATE OR REPLACE FUNCTION fu_2() RETURNS DOUBLE
BEGIN
	DECLARE res DOUBLE;
	SELECT AVG(jikwonpay) INTO res FROM jikwon;
	RETURN res;
END $$
delimiter ;

SELECT fu_2();	-- 사용자 함수
SELECT AVG(jikwonpay) FROM jikwon;	-- 내장함수


-- 사용자 정의 함수 3
-- 각 직원 연봉의 10% 반환
delimiter $$
CREATE OR REPLACE FUNCTION fu_3(bun INT) RETURNS DOUBLE
BEGIN
	DECLARE pay INT;
	SET pay = 0;
	SELECT jikwonpay * 0.1 INTO pay FROM jikwon WHERE jikwonno = bun;
	RETURN pay;
END $$
delimiter ;

SELECT fu_3(1);
SELECT jikwonno,jikwonname,jikwonjik,fu_3(jikwonno) AS donate,jikwongen FROM jikwon;


-- 사용자 정의 함수 4
-- 부서 번호를 부서명으로
delimiter $$
CREATE OR REPLACE FUNCTION fu_4(bun INT) RETURNS VARCHAR(10)
BEGIN
	DECLARE bname VARCHAR(10);
	SELECT busername INTO bname FROM buser WHERE buserno = bun;
	RETURN bname;
END $$
delimiter ;

SELECT jikwonno,jikwonname,busernum, fu_4(busernum) FROM jikwon;

-- 문1) jikwon 테이블에 대한 부서번호가 있으면 부서명을, 없으면 '임시직'을 반환하는 함수

-- 문2) 고객번호를 입력하여 나이를 출력하는 함수