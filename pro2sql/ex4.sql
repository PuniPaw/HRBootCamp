-- JOIN 연습2 ---------------

-- 문1) 총무부에서 관리하는 고객수 출력 (고객 30살 이상만 작업에 참여)

SELECT COUNT(gogek.gogekno) AS 고객수수
FROM gogek
JOIN jikwon ON gogek.gogekdamsano = jikwon.jikwonno
JOIN buser ON jikwon.busernum = buser.buserno
WHERE buser.busername = '총무부'
  AND SUBSTR(gogek.gogekjumin, 1, 2) <= '96';

-- 문2) 부서명별 고객 인원수 (부서가 없으면 "무소속")
 
SELECT IFNULL(busername, '무소속') AS 부서,
	COUNT(gogek.gogekno) AS 고객수
FROM gogek
LEFT JOIN jikwon ON gogek.gogekdamsano = jikwon.jikwonno
LEFT JOIN buser ON jikwon.busernum = buser.buserno
GROUP BY IFNULL(buser.busername, '무소속');

-- 문3) 고객이 담당직원의 자료를 보고 싶을 때 즉, 고객명을 입력하면  담당직원 자료 출력  
--         :    ~ WHERE GOGEK_NAME='강나루'
-- 출력 ==>  직원명    직급   부서명  부서전화    성별

SELECT jikwon.jikwonname AS 직원명,
		 jikwon.jikwonjik AS 직급,
		 buser.busername AS 부서명
FROM jikwon
JOIN buser ON jikwon.busernum = buser.buserno
JOIN gogek ON gogek.gogekdamsano = jikwon.jikwonno
WHERE gogek.gogekname = '강나루' 

-- 문4) 부서와 직원명을 입력하면 관리고객 자료 출력
--         ~ WHERE BUSER_NAME='영업부' AND JIKWON_NAME='이순신'
-- 	출력 ==>  고객명    고객전화      성별
--              강나루   123-4567       남

 
SELECT gogek.gogekname AS 고객명,
		 gogek.gogektel AS 고객전화,
		 CASE 
          WHEN SUBSTRING(gogek.gogekjumin, 8, 1) IN ('1', '3') THEN '남'
          WHEN SUBSTRING(gogek.gogekjumin, 8, 1) IN ('2', '4') THEN '여'
       END AS 성별
FROM gogek
JOIN jikwon ON gogek.gogekdamsano = jikwon.jikwonno
JOIN buser ON buser.buserno = jikwon.busernum
WHERE buser.busername='영업부' AND jikwon.jikwonname='이순신'


-- 문5) 담당 고객이 한 명도 없는 직원 찾기

SELECT jikwon.jikwonname AS 직원명
FROM jikwon
LEFT JOIN gogek ON gogek.gogekdamsano = jikwon.jikwonno
WHERE gogek.gogekno IS NULL;

-- 문6) buser, jikwon, gogek 세 테이블을 이용하여 부서명, 직원명, 직급, 담당 고객 수를 출력하시오.
-- 단, 담당 고객이 없는 직원도 출력하고 담당 고객 수가 많은 직원부터 정렬하시오.

SELECT buser.busername AS 부서명,
       jikwon.jikwonname AS 직원명,
       jikwon.jikwonjik AS 직급,
       COUNT(gogek.gogekno) AS '담당 고객 수'
FROM jikwon
LEFT JOIN gogek ON gogek.gogekdamsano = jikwon.jikwonno
LEFT JOIN buser ON jikwon.busernum = buser.buserno
GROUP BY buser.busername, jikwon.jikwonname, jikwon.jikwonjik
ORDER BY COUNT(gogek.gogekno) DESC;
