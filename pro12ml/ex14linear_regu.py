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
from sklearn.metrics import mean_squared_error

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
