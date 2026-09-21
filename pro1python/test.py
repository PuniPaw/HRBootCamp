class Gugudan:
    def print_dan(self):
        dan = 3
        i = 0
        for dan in range(3, 10, 2):
            for i in range(1, 10):
                print(f'{dan} X {i} = {dan*i}', end=' ')
                i += 1
            print()



gugu = Gugudan()  # 객체 생성 후 메소드 호출
gugu.print_dan()