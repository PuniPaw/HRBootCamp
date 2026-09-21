# client

from socket import *

clientsock = socket(AF_INET, SOCK_STREAM)
clientsock.connect(('192.168.0.43', 8888))
clientsock.send('안냥 고등어'.encode())  # 문자열을 바이트로 변경

clientsock.close()

# server 실행 중 - client 실행 - server가 수신 후 종료