# 다층 인공신경망(MLP)으로 다항 분리
# sklearn.datasets.load_wine()
# • 샘플 수: 총 178개 (클래스별 59개, 71개, 48개)
# • 특성(Features) 수: 13개의 양수(Real, positive) 수치형 특성
# • 타겟(Target) 클래스: 3개 (이탈리아의 서로 다른 세 지역에서 생산된 와인 원산지 분류)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

data = load_wine()
x = data.data
y = data.target
print(x[:2], ' ', x.shape)
print(y[:2], ' ', np.unique(y))

x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=42, stratify=y
)

# Scaleing (MLP에서 권장)
scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(x_train)
x_test_scaled = scaler.fit_transform(x_test)

# 모델 생성
model = MLPClassifier(
    hidden_layer_sizes=(20, 10),       # 은닉층 2개(첫번째: 노드 20개, 두번째: 노드 10개)
    solver='adam',          # 손실 최소화
    activation='relu',      # 은닉층의 활성화 함수
    max_iter=150,
    learning_rate_init=0.001,
    random_state=42,
    verbose=1       # 학습 도중 로그 출력 여부
)

model.fit(x_train_scaled, y_train)
pred = model.predict(x_test_scaled)
print('acc: ', accuracy_score(y_test, pred))
print(classification_report(y_test, pred))

# 혼동행렬 시각화
cm = confusion_matrix(y_test, pred)
plt.figure(figsize=(5, 4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title('confusion matrix')
plt.xlabel('predict')
plt.ylabel('actual')
plt.show()