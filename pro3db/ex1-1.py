# 문1-1) 직원번호와 직원명을 입력(로그인)하여 성공하면 아래의 내용 출력
# 해당 직원이 근무하는 부서 내의 직원 전부를 직급별 오름차순우로 출력. 직급이 같으면 이름별 오름차순한다.

# 직원번호 입력 : _______
# 직원명 입력 : _______
# 직원번호 직원명 부서명 부서전화 직급 성별
# 1 홍길동 총무부 111-1111 이사 남
# ...
# 직원 수 :
 
# 이어서 로그인한 해당 직원이 관리하는 고객 자료도 출력한다.
# 고객번호 고객명 고객전화 나이
# 1 사오정 555-5555 34
# 관리 고객 수 :

import MySQLdb
from dotenv import load_dotenv
import os

load_dotenv()

config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT")),
    "charset": os.getenv("DB_CHARSET")
}

def LoginFunc():
    conn = None
    try:
        conn = MySQLdb.connect(**config)
        cursor = conn.cursor()
        jikwon_no = input("직원번호를 입력하세요: ")
        jikwon_name = input("직원명을 입력하세요: ")
        if jikwon_no == "" or jikwon_name == "":
            print("직원번호와 직원명을 모두 입력해야 합니다.")
            return

        sql = """
        select j.jikwonno as 직원번호,
                j.jikwonname as 직원명,
                b.busername as 부서명,
                b.busertel as 부서전화,
                j.jikwonjik as 직급,
                j.jikwongen as 성별,
                j.busernum as 부서번호
                from jikwon j left outer join buser b on j.busernum = b.buserno
                where j.jikwonno = %s and j.jikwonname = %s
        """

        cursor.execute(sql, (jikwon_no, jikwon_name))
        data = cursor.fetchone()

        if not data:
            print("로그인 실패: 직원번호 또는 직원명이 올바르지 않습니다.")
            return

        print("로그인 성공")
        print("직원번호:", data[0])
        print("직원명:", data[1])
        print("부서명:", data[2])
        print("부서전화:", data[3])
        print("직급:", data[4])
        print("성별:", data[5])

        busernum = data[6]

        # 같은 부서 직원 전체 조회: 직급 오름차순, 같으면 이름 오름차순
        sql2 = """
        select j.jikwonno as 직원번호,
                j.jikwonname as 직원명,
                j.jikwonjik as 직급,
                j.jikwongen as 성별
                from jikwon j
                where j.busernum = %s
                order by j.jikwonjik asc, j.jikwonname asc
        """
        cursor.execute(sql2, (busernum,))
        rows = cursor.fetchall()

        print("\n=== 같은 부서 직원 목록 ===")
        print(f"직원 수:{len(rows)}")
        for row in rows:
            print(f"직원번호:{row[0]}  직원명:{row[1]}  직급:{row[2]}  성별:{row[3]}")

        # 관리 고객 수 조회
        sql3 = """
        select  g.gogekno as 고객번호,
                g.gogekname as 고객명,
                g.gogektel as 고객전화,
                YEAR(CURDATE()) - (
                    CASE
                        WHEN SUBSTRING(g.gogekjumin, 8, 1) IN ('1', '2') 
                            THEN 1900 + SUBSTRING(g.gogekjumin, 1, 2)
                        WHEN SUBSTRING(g.gogekjumin, 8, 1) IN ('3', '4') 
                            THEN 2000 + SUBSTRING(g.gogekjumin, 1, 2)
                    END
                ) AS 나이
                from gogek g
                where g.gogekdamsano = %s
        """

        cursor.execute(sql3, (jikwon_no,))
        rows = cursor.fetchall()
        print(f"\n=== 관리 고객 수 ===")
        print(f"관리 고객 수:{len(rows)}")
        for row in rows:
            print(f"고객번호:{row[0]}  고객명:{row[1]}  고객전화:{row[2]}  나이:{row[3]:.0f}")

    except Exception as e:
        print("Error:", e)
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    LoginFunc()