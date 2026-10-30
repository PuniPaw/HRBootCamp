# 이원분산분석(two-way ANOVA)  ---------------------------

# 독립변인의 수가 두 개 이상일 때 집단 간 차이가 유의한지를 검증하는 데 사용한다. 

# 상호작용효과(Interaction effect) : 한 변수의 변화가 결과에 미치는 영향이 다른 변수의 수준에 따라 달라지는지를 확인하기 위해 사용된다.

# - 두 개의 요인에 대한 집단(독립변수) 각각이 종속변수(평균)에 영향을 주는지 검정
# - 주효과(개별효과) : 독립변수들이 각각 독립적으로 종속변수에 미치는 영향을 검정하는 것
# - 상호작용효과(교호작용) : 독립변수들이 서로 연관되어 종속변수에 미치는 영향을 검정하는 것
#                                          한 독립변수가 종속변수에 미치는 영향이 다른 독립변수의 수준에 따라 달라지는 현상

# 쉬운 예시 (약물과 음료):
# 약(A): 감기약을 먹으면 증상이 완화됩니다.
# 음료(B): 물을 마시는 것은 건강에 문제가 없습니다.
# 교호작용 발생: 감기약을 '물'과 먹으면 효과가 좋지만 '술'과 먹으면 치명적이다.
# 즉, 약의 효과가 함께 복용한 음료의 종류에 따라 완전히 달라진다.

# 실습: 독의 종류와 처치 방법에 따라 실험동물의 평균 생존시간에 차이가 있는가 검증

from scipy import stats
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns
from statsmodels.formula.api import ols 
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.multicomp import pairwise_tukeyhsd

data = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/poison_treat.csv', index_col=0)
# 첫 번째 열은(index 0)을 DataFrame의 인덱스로 사용

print(data.head(3))
print(data.shape)
# 데이터 설명
# - poison : 독의 종류 (3개 수준)
# - treat  : 처치방법 (4개 수준)
# - time   : 독에 노출된 실험동물의 생존시간
#
# 독 3종류 × 처치방법 4종류 = 12개 조합
# 각 조합에서 실험동물 4마리 관측 → 총 48개 자료
# 독이 퍼지는 시간이 아니라 '생존시간'을 분석함

# [주효과 가설 1 : 독의 종류]
# 귀무(H0) : 독의 종류에 따른 평균 생존시간은 모두 같다.
# 대립(H1) : 독의 종류에 따른 평균 생존시간 중 적어도 하나는 다르다.

# [주효과 가설 2 : 처치방법]
# 귀무(H0) : 처치방법에 따른 평균 생존시간은 모두 같다.
# 대립(H1) : 처치방법에 따른 평균 생존시간 중 적어도 하나는 다르다.

# [교호작용 가설]
# 귀무(H0) : 독의 종류와 처치방법 간 교호작용은 없다.
# 대립(H1) : 독의 종류와 처치방법 간 교호작용은 있다.
# 교호작용이 있다는 의미: 처치방법에 따른 생존시간 차이가 독의 종류에 따라 달라짐

# 주효과: 각각의 독립변수에 따라 종속변수의 평균이 달라지는가?
# 교호작용: 한 독립변수에 따른 평균 차이가 다른 독립변수의 수준에 따라 달라지는가?
print('독 종류별 표본 수: ', data.groupby('poison').size())
print('처치 방법별 표본 수: ', data.groupby('treat').size())
print('독 종류 * 처치 방법별 표본 수: ', data.groupby(['poison', 'treat']).size())
# 모든 조합에서 표본 수가 4로 동일함. 균형설계됨.

print('\n요인별 기술 통계')
print('독 종류별 생존 시간: ', data.groupby('poison')['time'].agg(['count','mean','std']))
print('처치 방법별 생존 시간: ', data.groupby('treat')['time'].agg(['count','mean','std']))

# 이원분산분석 ---------
model = ols('time ~ C(poison) * C(treat)', data=data).fit()    #     * : 주효과 + 교호작용 분석
result = anova_lm(model, type=2)
print('\n이원분산분석:\n', result)
# 이원분산분석:
#                        df    sum_sq   mean_sq          F        PR(>F)
# C(poison)            2.0  1.033013  0.516506  23.221737  3.331440e-07
# C(treat)             3.0  0.921206  0.307069  13.805582  3.777331e-06
# C(poison):C(treat)   6.0  0.250137  0.041690   1.874333  1.122506e-01
# Residual            36.0  0.800725  0.022242        NaN           NaN

# 해석
p_poison = result.loc['C(poison)' 'PR(>F)']
p_treat = result.loc['C(treat)' 'PR(>F)']
p_interaction = result.loc['C(poison):C(treat)', 'PR(>F)']
alpha = 0.05

if p_poison < alpha:
    print('독 종류: 귀무 기각 - 독의 종류에 따라 평균 생존 시간에 유의한 차이가 있다.')
else:
    print('독 종류: 귀무 채택 - 우연히 발생한 데이터')

if p_treat < alpha:
    print('처치 방법: 귀무 기각 - 처치 방법에 따라 평균 생존 시간에 유이한 차이가 있다.')
else:
    print('처치 방법: 귀무 채택 - 우연히 발생한 데이터.')

if p_interaction < alpha:
    print('교호 작용: 귀무 기각 - 처치 방법의 효과는 독의 종류에 따라 다르다.')
else:
    print('교호 작용: 귀무 채택 - 처치 방법의 효과는 독의 종류에 따라 다르다는 주장의 근거가 부족하다.')

# 사후 검정(Post-hoc test)
print('\n독 종류별 사후 검정')
tkResult1 = pairwise_tukeyhsd(endog=data['time'], groups=['posion'], alpha=alpha)
print(tkResult1)

tkResult1.plot_simultaneous(xlabel='평균생존시간', ylabel='독 종류')
plt.title('독의 종류별 생존 시간')
plt.show()
plt.close()

print('\n처치 방법 별 사후 검정')
tkResult2 = pairwise_tukeyhsd(endog=data['time'], groups=['treat'], alpha=alpha)
print(tkResult2)

tkResult2.plot_simultaneous(xlabel='평균생존시간', ylabel='처치 방법')
plt.title('독의 종류별 생존 시간')
plt.show()
plt.close()