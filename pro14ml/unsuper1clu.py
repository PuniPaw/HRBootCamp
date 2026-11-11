# 군집분석: 데이터 간의 유사도를 정의하고 그 유사도에 가까운
# 것 부터 순서대로 합쳐가는 방법으로, 거리나 상관계수 등을 이용한다.
# 이는 비슷한 특성을 가진 개체를 그룹으로 만들고,
# 군집 분리 후 t-test, ANOVA 분석 등을 통해 군집 간 평균의 차이를 확인할 수도 있다.
# 군집분석은 데이터만 주고 label은 제공하지 않는 비지도학습이다.

# 클러스터링 기법 중 계층적 클러스터링 연습
# 응집형(군집의 크기를 점점 늘리기 - 상향식)과
# 분리형(군집으 크기를 줄여 나가기 - 하향식)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib

np.random.seed(123)

var = ['x', 'y']
labels = ['점0', '점1', '점2', '점3', '점4']
x = np.random.random_sample([5, 2]) * 10
df = pd.DataFrame(x, columns=var, index=labels)
print(df)

plt.scatter(x[:, 0], x[:, 1], c='blue', marker='o', s=50)
# text추가
for i, txt in enumerate(labels):
    plt.text(x[i, 0], x[i, 1], txt)

plt.grid(True)
plt.show()

# 각 점 간의 거리 계산
from scipy.spatial.distance import pdist, squareform
dist_vec = pdist(df, metric='euclidean')
print('dist_vec: ', dist_vec)

# pdist의 결과를 사각형 형식으로 보기
row_dist = pd.DataFrame(squareform(dist_vec), columns=labels, index=labels)
print(row_dist)

print()
# 계층적 클러스터링 (군집분석)
from scipy.cluster.hierarchy import linkage # 응집형 계층적 클러스터링
row_clusters = linkage(dist_vec, method='ward')
# print(row_clusters)
df2 = pd.DataFrame(row_clusters, columns=['군집id1', '군집id2', '거리', '군집멤버'])
print(df2)
#    군집id1  군집id2        거리  군집멤버
# 0    0.0    2.0  1.388848   2.0   <-- 점0과 점2를 병합. 병합된 군집 데이터 수: 2, 새로운 군집 ID: 5
# 1    4.0    5.0  2.657109   3.0   <-- 점4과 점5를 병합. 병합된 군집 데이터 수: 3, 새로운 군집 ID: 6
# 2    1.0    6.0  5.454004   4.0   <-- 점1과 점6를 병합. 병합된 군집 데이터 수: 4, 새로운 군집 ID: 7
# 3    3.0    7.0  6.647102   5.0   <-- 점3과 점7를 병합. 병합된 군집 데이터 수: 5, 새로운 군집 ID: 8
# 군집8 = {점0, 점1, 점2, 점3, 점4}
# 최종적으로 5개의 점이 하나의 군집이 됨

print('군집6에 속한 멤버(점)들 보기 ---')
from scipy.cluster.hierarchy import to_tree

root, nodes = to_tree(row_clusters, rd=True)    # linkage 결과를 트리구조로 변환
ids = nodes[6].pre_order()  # 군집6에 속한 원본 점id
print('군집6의 점id: ', ids)
print('군집6의 점이름: ', [labels[i] for i in ids])
print(df.iloc[ids])     # 군집 6에 포함된 실제 데이터

# 군집의 계층 구조를 계통도(dendrogram)로 출력
from scipy.cluster.hierarchy import dendrogram
dendrogram(row_clusters, labels=labels)
plt.tight_layout()
plt.ylabel('유클리드 거리값')
plt.show()