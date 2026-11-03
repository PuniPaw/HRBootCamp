# [로지스틱 회귀 핵심]
# 선형식 wx + b 의 범위: -∞ ~ +∞  /  확률 p 의 범위: 0 ~ 1  → 그대로 못 씀
# odds = p / (1-p)            : 범위 0 ~ +∞
# logit = log(p / (1-p))      : 범위 -∞ ~ +∞ (p=0.5 일 때 0) → 선형식과 범위 일치
# log(p / (1-p)) = wx + b 라고 정의됨
# 이를 p에 대해 풀면 p = 1 / (1 + e^(-z))  → 시그모이드 함수
# 그러므로 z = wx + b --> sigmoid(z) --> p( 0 ~ 1 ): 이항 분류 (p >= 0.5 이면 1, 아니면 0)

# sigmoid function 수식에 의해 변환된 값 확인

import math

def MySigmoidFunc(num):     # num: logit 변환한 값이라 가정
    return 1/ (1+math.exp(-num))

print(MySigmoidFunc(3))
print(MySigmoidFunc(1.5))
print(MySigmoidFunc(-5.0))
print(MySigmoidFunc(-10))
# 0.9525741268224334
# 0.8175744761936437
# 0.0066928509242848554
# 4.5397868702434395e-05

import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib

print('\n로짓(logit)변환된 (가정)값으로 시그모이드 함수 통과 후 결과 시각화')
x = np.linspace(-10, 10, 50)    # 입력자료 (연속형)
print(x)

# 선형결합 (이미 logit된 값)
w = 1.5
b = -2
z = w * x + b

def OurSigmoidFunc(z):     # z: logit 변환한 값이라 가정
    return 1/ (1+np.exp(-z))

p = OurSigmoidFunc(z)
print('p: \n', p)

# 일부만 보기
print('x[:3]: ', np.round(x[:3], 3))
print('z[:3](logit): ', np.round(z[:3], 3))
print('p[:3](확률): ', p[:3])

# 시각화
plt.figure(figsize=(8, 5))
plt.plot(x, p, label='sigmoid(z)', color='blue')
plt.axhline(0.5, color='red', linestyle='--')
plt.title('z=wx + b --> sigmoid --> 확률(이항)')
plt.xlabel('x(입력값)')
plt.ylabel('p(확률값)')
plt.grid(True)
plt.legend()
plt.show()