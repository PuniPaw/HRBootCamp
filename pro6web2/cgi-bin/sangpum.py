# cgi-bin/sangpum.py : 웹용 파이선 - MariaDB의 자료를 출력

# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding="utf-8") 

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

# 클라이언트 브라우저로 파이썬 처리 값 출력
print("Content-Type:text/html; charset=utf-8")
print("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>상품</title>
</head>
<body>
    <h2>* 상품 정보 *</h2>

</body>
</html>
"""
)

conn = None
try:
    conn = MySQLdb.connect(**config)
    cursor = conn.cursor()
    cursor.execute("""
        select code, sang, su, dan from sangdata
    """)

    datas = cursor.fetchall()
    print("""
    <table border="1">
        <tr>
            <td>코드</td>
            <td>품명</td>
            <td>수량</td>
            <td>단가</td>
        </tr>
        """)
    for data in datas:
        print(f"""
            <tr>
                <td>{data[0]}</td>
                <td>{data[1]}</td>
                <td>{data[2]}</td>
                <td>{data[3]}</td>
            </tr>
        """)
    print("""
    </table>
    """)
except Exception as e:
    print('err: ', e)
finally:
    if conn:
        conn.close()