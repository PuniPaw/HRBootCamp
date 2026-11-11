# iris dataset으로 실습
# KNN (K-Nearest Neighbors)

import pandas as pd
import numpy as np
from sklearn.datasets import load_iris

iris = load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df['target'] = iris.target
print(df.head(2))
print(df.info())
print(iris.target_names)    # ['setosa' 'versicolor' 'virginica']

# iris는 결측치와 범주형 feature가 없어서 전처리가 필요 없음
x = df.drop('target', axis=1)   # feature
y = df['target']                # label(class) : 0, 1, 2

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=42, stratify=y
)

print('분류 모델 생성 ---')
from sklearn.linear_model import Perceptron
model = Perceptron(max_iter=1000, eta0=0.1, random_state=0)
print(model)

model.fit(x_train, y_train)

# 분류 예측
y_pred = model.predict(x_test)
print('예측값: ', y_pred)
print('실제값: ', y_test.values)
print(f'총 갯수: {len(y_test)}, 오류수: {(y_test != y_pred).sum()}')

# 평가
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
print('분류 정확도: ', accuracy_score(y_test, y_pred))
print('confusion_matrix: \n', confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred, target_names=iris.target_names))

print()     # 교차 검증
from sklearn.model_selection import cross_val_score
scores = cross_val_score(model, x, y, cv=5)
print(f'교차 검증에서 각 fold:{scores}, 평균: {scores.mean()}')

print()     # 최적의 k 찾기 - k 값에 따른 교차 검증 평균 정확도 비교
k_range = range(1, 21)
k_scores = [cross_val_score(KNeighborsClassifier(n_neighbors=k), x, y, cv=5).mean()
            for k in k_range]
best_k = k_range[int(np.argmax(k_scores))]
print('최적의 k: ', best_k, ' 정확도: ', max(k_scores))

import matplotlib.pyplot as plt
import koreanize_matplotlib
plt.figure()
plt.plot(k_range, k_scores, marker='o')
plt.xlabel('k (n_neighbors)')
plt.ylabel('교차 검증 평균 정확도')
plt.xticks(k_range)
plt.grid(True)
plt.show()

print('새로운 자료에 대한 예측')
newdata = pd.DataFrame([{
    'sepal length (cm)': 6.1,
    'sepal width (cm)': 2.8,
    'petal length (cm)': 4.7,
    'petal width (cm)': 1.2,
}])
newpred = model.predict(newdata)
print('예측결과: ', iris.target_names[newpred[0]])
print('확률은 ', np.round(model.predict_proba(newdata), 4))   # 이웃 5개 중 각 클래스 비율

# 새 데이터와 가장 가까운 이웃 5개 확인
dist, idx = model.kneighbors(newdata)
print('가까운 이웃의 거리: ', np.round(dist, 3))
print('가까운 이웃의 클래스: ', iris.target_names[y_train.iloc[idx[0]].values])