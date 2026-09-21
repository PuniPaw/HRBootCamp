# 원격 데이터베이스와 연동 프로그래밍
# MariaDB: 
# 준비 1) IP(네트워크에서 컴퓨터나 장치를 구분하기 위한 규약) 주소 필요.
# 준비 2) 연결용 Driver file 필요

# pip install mysqlclient

import MySQLdb

# DB 연결 방법 1
# conn = MySQLdb.connect(host='127.0.0.1', user='root', password='123', database='test', port=3306, charset='utf8') 

# DB 연결 방법 2
config_data = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "123",
    "database": "test",
    "port": 3306,
    "charset": "utf8"
}

conn = MySQLdb.connect(**config_data)

# DB 연결 방법 3
# json 파일 읽기
import json
with open("dbconnec.json", mode="r", encoding="utf-8") as f:
    config_data = json.load(f)

def myFunc():
    try:

        cursor = conn.cursor()    # SQL 처리를 위한 객체 생성. SQL 실행 담당

        # 자료 추가
        # isql = "insert into sangdata(code, sang, su, dan) values(5, '마스크', 5, 3000)"
        # cursor.execute(isql)
        """
        isql = "insert into sangdata values(%s, %s, %s, %s)"
        # ins_data = (6, '커피', 10, 5000)    # tuple type
        ins_data = 6, '커피', 10, 5000    # tuple type
        cursor.execute(isql, ins_data)
        conn.commit()   # 원격 db에 저장
        """

        # 자료 수정
        """
        usql = "update sangdata set sang=%s, su=%s, dan=%s where code=%s"
        # update_data = ('물티슈', 3, 1000, 5)
        update_data = '물티슈', 3, 1000, 5
        cursor.execute(usql, update_data)
        conn.commit()   # 원격 db에 저장
        """
        """
        usql = "update sangdata set sang=%s, su=%s, dan=%s where code=%s"
        up_date = '콜라', 11, 3000, 6
        # insert, update, delete 는 성공ㅇ하면 성공 갯수, 실패하면 0을 반환
        cou = cursor.execute(usql, up_date)
        print("성공 갯수:", cou)
        conn.commit()
        """

        # 자료 삭제
        code = '6'
        # dsql = "delete from sangdata where code=" + code
        # secure coding 가이드라인에 맞게 프로그래밍 해야 한다.
        # 해킹 위험: sql 인젝션은 사용자의 입력값을 검증하지 않는 웹 어플리케이션의 취약점을 이용하여 악의적인 SQL 문을 삽입하는 공격 기법이다.

        dsql = "delete from sangdata where code=%s"   # 추천 1: 권장
        cursor.execute(dsql, (code,))
        # dsql = "delete from sangdata where code='{}'".format(code)  # 추천2
        # cursor.execute(dsql)
        cou = cursor.execute(dsql, (code,)) # 삭제 후 반환 값 얻기
        if cou != 0:
            print("삭제 성공")
        else:
            print("삭제 실패")

        conn.commit()

        # 자료 읽기
        sql = "select * from sangdata"
        cursor.execute(sql)
        for data in cursor.fetchall():
            print(data)

        print()

        cursor.execute(sql)
        for data in cursor:
            print(data[0], data[1], data[2], data[3])

        print()
        cursor.execute(sql)
        for code, sang, su, dan in cursor:
            print(code, sang, su, dan)

        print()
        cursor.execute(sql)
        for a, b, 수량, 단가 in cursor:
            print(a, b, 수량, 단가)

    except Exception as e:
        print("Error:", e)
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    myFunc()