# LogisticRegression: 날씨 예보(비가 올지 안 올지)

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import statsmodels.api as sm
import statsmodels.formula.api as smf

data = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/weather.csv')
print(data.head(3), data.shape)
print(data.info())
df = pd.DataFrame()
df = data.drop(['Date', 'RainToday'], axis=1)
df['RainTomorrow'] = df['RainTomorrow'].map({'Yes':1, 'No':0})
print(df.head(2), df.shape)
print(df['RainTomorrow'].unique())
# RainTomorrow: 종속변수(class) - 범주형, 나머지열: 독립변수(feature)

print('데이터 분리: 학습용(trina dataset), 검증용(test dataset)')
# 모델의 성능을 객관적으로 파악하기 위함 - 과적합 방지
train, test = train_test_split(df, test_size=0.3, random_state=42)
print(train.shape, test.shape)
print(train.head(3))
print(test.head(3))

# 모델 생성
col_select = "+".join(train.columns.difference(['RainTomorrow']))
print(col_select)
my_formula = 'RainTomorrow ~ ' + col_select
model = smf.logit(formula=my_formula, data=train).fit()
print(model.summary())      # 각 변수별 p-value > 0.05 인 경우 제거 고민
print(model.params)
print()
print('예측값: ', np.rint(model.predict(test)[:5].values))
print('실제값: ', test['RainTomorrow'][:5].values)

# 분류 정확도(train data로 함)
# pred_table(): 기본적으로 모델 학습에 사용한 train데이터만 대상으로 혼동행렬을 생성
pred_mat = model.pred_table()
print(pred_mat)
print('분류 정확도(Accuracy): ', (pred_mat[0][0] + pred_mat[1][1]) / len(train))            # train

# 분류 정확도(test data로 함)
from sklearn.metrics import accuracy_score, confusion_matrix
pred = model.predict(test)
conf_mat = confusion_matrix(test['RainTomorrow'], np.rint(pred))
print(conf_mat)
print('분류 정확도(Accuracy): ', (conf_mat[0][0] + conf_mat[1][1]) / len(test))            # test
print('분류 정확도(Accuracy): ', accuracy_score(test['RainTomorrow'], np.rint(pred)))      # 상동
print('분류 정확도(Accuracy): ', accuracy_score(test['RainTomorrow'], (pred >= 0.5).astype(int)))   # 상동
# pred_table()은 학습에 쓴 train 데이터 기준이라 정확도가 낙관적으로 나옴.
# 처음 보는 데이터에 대한 실제 성능(일반화 성능)을 보려면 test 데이터로 혼동행렬을 구해야 함.
# train 정확도 >> test 정확도 라면 train에만 지나치게 맞춰진 과적합(overfitting)을 의심할 수 있다.

