# 과적합(Overfitting)
# 선형 회귀 모델이 훈련 데이터(Training Data)에 너무 과하게 학습되어,
# 데이터에 포함된 노이즈(잡음)이나 지엽적인 특성까지 암기해버리는 현상.
# 훈련 데이터에 대한 예측 오차는 매우 낮지만, 처음 보는 테스트 데이터(Test Data)나
# 새로운 데이터가 들어왔을 때 예측 성능(일반화 능력)이 크게 떨어진다.

# Linear Regression에서 과적합을 해결하는 방법
# 특성(Feature)줄이기, 정규화(Regularization)적용, 더 많은 데이터 수집하기...

# 이 중에서 정규화 (Regularization) 적용하기 진행 ------
# 회귀계수 없이 값이 너무 커지지 않도록 비용 함수(Cost Function)에 페널티를 부과(규제)
# Ridge (L2 규제): 가중치들의 제곱합을 최소화하여 계수들을 0에 가깝게 작게 만든다.
# Lasso (L1 규제): 가중치들의 절대값 합을 최소화하여, 중요하지 않은 특성의 계수를 아에 0으로 
# ElasticNet(Ridge + Lasso)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet

iris = load_iris()
# print(iris)
print(iris.keys())  # ['data', 'target', 'frame', 'target_names', 'DESCR', 'feature_names', 'filename', 'data_module']

pd.set_option('display.max_columns', None)

iris_df = pd.DataFrame(iris.data, columns=iris.feature_names)
iris_df['target'] = iris.target
iris_df['target_names'] = iris.target_names[iris.target]
print(iris_df.head(2))
#    sepal length (cm)  sepal width (cm)  petal length (cm)  petal width (cm)  \
# 0                5.1               3.5                1.4               0.2   
# 1                4.9               3.0                1.4               0.2   

#    target target_names  
# 0       0       setosa  
# 1       0       setosa 
print(iris_df.shape)


# train(학습) / test(검증) 데이터로 분리    - 7:3
train_set, test_set = train_test_split(iris_df, test_size=0.3, random_state=12)
print(train_set.shape, test_set.shape)
print(train_set.head(3))
print(test_set.head(3))

print(train_set.iloc[:, [2]])   # petal length (cm), 독립변수
print(train_set.iloc[:, [3]])    # petal width (cm), 종속변수


# 회귀분석 방법 1 - LinearRegression
# 학습은 train dataset 사용
model_linear = LinearRegression().fit(X=train_set.iloc[:,[2]], y=train_set.iloc[:, [3]])
print('slope: ', model_linear.coef_)
print('bias: ', model_linear.intercept_)

# 모델 평가는 test dataset으로 작업
pred = model_linear.predict(test_set.iloc[:, [2]])
print('예측값: ', np.round(pred[:5].flatten(), 1))
print('실제값: ', test_set.iloc[:, [3]][:5].values.flatten())
# 예측값:  [0.2 1.7 0.2 1.3 2.1]
# 실제값:  [0.3 1.9 0.2 1.3 2.3]

print(f'r2_score(결정계수): {r2_score(test_set.iloc[:, [3]], pred)}')
# 시각화
plt.scatter(train_set.iloc[:,[2]], train_set.iloc[:,[3]], color='red')
plt.plot(np.array(test_set.iloc[:,[2]]), model_linear.predict(test_set.iloc[:,[2]]))
plt.show()

# 회귀분석 방법 2 - 정규화(규제) 모델 : Ridge / Lasso / ElasticNet ------
# 규제 효과를 보기 위해 독립변수를 3개로 늘림 (sepal length, sepal width, petal length) -> petal width 예측
# alpha : 규제 강도. 클수록 계수를 더 강하게 줄임 (alpha=0 이면 일반 LinearRegression과 같음)
x_train = train_set.iloc[:, [0, 1, 2]]
y_train = train_set.iloc[:, 3]
x_test = test_set.iloc[:, [0, 1, 2]]
y_test = test_set.iloc[:, 3]

models = {
    'Linear': LinearRegression(),
    'Ridge(L2)': Ridge(alpha=10),
    'Lasso(L1)': Lasso(alpha=0.1),
    'ElasticNet': ElasticNet(alpha=0.1, l1_ratio=0.5),   # l1_ratio: L1 비율 (0.5 -> L1:L2 = 5:5)
}

print('\n모델별 회귀계수 및 성능 비교')
coef_df = pd.DataFrame(index=x_train.columns)
for name, m in models.items():
    m.fit(x_train, y_train)
    pred = m.predict(x_test)
    coef_df[name] = m.coef_
    print(f'{name:12s} r2: {r2_score(y_test, pred):.4f}   mse: {mean_squared_error(y_test, pred):.4f}')
print(np.round(coef_df, 4))
# Linear       r2: 0.9331   mse: 0.0356
# Ridge(L2)    r2: 0.9432   mse: 0.0302
# Lasso(L1)    r2: 0.9407   mse: 0.0316
# ElasticNet   r2: 0.9415   mse: 0.0311
#                    Linear  Ridge(L2)  Lasso(L1)  ElasticNet
# sepal length (cm) -0.2666    -0.0390      0.000      0.0000
# sepal width (cm)   0.2524     0.0532      0.000      0.0000
# petal length (cm)  0.5578     0.4300      0.389      0.3991
# -> 규제 모델들이 test 성능이 조금 더 좋음 (과적합 완화)
# Lasso는 중요하지 않은 특성의 계수를 0으로 만들어 특성 선택 효과가 있음


# alpha 변화에 따른 계수 변화 확인 (Ridge vs Lasso)
alphas = [0.001, 0.01, 0.1, 1, 10, 100]
ridge_coefs, lasso_coefs = [], []
for a in alphas:
    ridge_coefs.append(Ridge(alpha=a).fit(x_train, y_train).coef_)
    lasso_coefs.append(Lasso(alpha=a).fit(x_train, y_train).coef_)

print('\nRidge alpha별 계수\n', pd.DataFrame(ridge_coefs, index=alphas, columns=x_train.columns).round(4))
print('\nLasso alpha별 계수\n', pd.DataFrame(lasso_coefs, index=alphas, columns=x_train.columns).round(4))
# Ridge : alpha가 커져도 계수가 0에 '가까워질' 뿐 정확히 0이 되지는 않음
#          sepal length  sepal width  petal length
# 0.001       -0.2666       0.2523       0.5577
# 1.000       -0.2176       0.2057       0.5312
# 10.000      -0.0390       0.0532       0.4300
# 100.000      0.0856      -0.0176       0.2915
# Lasso : alpha=0.1 부터 sepal 계수가 정확히 0 -> petal length만 남음 (특성 선택), alpha>=10 이면 전부 0
#          sepal length  sepal width  petal length
# 0.001       -0.2483       0.2336       0.5480
# 0.010       -0.0863       0.0661       0.4616
# 0.100        0.0000       0.0000       0.3890
# 1.000        0.0000       0.0000       0.0864
# 10.000       0.0000       0.0000       0.0000


# 시각화 : alpha가 커질수록 계수가 0으로 줄어드는 모습
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
for ax, coefs, title in zip(axes, [ridge_coefs, lasso_coefs], ['Ridge (L2)', 'Lasso (L1)']):
    ax.plot(alphas, coefs, marker='o')
    ax.set_xscale('log')
    ax.axhline(0, color='gray', linestyle='--')
    ax.set_title(title)
    ax.set_xlabel('alpha (log scale)')
    ax.set_ylabel('coefficient')
    ax.legend(x_train.columns)
    ax.grid(True)
plt.show()
