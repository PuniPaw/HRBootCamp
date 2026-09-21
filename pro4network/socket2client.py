# client

from socket import *

clientsock = socket(AF_INET, SOCK_STREAM)
clientsock.connect(('192.168.0.43', 7788))
clientsock.send('안냥 고등어'.encode()) # 문자열을 바이트로 변경
print('수신 자료: ', clientsock.recv(1024).decode())
clientsock.close()

# server 실행 중 - client 실행 - server가 수신 후 종료