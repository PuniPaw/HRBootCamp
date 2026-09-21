# 1회용 서버
from socket import *

# socket 객체 생성
serversock = socket(AF_INET, SOCK_STREAM)   # socket(소켓종류, 소켓유형)
#socket을 이용해 특정 컴퓨터와 바인딩(서버의 ip와 port 연결)
serversock.bind(('192.168.0.43', 8888))

# 연결 대기상태로 전환 - 리스너 설정
serversock.listen(5)
print('서버 서비스 중...')

# 클라이언트의 접속 대기
conn, addr = serversock.accept()
print('client addr: ', addr)

# 클라이언트가 보낸 데이터 수신
msg = conn.recv(1024).decode()
print('from client message: ', msg)

# 연결 종료
conn.close()
serversock.close()

