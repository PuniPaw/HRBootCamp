"""
이미지 분류(Image Classification)란 컴퓨터가 이미지의 픽셀값을 숫자 데이터로 처리하고,
해당 이미지에 부여된 정답(Label)을 바탕으로 특징과 패턴을 학습하여 새로운 이미지가
어떤 종류에 속하는지 예측하는 기술이다.
전통적인 머신러닝에서는 이미지의 픽셀값을 1차원 벡터로 전환하여 학습에 사용하고,
CNN과 같은 딥러닝에서는 이미지의 공간적 구조를 유지하면서 특징을 학습한다.

-- 이미지 분류는 이미지를 컴퓨터가 처리할 수 있는 숫자 데이터로 표현하고,
정답이 있는 이미지들을 이용해 특징과 패턴을 학습한 뒤,
새로운 이미지가 어떤 클래스에 속하는지 예측하는 과정 ---

이미지 분류 과정:
1) 원본 이미지 -> 픽셀숫자화 -> [[124, 85, ...],[97, 52, ...]] -> 배열로 표현
2) 모델 학습(배열 + 정답) -> 모델 생성
"""
import numpy as np
img = np.random.randint(0, 256, (28, 28))   # 28 x 28 크기의 가상 흑백 이미지
print(img.shape)    # (28, 28)
vector = img.flatten()  # 1차원 벡터로 변환
print(vector.shape) # (784, )   즉, 28 * 28 개의 픽셀을 가진 이미지는 784개 벡터로 변환

# PCA(주성분 분석): 선형대수 관점에서, 입력 데이터의 공분산 행렬을 고윳값 분해하고
# 이렇게 구한 고유벡터에 입력 데이터를 선형변환 하는 것이다.
# 이 고유벡터가 PCA의 주성분 벡터로서 입력 데이터의 분산이 큰 방향을 나타낸다.
# 입력 데이터가 성질을 최대한 유지한 상태로 고차원을 저차원 데이터로 변환하는 기법
# 차원 축소의 3가지 순기능
# 1) 차원이 낮아지면 대상에 대한 이해가 보다 쉬워지게 된다.
# 2) 연산 속도가 개선된다.
# 3) '차원의 저주'를 해결하는 열쇠가 된다.
# 차원 증가에 따라 요구되는 데이터의 양이 기하급수적으로 늘어나기 때문에 차원축소를 함.

# iris data로 차원 축소
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import koreanized_matplotlib
import seaborn as sns
import pandas as pd
from sklearn.datasets import load_iris

iris = load_iris()
n = 10
x = iris.__delattr__[:n, :2]    # sepal length, width 열만 선택
print('차원 축소 전: ', x, x.shape, type(x))
print(x.T)

# 시각화 1: 각 샘플의 두 특성 값을 선으로 연결해 비교
plt.plot(x.T, 'o:')
plt.xticks(range(2), ['꽃받침길이', '꽃받침너비'])
plt.grid(True)
plt.title('아이리스 크기 특성')
plt.xlabel('특성의 종류')
plt.ylabel('특성값')
plt.legend(['표본 {}'.format(i + 1) for i in range(n)])
plt.show()
plt.close()

# 시각화 2: 산점도
df = pd.DataFrame(x)
print(df)

ax = sns.scatterplot(x=0, y=1, data=df, markers='s', s=100, color='b')
for i in range(n):
    ax.text(x[i, 0] - -0.05, x[i, 1] + -0.05, '표본{}'.format(i+1))

plt.title('아이리스 크기 특성')
plt.xlabel('꽃받침길이')
plt.ylabel('꽃받침너비')
plt.show()
plt.close()

# 위 두개의 그래프 결과 두 변수는 공통적인 특징이 있으므로 차원축소의 근거가 있다고 판단.
# PCA를 진행 - 선형변환을 통해 차원을 축소
# 순서1: 입력 데이터의 공분산 행렬을 생성한다.
# 순서2: 공분산 행렬의 고유벡터와 고윳값(고유벡터 크기)을 계산한다.
# 순서3: 고윳값이 큰 순서대로 k개(PCA 변환 차수 만큼)만큼 고유 벡터 추출
# 순서4: 고윳값이 가장 큰 순으로 추출된 고유벡터를 이용해 새롭게 입력 데이터를 변환한다.
# sklearn의 PCA를 이용하면 순서대로 진행함

pca1 = PCA(n_components=1)  # 변환할 차원 수(제 1 주성분)
# pca1 = PCA(n_components=2)  # 제1주성분(데이터 분산이 가장 큰 방향), 제2주성분(제1주성분과 직교하면서 분산이 두 번째로 큰 방향)
x_low = pca1.fit_transform(x)   # 특징 행렬을 낮은 차원의 근사행렬로 변환
print('x_low: ', x_low, ' ', x_low.shape)

# 값 비교
x2 = pca1.inverse_transform(x_low)  # 주성분값 원복
print('원복 후: ', x2, x2.shape)
print('원본: ', x[0:, :])
print('주성분: ', x_low[0])
print('원복: ', x[0:, :])

# 주성분 분석값을 기반으로 시각화: pca방향벡터
pc1 = pca1.components_[0]   # components_: 주성분 벡터
mean = x.mean(axis=0)   # 데이터 평균(중심점)

df = pd.DataFrame(x)
ax = sns.scatterplot(x=0, y=1, data=df, markers='s', s=100, color='b')
for i in range(n):
    ax.text(x[i, 0] - -0.05, x[i, 1] + -0.05, '표본{}'.format(i+1))

# PCA 축 (화살표)
plt.quiver(
    mean[0], mean[1],   # 시작점(평균)
    pc1[0], pc1[1],     # 방향
    scale=3, color='r', width=0.01
)

plt.title('아이리스 크기 특성 + 제1주성분')
plt.xlabel('꽃받침길이')
plt.ylabel('꽃받침너비')
plt.axis('equal')   # x, y눈금 간격 동일 비율로 표시
plt.show()
plt.close()

print('******' * 5)
# 원본 열 4개를 차원 축소해 2개의 열로 변환 후 SVM 분류 모델 작성
x = iris.data
print(x[0, :])
pca2 = PCA(n_components=2)
x_low2 = pca2.fit_transform(x)
print('x_low2: ', x_low2[0, :], ' ', x_low2.shape)

# 변동성 비율 확인: 각 주성분이 전체 데이터의 분산을 얼마나 잘 설명하는지에 대한 비율
print(pca2.explained_variance_ratio_)
x4 = pca2.inverse_transform(x_low2)
print('최초 자료: ', x[0])
print('차원 축소: ', x_low2[0])
print('차원 복귀: ', x4[0, :])
print()

iris1 = pd.DataFrame(x, columns=['sepal length', 'sepal width', 'petal length', 'petal width'])
print(iris1.head(3))
iris2 = pd.DataFrame(x_low2, columns=['var1', 'var2'])
print(iris2.head(3))

from sklearn import svm, metrics
feature1 = iris1.values
print(feature1[:3])
label = iris.target
print(label[:3])

print('원본 데이터로 SVM 분류 모델 작성')
model1 = svm.SVC(C=0.1, random_state=0).fit(feature1, label)
pred1 = model1.predict(feature1)
print('model1 accuarcy: ', metrics.accuracy_score(label, pred1))

print('PCA데이터로 SVM 분류 모델 작성')
feature2 = iris2.values
print(feature2[:3])

model2 = svm.SVC(C=0.1, random_state=0).fit(feature2, label)
pred2 = model2.predict(feature2)
print('model2 accuarcy: ', metrics.accuracy_score(label, pred2))