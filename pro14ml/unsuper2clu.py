# 계층적 군집 분석: 학생 10명의 시험점수 상ㅇ

import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster

students = ['s1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10']
scores = np.array([76,95,65,85,60,92,55,88,83,72]).reshape(-1, 1)
print('점수: ', scores)

linked = linkage(scores, method='ward')

# 시각화
plt.figure(figsize=(10, 6))
dendrogram(linked, labels=students)
plt.title('학생들 점수 군집')
plt.xlabel('학생명')
plt.ylabel('거리')
plt.axhline(y=25, color='red', linestyle='--', label='cut at 25')
plt.legend()
plt.grid(True)
plt.show()

# 계층적 군집분석 결과를 3개의 군집으로 나누기
clusters = fcluster(linked, t=3, criterion='maxclust')
print('학생 군집 결과')
for stu, cluster in zip(students, clusters):
    print(f'{stu}: cluster {cluster}')

print()
# 군집별 점수와 이름 확인
cluster_info = {}
for student, cluster, score in zip(students, clusters, scores.flatten()):
    if cluster not in cluster_info:
        cluster_info[cluster] = {"students":[], "scores":[]}

    cluster_info[cluster]['students'].append(student)
    cluster_info[cluster]['scores'].append(score)

print(cluster_info)

print('\n군집별로 평균 점수와 이름 출력')
for cluster_id, info in sorted(cluster_info.items()):
    avg_score = np.mean(info['scores'])
    students_list = ', '.join(info['students'])
    print(f'군집 {cluster_id}: 평균 점수={avg_score:.2f}, 학생들={students_list}')