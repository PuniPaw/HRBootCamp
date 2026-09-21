-- 문1) 2010년 이후에 입사한 남자 중 급여를 가장 많이 받는 직원은?

SELECT jikwonname AS 직원명, 
       jikwonpay AS 급여, 
       jikwonibsail AS 입사일
FROM jikwon
WHERE jikwonibsail >= '2010-01-01'
  AND jikwongen = '남'
ORDER BY jikwonpay DESC
LIMIT 1;

-- 문2)  평균급여보다 급여를 많이 받는 직원은?

SELECT jikwonname AS 직원명,
		 jikwonpay AS 급여
FROM jikwon
WHERE jikwonpay > (SELECT AVG(jikwonpay) FROM jikwon);

-- 문3) '이미라' 직원의 입사 이후에 입사한 직원은?

SELECT jikwonname AS 직원명,
       jikwonibsail AS 입사일
FROM jikwon
WHERE jikwonibsail > (SELECT jikwonibsail FROM jikwon WHERE jikwonname = '이미라');

-- 문4) 2010 ~ 2015년 사이에 입사한 총무부(10),영업부(20),전산부(30) 직원 중 급여가 가장 적은 사람은?
-- (직급이 NULL인 자료는 작업에서 제외)

SELECT jikwon.jikwonname AS 직원명, 
       buser.busername AS 부서명, 
       jikwon.jikwonpay AS 급여
FROM jikwon
JOIN buser ON jikwon.busernum = buser.buserno
WHERE jikwon.jikwonibsail BETWEEN '2010-01-01' AND '2015-12-31'
  AND jikwon.busernum IN (10, 20, 30)
  AND jikwon.jikwonjik IS NOT NULL
ORDER BY jikwon.jikwonpay ASC
LIMIT 1;
 

-- 문5) 한송이, 이순신과 직급이 같은 사람은 누구인가?

SELECT jikwonname AS 직원명, 
       jikwonjik AS 직급
FROM jikwon
WHERE jikwonjik IN (
    SELECT jikwonjik 
    FROM jikwon 
    WHERE jikwonname IN ('한송이', '이순신')
);

-- 문6) 과장 중에서 최대급여, 최소급여를 받는 사람은?

SELECT jikwonname AS 직원명, 
       jikwonjik AS 직급, 
       jikwonpay AS 급여
FROM jikwon
WHERE jikwonjik = '과장'
  AND jikwonpay IN (
      (SELECT MAX(jikwonpay) FROM jikwon WHERE jikwonjik = '과장'),
      (SELECT MIN(jikwonpay) FROM jikwon WHERE jikwonjik = '과장')
  );

-- 문7) 30번 부서의 평균급여보다 급여가 많은 '대리' 는 몇명인가?

SELECT COUNT(*) AS 인원수
FROM jikwon
WHERE jikwonjik = '대리'
  AND jikwonpay > (
      SELECT AVG(jikwonpay) 
      FROM jikwon 
      WHERE busernum = 30
  );

-- 문8) 고객을 확보하고 있는 직원들의 이름, 직급, 부서명을 입사일 별로 출력하라.

SELECT DISTINCT jikwon.jikwonname AS 직원명, 
                jikwon.jikwonjik AS 직급, 
                buser.busername AS 부서명
FROM jikwon
JOIN buser ON jikwon.busernum = buser.buserno
JOIN gogek ON jikwon.jikwonno = gogek.gogekdamsano
ORDER BY jikwon.jikwonibsail ASC;

-- 문9) 이순신과 같은 부서에 근무하는 직원과 해당 직원이 관리하는 고객 출력
-- (고객은 나이가 30 이하면 '청년', 50 이하면 '중년', 그 외는 '노년'으로 표시하고, 고객 연장자 부터 출력)
-- 출력 ==>  직원명    부서명     부서전화     직급      고객명    고객전화    고객구분
--           한송이    총무부     123-1111    사원      백송이    333-3333    청년   

SELECT 
    직원명, 부서명, 부서전화, 직급, 고객명, 고객전화,
    CASE 
        WHEN 나이 <= 30 THEN '청년'
        WHEN 나이 <= 50 THEN '중년'
        ELSE '노년'
    END AS 고객구분
FROM (
    SELECT 
        jikwon.jikwonname AS 직원명, 
        buser.busername AS 부서명, 
        buser.busertel AS 부서전화, 
        jikwon.jikwonjik AS 직급, 
        gogek.gogekname AS 고객명, 
        gogek.gogektel AS 고객전화,
        YEAR(CURDATE()) - (
            CASE
                WHEN SUBSTRING(gogek.gogekjumin, 8, 1) IN ('1', '2') 
                    THEN 1900 + SUBSTRING(gogek.gogekjumin, 1, 2)
                WHEN SUBSTRING(gogek.gogekjumin, 8, 1) IN ('3', '4') 
                    THEN 2000 + SUBSTRING(gogek.gogekjumin, 1, 2)
            END
        ) AS 나이
    FROM jikwon
    JOIN buser ON jikwon.busernum = buser.buserno
    JOIN gogek ON jikwon.jikwonno = gogek.gogekdamsano
    WHERE jikwon.busernum = (
        SELECT busernum FROM jikwon WHERE jikwonname = '이순신'
    )
) AS sub
ORDER BY 나이 DESC;

-- 문10) JIKWON, BUSER, GOGEK 테이블을 이용하여 담당 고객 수가 가장 많은 직원을 출력하시오.
-- 동일한 고객 수를 가진 직원이 여러 명이면 모두 출력한다.
-- 출력 ==>   부서명   직원명   직급   담당고객수

SELECT buser.busername AS 부서명, 
       jikwon.jikwonname AS 직원명, 
       jikwon.jikwonjik AS 직급, 
       COUNT(gogek.gogekno) AS 담당고객수
FROM jikwon
JOIN buser ON jikwon.busernum = buser.buserno
JOIN gogek ON jikwon.jikwonno = gogek.gogekdamsano
GROUP BY jikwon.jikwonno, buser.busername, jikwon.jikwonname, jikwon.jikwonjik
HAVING COUNT(gogek.gogekno) = (
    SELECT MAX(customer_cnt) 
    FROM (
        SELECT COUNT(g2.gogekno) AS customer_cnt 
        FROM gogek g2 
        GROUP BY g2.gogekdamsano
    ) AS sub_table
);

-- 힌트 :  GROUP BY ~ HAVING 사용
-- 직원별 고객 수 계산 --> 그중 가장 큰 고객 수 계산 --> 그 고객 수를 가진 직원 찾기