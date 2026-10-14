# 고수준의 자료구조(Series, DataFrame)와 빠르고 쉬운 데이터 분석용 함수 제공
# 통합된 시계열 연산, 축약연산, 누락 데이터 처리, SQL, 시각화 ... 등을 제공
# 데이터 랭글링(Data Wrangling), 데이터 먼징(Data Munging)을 효율적으로 처리 가능

import numpy as np
import pandas as pd
from pandas import Series, DataFrame

# Series: 일련의 객체를 담을 수 있는 1차원 배열과 같은 자료구조로 색인(index)을 준다
obj = pd.Series([3, 7, -5, 4])  # (3, 7, -5, 4) -0, {3, 7, -5, 4} - X, dict
# obj = pd.Series([3, 7, , 4, '일'])    # 요소값 모두가 object type
print(obj, type(obj))

print()
obj2 = pd.Series([3, 7, -5, 4], index = ['a', 'b', 'c', 'd'])
print(obj2)
print(obj2.sum(), ' ', np.sum(obj2), ' ', sum(obj2))
print(obj2.std())   # 5.123475382979799 pandas의 함수는 numpy 기반

print(obj2.index)   # 색인만 출력
print(obj2.values)  # 값만 출력

# 인덱싱 / 슬라이싱
print(obj2['a'])    # 'a' 인덱스의 값: 3
print(obj2[['a']])  # a    3

print(obj2[['a', 'b']])     # a    3
                            # b    7

print(obj2['a':'c'])        # a    3
                            # b    7
                            # c   -5
print()
# print(obj2[2])    # KeyError: 인덱스 순서는 문자열을 사용 중
print(obj2.iloc[2]) # iloc[위치번호]: Series의 2번째 위치에 있는 값
print(obj2.loc['c'])# loc['인덱스 이름']

print()
print(obj2[1:4])
# print(obj2[2, 1])           # key = (2, 1) 튜플 → MultiIndex 전용이라 KeyError
print(obj2.iloc[[2, 1]])    # 위치 기반 팬시 인덱싱: c, b 순서로 출력
print(obj2[['c', 'b']])      # 라벨 기반 팬시 인덱싱: 위와 같은 결과

print()
print('a' in obj2)  # 인덱스에 'a' 여부 확인: True
print('k' in obj2)  # False

print('\n파이썬 dict 자료를 Series 객체로 생성')
names = {'mouse':5000, 'keyboard':35000, 'monitor':500000}
print(names, type(names))   # {'mouse': 5000, 'keyboard': 35000, 'monitor': 500000} <class 'dict'>

obj3 = Series(names)
print(obj3, type(obj3))     #mouse         5000
                            # keyboard     35000
                            # monitor     500000
                            # dtype: int64 <class 'pandas.Series'>

obj3.index = ['마우스', '키보드', '모니터']
print(obj3, type(obj3))     #마우스      5000
                            # 키보드     35000
                            # 모니터    500000
                            # dtype: int64 <class 'pandas.Series'>

obj3.name = '상품가격'
print(obj3)                 # 마우스      5000
                            # 키보드     35000
                            # 모니터    500000
                            # Name: 상품가격, dtype: int64

print('-------')
# DataFrame: 표 모양(2차원 형태 자료)의 자료 구조로 여러 개의 칼럼을 갖는다. (Series가 모인)
# 각 칼럼은 서로 다른 종류의 값을 기억할 수 있다.
# 같은 길이의 리스트에 담긴 dict type의 데이터를 이용해 DataFrame 객체

df = pd.DataFrame(obj3)
print(df, type(df))     # class 'pandas.DataFram'

print()
data = {
    'irum':['홍길동', '한국인', '신기해', '공기밥', '한가해'],
    'juso': ['역삼동', '신당동', '역삼동', '역삼동', '신사동'],
    'nai': [23, 25, 33, 30, 35]
}

frame = pd.DataFrame(data)  # dict -> DataFrame
print(frame)    #   irum juso  nai
                # 0  홍길동  역삼동   23
                # 1  한국인  신당동   25
                # 2  신기해  역삼동   33
                # 3  공기밥  역삼동   30
                # 4  한가해  신사동   35

print()
print(frame['irum'], type(frame['irum']))   # Name: irum, dtype: str <class 'pandas.Series'>
print(frame.irum, type(frame['irum']))      # Name: irum, dtype: str <class 'pandas.Series'>

print(DataFrame(data=data, columns=['juso', 'irum', 'nai'])) # 열(column) 순서 변경

# NaN (결측치)
frame2 = pd.DataFrame(data,
                    columns=['irum', 'nai', 'juso', 'tel'], index=['a', 'b', 'c', 'd', 'e'])
print(frame2)

val = pd.Series(['222-2222', '333-3333', '444-4444'], index=['b', 'c', 'd'])
print(val)

print()
frame2['tel'] = val     # 기존 자료 덮어쓰기
print(frame2)

print()
print(frame.T)      # 전치

print()
print(frame2.values, type(frame2.values))
print(frame2.values[0, 1])
print(frame2.values[0:2])

print()
# 삭제
frame3 = frame2.drop('d')   # 행 삭제
# frame3 = frame2.drop('d', axis=0)
print(frame3)

# frame4 = frame2.drop('tel') # 열 삭제
frame4 = frame2.drop('tel', axis=1)
print(frame4)

print('--------')
print(frame2)
print(frame2.sort_index(axis=0, ascending=False))   # 행 단위 정렬
print(frame2.sort_index(axis=1, ascending=True))    # 열 단위 정렬

print()
print(frame2.rank(axis=0))  # 순위 매김

counts = frame2['juso'].value_counts()
print(counts)

# 문자열 자르기
data = {
    'juso': ['서초구 서초2동', '강남구 역삼동', '강남구 대치동'],
    'inwon': [23, 25, 15]
}
fr = pd.DataFrame(data)
print(fr)

result1 = Series(x.split()[0] for x in fr.juso)
result2 = Series(x.split()[1] for x in fr.juso)
print(result1)
print(result2)
print(result1.value_counts())