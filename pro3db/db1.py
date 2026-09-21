# SQLite: 개인용 db, python 에 기본 내장, 경량 dbms
# 서버를 운영하지 않아 시스템 내에서 별도의 자원을 사용할 필요가 없고, 설치가 필요 없으며, 단일 파일로 구성되어 있어 배포가 용이하다.

import sqlite3

print("SQLite3 version:", sqlite3.sqlite_version)
print()

# conn = sqlite3.connect("exam.db")  # 파일에 데이터 보관
conn = sqlite3.connect(":memory:")  # ram에서만 작업. 휘발성

try:
    cur = conn.cursor()    # SQL 처리를 위한 객체 생성. SQL 실행 담당

    # 테이블 생성
    cur.execute("create table if not exists friends(name text, phone text, addr text)")  # 테이블 생성

    # 데이터 삽입
    cur.execute("insert into friends values('홍길동', '010-1111-1111', '서울시')")
    cur.execute("insert into friends values(?,?,?)", ('이기자', '111-2222','서초2동'))

    inputdatas = ('신기해', '010-3333-3333', '강남구')
    cur.execute("insert into friends values(?,?,?)", inputdatas)

    inputdats2 = (('신기한', '010-4444-4444', '강남구'), ('신기한2', '010-5555-5555', '강남구'))
    cur.executemany("insert into friends values(?,?,?)", inputdats2)
    conn.commit()

    # 자료 조회
    cur.execute("select * from friends")
    # print(cur.fetchone())  # 한 건만 가져오기
    # print(cur.fetchmany(2))  # 여러 건 가져오기
    print(cur.fetchall())  # 전체 가져오기
    print()
    cur.execute("select name,addr,phone from friends")
    for row in cur.fetchall():
        print(row)
        print(row[0] + '님의 주소는 ' + row[1] + '이고, 전화번호는 ' + row[2] + '입니다.')


except Exception as e:
    print("Error:", e)
finally:
    conn.close()
