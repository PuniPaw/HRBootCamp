# 보스턴 주택 가격
# 1978년에 발표된 데이터로 미국 보스턴 지역의 주택 가격에 영향을 미치는 요소들을 정리함 

# CRIM - per capita crime rate by town
# ZN - proportion of residential land zoned for lots over 25,000 sq.ft.
# INDUS - proportion of non-retail business acres per town.
# CHAS - Charles River dummy variable (1 if tract bounds river; 0 otherwise)
# NOX - nitric oxides concentration (parts per 10 million)
# RM - average number of rooms per dwelling
# AGE - proportion of owner-occupied units built prior to 1940
# DIS - weighted distances to five Boston employment centres
# RAD - index of accessibility to radial highways
# TAX - full-value property-tax rate per $10,000
# PTRATIO - pupil-teacher ratio by town
# B - 1000(Bk - 0.63)^2 where Bk is the proportion of blacks by town
# LSTAT - % lower status of the population
# MEDV - Median value of owner-occupied homes in $1000's

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures


pd.set_option('display.max_columns', None)

df = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/housing.data', header=None, sep=r'\s+')
df.columns = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT', 'MEDV']
print(df.head(2))
print(df.corr())
# LSTAT   -0.496996  0.488676  0.543993  0.374044 -0.366087  1.000000 -0.737663  (저소득층 인구)
# MEDV     0.249929 -0.381626 -0.468536 -0.507787  0.333461 -0.737663  1.000000  (주택 가격)

x = df[['LSTAT']].values
y = df['MEDV'].values
print(x[:3])
print(y[:3])

# 단항을 통한 단순선형회귀 모델
model = LinearRegression()

# 다항 특성(변수)
quad = PolynomialFeatures(degree=2)
cubic = PolynomialFeatures(degree=3)
x_quad = quad.fit_transform(x)
x_cubic = cubic.fit_transform(x)
print(x_quad[:3])
print(x_cubic[:3])

# 단순회귀
model.fit(x, y)
x_fit = np.arange(x.min(), x.max(), 1)[:, np.newaxis]
y_lin_fit = model.predict(x_fit)    # 그래프에 표시용
print('y_lin_fit: ', y_lin_fit)
model_r2 = r2_score(y, model.predict(x))
print('model_r2: ', model_r2)   # 0.5441462975864797

# 다항(2차)
model.fit(x_quad, y)
y_quad_fit = model.predict(quad.fit_transform(x_fit))
q_r2 = r2_score(y, model.predict(x_quad))
print('q_r2: ', q_r2)       # 0.6407168971636612 - model_r2보다 10% 정도 증가함


# 다항(3차)
model.fit(x_cubic, y)
y_cubix_fit = model.predict(cubic.fit_transform(x_fit))
c_r2 = r2_score(y, model.predict(x_cubic))
print('c_r2: ', c_r2)       # 0.6578476405895719


# 시각화
plt.scatter(x, y, label='초기 데이터')
plt.plot(x_fit, y_lin_fit, linestyle=':', label='linear fit(d=1), $R^2=%.2f$'%model_r2, lw=3, c='b')
plt.plot(x_fit, y_quad_fit, linestyle='-', label='quad fit(d=2), $R^2=%.2f$'%q_r2, lw=3, c='r')
plt.plot(x_fit, y_cubix_fit, linestyle='--', label='cubix fit(d=3), $R^2=%.2f$'%c_r2, lw=3, c='k')
plt.xlabel('하위계층비율')
plt.ylabel('주택가격')
plt.legend()
plt.show()