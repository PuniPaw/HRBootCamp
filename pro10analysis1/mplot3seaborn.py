# seaborn: matplotlib의 기능 보충용, 통계 데이터 시각화에 특화

import matplotlib.pyplot as plt
import seaborn as sns
import koreanize_matplotlib

titanic = sns.load_dataset('titanic')
# print(titanic.info())
print(titanic.info(max_cols=None))  # 전체 정보 출력, max_cols 칼럼 5개 초과하면 

sns.displot(titanic['age'])
plt.title('나이 차트')
plt.show()

sns.boxplot(y='age', data=titanic, palette='Paired')
plt.show()

sns.relplot(x='sex', y='age', data=titanic)
plt.show()

titanic_pivot = titanic.pivot_table(index='class', columns='sex', aggfunc='size')
print(titanic_pivot)
sns.heatmap(titanic_pivot, cmap=sns.light_palette('gray', annot=True, fmt='d'))
plt.show()

# Boxplot 기준으로 이상치(aoutlier) 확인
import pandas as pd
data = [10,12,13,15,14,12,11,100]
df = pd.DataFrame({'score':data})
print(df)

# IQR (제 3사분위 - 제 1사분위한 값) 기반 이상치 탐지
q1 = df['score'].quantile(0.25)
q3 = df['score'].quantile(0.75)
iqr = q3 - q1

# 이상치(outlier) 탐지 기준선
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 - 1.5 * iqr

# 이상치, 정상치 분리
outliers = df[(df['score'] < lower_bound) | (df['score'] > upper_bound)]
filtered_df = df[(df['score'] >= lower_bound) & (df['score'] <= upper_bound)]

print('이상치 값: ', outliers)

# 박스플롯 시각화: 제거 전/후 비교
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# 이상치 포함
sns.boxplot(y=df['score'], ax=axes[0], color='yello')
axes[0].set_title('이상치 포함 데이터')
axes[0].set_ylabel('Score')
axes[0].grid(True)

# 이상치 제거 후
sns.boxplot(y=filtered_df, ax=axes[1], color='lightblue')
axes[1].set_title('이상치 제거 후')
axes[1].set_ylabel('Score')
axes[1].grid(True)

plt.tight_layout()
plt.show()