# iris dataset으로 실습
# Naive Bayes

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

# NaiveBayes 모델 학습 - feature가 연속형이므로 GaussianNB
from sklearn.naive_bayes import GaussianNB
model = GaussianNB()
model.fit(x_train, y_train)

# 예측 및 평가
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
pred = model.predict(x_test)
print('분류 정확도: ', accuracy_score(y_test, pred))
print('confusion_matrix: \n', confusion_matrix(y_test, pred))
print(classification_report(y_test, pred, target_names=iris.target_names))

print()     # 교차 검증
from sklearn.model_selection import cross_val_score
scores = cross_val_score(model, x, y, cv=5)
print(f'교차 검증에서 각 fold:{scores}, 평균: {scores.mean()}')

print()     # feature 중요도 분석 - feature가 정규분포를 따른다는 가정하에 클래스별 평균
# GaussianNB의 theta_ : 클래스별 feature 평균, shape = (클래스 수 3, feature 수 4)
class_mean = pd.DataFrame(model.theta_, index=iris.target_names, columns=x.columns)
print('클래스별 feature 평균')
print(class_mean)

# 클래스가 3개이므로 '최대 평균 - 최소 평균'으로 클래스 간 차이를 측정
importance = model.theta_.max(axis=0) - model.theta_.min(axis=0)

feat_impo = pd.DataFrame({
    'feature': x.columns,
    'importance': importance
}).sort_values(by='importance', ascending=False)
print('feature 중요도')
print(feat_impo)

# importance 시각화
import matplotlib.pyplot as plt
import koreanize_matplotlib
plt.figure()
plt.bar(feat_impo['feature'], feat_impo['importance'])
plt.xlabel('feature')
plt.ylabel('중요도(클래스 간 평균 차이)')
plt.xticks(rotation=45)
plt.tight_layout()
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
print('확률은 ', np.round(model.predict_proba(newdata), 4))