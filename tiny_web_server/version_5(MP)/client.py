import socket
import datetime

HOST = '10.10.10.160'
PORT = 8888
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))
s.send(input().encode())
print(s.recv(1024).decode())
s.close()