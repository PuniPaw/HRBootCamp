class Bicycle:
    def __init__(self, name, wheel, price):
        self.name = name
        self.wheel = wheel
        self.price = price

    def total(self):
        return self.wheel * self.price

    def display(self):
        print(f'{self.name}님 자전거 바퀴 가격 총액은 {self.total()}원 입니다')

gildong = Bicycle('길동', 2, 50000) # 생성자로 name, wheel, price 입력됨
gildong.display()