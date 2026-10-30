# 분산(Varience) 한 개의 변수가 평균으로부터 얼마나 흩어져 있는지
# 공분산(Covarience): 한 개의 변수가 함께 어떻게 변하는지
# 두 변수가 각각의 평균을 기준으로 함께 증가하거나 감소하는 경향이 있는지 나타내는 통계량
# 계산: 각 관측값이 평균보다 높은지 낮은지 비교하여 두 편차의 곱을 계산
# 변수가 두 개인 경우는 분산은 방향을 가짐

import numpy as np

# 공분산
print('변수1: ', np.arange(1, 6))
print('변수2: ', np.arange(2, 7))

print(np.cov(np.arange(1, 6, 1), np.arange(2, 7, 1)))   # 2.5 우상향
print(np.cov(np.arange(10, 60, 10), np.arange(20, 70, 10)))   # 250 우상향
print(np.cov(np.arange(100, 600, 100), np.arange(200, 700, 100)))   # 2500 우상향
print(np.cov(np.arange(1, 6, 1), (3, 3, 3, 3, 3)))   # 수평선(직선)
print(np.cov(np.arange(1, 6, 1), np.arange(6, 1, -1)))   # -2.5 우하향
# 두 변수 사이의 선형관계 방향은 알 수 있으나 강도를 알 수는 없다.

# 상관 계수: 공분산을 표준화한 값 -> 공분산을 두 변수의 표준편차곱으로 나눈 값
#         : 두 변수의 측정 단위나 크기에 상관없이 -1 ~ 1 사이의 값으로 표현 가능
x = [8, 3, 6, 6, 9, 4, 3, 9, 3, 4]
print('x 평균: ', np.mean(x))
print('x 분산: ', np.var(x))

y = [6, 2, 4, 6, 9, 5, 1, 8, 4, 5]
print('y 평균: ', np.mean(y))
print('y 분산: ', np.var(y))

import matplotlib.pyplot as plt
plt.plot(x, y, 'o')
plt.show()

print('x, y의 공분산: ', np.cov(x, y))
print('x, y의 공분산: ', np.cov(x, y)[0, 1])    # 5.222222222222222 두 변수는 양의 관계. 우상향

x2 = [80, 30, 60, 60, 90, 40, 30, 90, 30, 40]
y2 = [60, 20, 40, 60, 90, 50, 10, 80, 40, 50]
print('x2, y2의 공분산: ', np.cov(x2, y2)[0, 1])   # 522.2222222222222 두 변수는 양의 관계. 우상향
plt.plot(x2, y2, 'o')
plt.show()

print()
# 두 데이터의 단위에 따라 패턴이 일치할지라도 공분산의 크기가 달라지므로 절대적 크기 판단이 어렵다.
# 공분산을 표준화해서 -1 ~ 0 ~ 1 범위로 만든 것이 상관계수 (r)
print('x, y의 상관계수: ', np.corrcoef(x, y))
print('x, y의 상관계수: ', np.corrcoef(x, y)[0, 1])
print('x2, y2의 상관계수: ', np.corrcoef(x2, y2)[0, 1])
# 피어슨 상관 계수(Pearson correclation coefficient)는 두 연속형 변수 간의 선형
# 범위: -1 부터 1 사이의 값을 가짐
# +1: 완벽한 양의 선형 관계
# 0: 선형 상관관계 없음
# -1: 완벽한 음의 선형 관계

from scipy import stats
print('scipy 모듈 사용 r: ', stats.pearsonr(x, y))  
# print(stats.spearmanr(x, y))

print('-- 비선형 데이터인 경우 공분산, 상관계수는 의미 없다. --')
m = [-3, -2, -1, 0, 1, 2, 3]
n = [9, 4, 1, 0, 1, 4, 9]
plt.plot(m, n, 'o')
plt.show()
print(np.cov(m, n)[0, 1])
print(np.corrcoef(m, n)[0, 1])