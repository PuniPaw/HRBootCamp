-- 문1) 사번   이름    부서  직급  근무년수  고객확보
--         1   홍길동  영업부 사원     6           O   or  X
-- 조건 : 직급이 없으면 임시직, 전산부 자료는 제외
-- 위의 결과를 위한 뷰파일 v_exam1을 작성

CREATE VIEW v_exam1 AS
SELECT j.jikwonno   AS 사번,
       j.jikwonname AS 이름,
       b.busername  AS 부서,
       IFNULL(j.jikwonjik, '임시직') AS 직급,
       TIMESTAMPDIFF(YEAR, j.jikwonibsail, CURDATE()) AS 근무년수,
       CASE 
           WHEN EXISTS (SELECT 1 FROM gogek g WHERE g.gogekdamsano = j.jikwonno) 
           THEN 'O' 
           ELSE 'X' 
       END AS 고객확보
FROM jikwon j
JOIN buser b ON j.busernum = b.buserno
WHERE b.busername != '전산부';

SELECT * FROM v_exam1;

-- 문2) 부서명   인원수
--        영업부     7
-- 조건 : 직원수가 가장 많은 부서 출력
-- 위의 결과를 위한 뷰파일 v_exam2을 작성
 
CREATE VIEW v_exam2 AS
SELECT b.busername AS 부서명,
       COUNT(j.jikwonno) AS 인원수
FROM buser b
JOIN jikwon j ON j.busernum = b.buserno
GROUP BY b.busername
ORDER BY 인원수 DESC
LIMIT 1;

SELECT * FROM v_exam2;

-- 문3) 가장 많은 직원이 입사한 요일에 입사한 직원 출력
--     직원명   요일     부서명   부서전화
--     한국인  수요일   전산부   222-2222
-- 위의 결과를 위한 뷰파일 v_exam3을 작성  

CREATE VIEW v_exam3 AS
SELECT j.jikwonname AS 직원명,
		 CASE DAYOFWEEK(j.jikwonibsail)
           WHEN 1 THEN '일요일'
           WHEN 2 THEN '월요일'
           WHEN 3 THEN '화요일'
           WHEN 4 THEN '수요일'
           WHEN 5 THEN '목요일'
           WHEN 6 THEN '금요일'
           WHEN 7 THEN '토요일'
       END AS 요일,
		 b.busername AS 부서명,
       b.busertel AS 부서전화
FROM jikwon j
JOIN buser b ON j.busernum = b.buserno
WHERE DAYOFWEEK(j.jikwonibsail) = (
    SELECT DAYOFWEEK(jikwonibsail)
    FROM jikwon
    GROUP BY DAYOFWEEK(jikwonibsail)
    ORDER BY COUNT(*) DESC
    LIMIT 1
);
SELECT * FROM v_exam3;
