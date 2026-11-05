# LogisticRegression - 다항분류(softmax 함수 사용) - iris dataset으로 실습
# Softmax 함수는 인공지능의 Multi-class Classification 문제에서 출력층에 주로 사용

import pandas as pd
import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.preprocessing import StandardScaler, MinMaxScaler  # 표준화, 정규화
from sklearn.linear_model import LogisticRegression
# LogisticRegression: 이항분류 뿐 아니라 다중 클래스를 지원함

iris = datasets.load_iris()
print(iris.keys())
print(iris.target)
print(iris.data[:3])
print(np.corrcoef(iris.data[:,2], iris.data[:,3])[0, 1])

x = iris.data[:,[2, 3]]
y = iris.target
print(x.shape, y.shape)         # (150, 2) (150,)
print(x[:3], y[:3], set(map(int, y)))
# [[1.4 0.2]
#  [1.4 0.2]
#  [1.3 0.2]] [0 0 0] {0, 1, 2}

print('\ntrain / test split (7:3)')
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)
print(x_train.shape, x_test.shape, y_train.shape, y_test.shape)     # (105, 2) (45, 2) (105,) (45,)
print(x_train[:3],x_test[:3], y_train[:3], y_test[:3])

# Scaling (데이터 크기 표준화/정규화 - 최적화 과정의 안정성·수렴 속도 향상, 과적합/과소적합 방지에 도움)
sc = StandardScaler()     # 표준화
sc.fit(x_train)
# sc.fit(x_test)      # 주의: feature만 스케일링한다.
x_train = sc.transform(x_train)
x_test = sc.transform(x_test)
print(x_train[:3])
print(x_test[:3])
# 스케일링 원복
ori_x_train = sc.inverse_transform(x_train)
print(ori_x_train[:3])
ori_x_test = sc.inverse_transform(x_test)
print(ori_x_test[:3])


print('분류 모델 생성 ------')
model = LogisticRegression(random_state=0)
model = LogisticRegression(
    C=1.0,              # 모델에 페널티 적용(L2 규제), 숫자값을 조정해 가며 정확도 확인 
    solver='lbfgs',     # 최적화 알고리즘 방식 중 하나
    # multi_class='multinomial',  # softmax 지원  - 최근 버전부터 생략
    max_iter=100,   # 최적화 알고리즘을 찾는 최대 반복 횟수
    random_state=0
)
print(model)

model.fit(x_train, y_train)     # train으로 학습

# 분류 예측
y_pred = model.predict(x_test)      # x_test 로 예측
print('예측값: ', y_pred)
print('실제값: ', y_test)
print(f'총 갯수: {len(y_test)}, 오류 수: {(y_test != y_pred).sum()}')

print(f'분류 정확도: {accuracy_score(y_test, y_pred)}')
conf_mat = confusion_matrix(y_test, y_pred)
print('혼동행렬: \n', conf_mat)
print('분류 정확도: ', np.trace(conf_mat) / np.sum(conf_mat))   # 클래스가 다항인 경우
# print('분류 정확도: ', conf_mat[0][0] + conf_mat[1][1] / len(y_test)) 

print(f'train score: {model.score(x_train, y_train)}')
print(f'test score: {model.score(x_test, y_test)}')
# train score와 test score의 차이가 크면 과적합 의심.

# 학습 후 검증이 끝난 모델 저장 후 읽기
import joblib
joblib.dump(model, 'ex20model.sav')     # .model