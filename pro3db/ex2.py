# 문2) 성별 직원 현황 출력 : 성별(남/여) 단위로 직원 수와 평균 급여 출력

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

        sql = """
        select j.jikwongen as 성별,
                count(*) as 직원수,
                avg(j.jikwonpay) as 평균급여
                from jikwon j
                group by j.jikwongen
                order by j.jikwongen asc
        """

        cursor.execute(sql)
        rows = cursor.fetchall()

        print("=== 성별 직원 현황 ===")
        for row in rows:
            print(f"성별:{row[0]}  직원수:{row[1]}명  평균급여:{row[2]:.0f}")

    except Exception as e:
        print("Error:", e)
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    LoginFunc()