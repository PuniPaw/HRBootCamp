# matplotlib: 프로팅 라이브러리. 그래프 작성을 위한 다양한 함수 제공
# 데이터 시각화는 복잡하고 방대한 양의 차트, 그래프, 지도 등의
#  시각적 형태로 표현하여 정보를 직관적으로 이해하고 빠른 의사결정을 돕는다.

import numpy as np
import matplotlib.pyplot as plt
plt.rc('font', family='malgun gothic')  # AppleGothic 한글 깨짐 방지
plt.rcParams['axes.unicode_minus'] = False  # 음수 깨짐 방지


x = ['서울', '인천', '수원']    # list
y = [5, 3, 7]                  # tuple
# y = {5, 3, 7}               # set X
plt.xlabel('지역명')
plt.ylabel('투자액')
plt.xlim([-1, 3])
plt.ylim([0, 10])
plt.yticks(list(range(0, 11, 3)))   # y축의 라벨을 인위적으로 변경
plt.plot(x, y) 
plt.show()

data = np.arange(1, 11, 2)
plt.plot(data)  # x축의 구간은 자동 설정
x = [0,1,2,3,4]
for a, b in zip(x, data):
    plt.text(x=a, y=b, s=str(b))
plt.show()

x = np.arange(10)
y = np.sin(x)
print(x, y)
# plt.plot(x, y, 'bo')    # color, marker
plt.plot(x, y, 'go--', linewidth=2, markersize=12)
plt.show()

# hold: 복수의 plot으로 여러 개의 차트를 겹처 그림
x = np.arange(0, np.pi * 3, 0.1)
print(x)
y_cos = np.cos(x)
y_sin = np.sin(x)
plt.figure(figsize=(10, 5))     # 그래프 전체 크기 지정(w, h)
plt.plot(x, y_sin, 'r') # 선
plt.scatter(x, y_cos)   # 산점도
plt.legend(['사인', '코사인'])  # 범례
plt.show()

print()
# subplot: 하나의 figure를 여러 개의 Axes(plot)으로 나누기
# plt.subplot(행, 열, 위치)  -> 위치는 1부터 시작
plt.figure(figsize=(10, 6))

plt.subplot(2, 1, 1)        # 2행 1열 중 첫 번째
plt.plot(x, y_sin, 'r')
plt.title('sine')
plt.grid(True)

plt.subplot(2, 1, 2)        # 2행 1열 중 두 번째
plt.plot(x, y_cos, 'b')
plt.title('cosine')
plt.grid(True)

plt.tight_layout()          # 서브플롯 간 제목/라벨 겹침 방지
plt.show()

print()
# 객체 지향 방식(객체지향 방식(fig, axes)) 사용하기
fig, axes = plt.subplots(2, 1, figsize=(10, 6))   # 2행 1열

axes[0].plot(x, y_sin, 'r')
axes[0].set_title('sine')
axes[0].grid(True)

axes[1].plot(x, y_cos, 'b')
axes[1].set_title('cosine')
axes[1].grid(True)

fig.tight_layout()
plt.show()

print()
irum = ['a', 'b', 'c', 'd', 'e']
kor = [80, 50, 70, 70, 90]
eng = [60, 70, 80, 90, 100]
plt.plot(irum, kor, 'ro-')
plt.plot(irum, eng, 'bo--')
plt.ylim([50, 100])
plt.title('시험 점수')
plt.legend(['국어', '영어'], loc='best')    # loc=1~4
plt.grid(True)

# 그래프를 이미지 파일로 저장
fig = plt.gcf()
plt.show()
fig.savefig('mplot1.png')

# 이미지 읽기
from matplotlib.pyplot import imread
img = imread('mplot1.png')
plt.imshow(img)
plt.show()