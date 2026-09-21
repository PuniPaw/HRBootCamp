-- 문1) 직급별 급여의 평균 (NULL인 직급 제외)

SELECT jikwonjik AS 직급, AVG(jikwonpay) AS 평균값 FROM jikwon GROUP BY jikwonjik;

-- 문2) 부장,과장에 대해 직급별 급여의 총합

SELECT jikwonjik AS 직급, SUM(jikwonpay) AS 총합 FROM jikwon WHERE jikwonjik IN ('부장', '과장') GROUP BY jikwonjik;

-- 문3) 2015년 이전에 입사한 자료 중 년도별 직원수 출력

SELECT YEAR(jikwonibsail) AS 입사연도, COUNT(*) AS 직원수 FROM jikwon WHERE jikwonibsail < '2015-01-01' GROUP BY YEAR(jikwonibsail);

-- 문4) 직급별 성별 인원수, 급여합 출력 (NULL인 직급은 임시직으로 표현)

SELECT IFNULL(jikwonjik, '임시직') AS 직급, 
COUNT(CASE WHEN jikwongen = '남' THEN 1 END) AS 남자, 
COUNT(CASE WHEN jikwongen = '여' THEN 1 END) AS 여자, 
SUM(jikwonpay) AS 급여합 FROM jikwon GROUP BY IFNULL(jikwonjik, '임시직');

-- 문5) 부서번호 10,20에 대한 부서별 급여 합 출력

SELECT busernum AS 부서번호, SUM(jikwonpay) AS '급여 합' FROM jikwon WHERE busernum IN(10, 20) GROUP BY busernum;

-- 문6) 급여의 총합이 7000 이상인 직급 출력(NULL인 직급은 임시직으로 표현)

SELECT IFNULL(jikwonjik, '임시직') AS 직급, SUM(jikwonpay) AS '급여 총합' FROM jikwon GROUP BY IFNULL(jikwonjik, '임시직') HAVING SUM(jikwonpay) >= 7000;

-- 문7) 직급별 인원수, 급여합계를 구하되 인원수가 3명 이상인 직급만 출력(NULL인 직급은 임시직으로 표현)

SELECT IFNULL(jikwonjik, '임시직') AS 직급, SUM(jikwonpay) AS 급여합계, COUNT(*) AS 인원수 FROM jikwon GROUP BY IFNULL(jikwonjik, '임시직') HAVING COUNT(jikwonjik) >= 3;


