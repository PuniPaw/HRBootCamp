# pandas 문제 7)
 
#  b) MariaDB에 저장된 jikwon 테이블을 이용하여 아래의 문제에 답하시오.
#      - pivot_table을 사용하여 성별 연봉의 평균을 출력
#      - 성별(남, 여) 연봉의 평균으로 시각화 - 세로 막대 그래프
#      - 부서명, 성별로 교차 테이블을 작성 (crosstab(부서, 성별))
 

import pymysql
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
import csv
from sqlalchemy import create_engine

"""
config = {
    'host':'127.0.0.1',
    'user':'root',
    'password':'123',
    'database':'test',
    'port':3306,
    'charset':'utf8'
}
"""

conn = None

try:
    # 방법 1
    # conn = pymysql.connect(**config)
    # cursor = conn.cursor
    # - 사번 이름 부서명 성별 연봉을 읽어 DataFrame을 작성
    sql = """
        select jikwonno 사번,jikwonname 직원명,busername 부서명,jikwongen 성별,jikwonpay 연봉
        from jikwon inner join buser
        on jikwon.busernum = buser.buserno
    """
    # df = pd.read_sql(sql, conn)
    # print(df.head(3))

    # 방법 2
    engine = create_engine("mysql+pymysql://root:123@127.0.0.1:3306/test")
    df = pd.read_sql(sql, engine)
    print(df.head(3))

    # pivot_table을 사용하여 성별 연봉의 평균을 출력
    pt = pd.pivot_table(df, index='성별', values='연봉', aggfunc='mean')
    print('성별 연봉의 평균: \n',pt)
    print()

    # 성별(남, 여) 연봉의 평균으로 시각화 - 세로 막대 그래프(pandas 제공)
    pt.plot(kind='bar', legend=False, color=['steelblue','aqua'], rot=0)
    plt.title('성별 연봉의 평균')
    plt.xlabel('성별')
    plt.xlabel('연봉')
    plt.tight_layout()
    plt.show()

    # 부서명, 성별로 교차 테이블을 작성(crosstab(부서, 성별))
    ct = pd.crosstab(df['부서명'], df['성별'])
    print('부서명, 성별 교차 테이블: \n', ct)

except Exception as e:
    print('err: ', e)
finally:
    engine.dispose()