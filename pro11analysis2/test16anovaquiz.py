# [ANOVA 예제 1]
# 빵을 기름에 튀길 때 네 가지 기름의 종류에 따라 빵에 흡수된 기름의 양을 측정하였다.
# 기름의 종류에 따라 흡수하는 기름의 평균에 차이가 존재하는지를 분산분석을 통해 알아보자.
# 조건 : NaN이 들어 있는 행은 해당 칼럼의 평균값으로 대체하여 사용한다.
# 수집된 자료 :  
# kind quantity
# 1 64
# 2 72
# 3 68 
# 4 77 
# 2 56 
# 1 NaN 
# 3 95
# 4 78
# 2 55
# 1 91 
# 2 63
# 3 49
# 4 70
# 1 80
# 2 90 
# 1 33 
# 1 44 
# 3 55 
# 4 66
# 2 77
import pandas as pd 
import numpy as np 
import scipy.stats as stats 
from statsmodels.formula.api import ols 
from statsmodels.stats.anova import anova_lm 
import matplotlib.pyplot as plt 
import koreanize_matplotlib 

data = pd.DataFrame({
    'oil':[1,2,3,4,2,1,3,4,2,1,2,3,4,1,2,1,1,3,4,2],
    'L':[64,72,68,77,56,np.nan,95,78,55,91,63,49,70,80,90,33,44,55,66,77]
})
print(data.head(3),' ',len(data))
print('결측치 확인 : ', data.isnull().sum())  

# NaN을 해당 칼럼의 평균으로 대체 
print('L 평균 : ', data['L'].mean())  # 67.526315
data['L'] = data['L'].fillna(data['L'].mean())
print(data.describe())

# 기름 종류별 흡수량 자료, 평균 얻기  
gr1 = data[data['oil']==1]['L']
gr2 = data[data['oil']==2]['L']
gr3 = data[data['oil']==3]['L']
gr4 = data[data['oil']==4]['L']
print(np.mean(gr1),' ',np.mean(gr2),' ',np.mean(gr3),' ',np.mean(gr4))


print()
# 정규성 확인 
print(stats.shapiro(gr1).pvalue)  # 0.868040
print(stats.shapiro(gr2).pvalue)  # 0.592392
print(stats.shapiro(gr3).pvalue)  # 0.486010
print(stats.shapiro(gr4).pvalue)  # 0.416216
# 모두 0.05보다 크므로 정규성 만족 

print()
# 등분산성 확인 
print(stats.levene(gr1,gr2,gr3,gr4).pvalue)   # 0.326896
# print(stats.bartlett(gr1,gr2,gr3,gr4).pvalue) 
# 0.05보다 크므로 등분산성 만족 

# 일원분산분석 방법1 : anova_lm()
lmodel = ols('L ~ C(oil)', data=data).fit()
print(anova_lm(lmodel, type=1))


# 일원분산분석 방법2 : f_oneway()
f_stat, pv = stats.f_oneway(gr1,gr2,gr3,gr4)
print('f_stat : ', f_stat)  # 0.266935
print('p_value : ', pv)     # 0.848244

# 해석 : pvalue 0.848244 > alpha 0.05 이므로 귀무 채택 
# 기름의 종류에 따라 흡수하는 기름의 평균에 차이가 없다.

print()
# 정규성이 깨졌다면 stats.kruskal 검정 
print(stats.kruskal(gr1,gr2,gr3,gr4))  # pvalue=0.824237 동일하게 귀무 채택 

print('사후 검정')
from statsmodels.stats.multicomp import pairwise_tukeyhsd
tukResult = pairwise_tukeyhsd(endog=data['L'], groups=data['oil'])
print(tukResult)
# 모든 그룹 쌍의 reject가 False : 유의미한 차이가 있는 쌍이 없다.

# 시각화 
tukResult.plot_simultaneous(xlabel='흡수량 평균', ylabel='기름 종류')
plt.show()


# [ANOVA 예제 2]
# 
# DB에 저장된 buser와 jikwon 테이블을 이용하여 총무부, 영업부, 전산부, 관리부 직원의 연봉의 평균에 차이가 있는지 검정하시오. 만약에 연봉이 없는 직원이 있다면 작업에서 제외한다.