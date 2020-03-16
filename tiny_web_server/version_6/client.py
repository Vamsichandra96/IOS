import socket
import datetime

HOST = '127.0.0.1'
PORT = 8888
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))
str = "hello"
s.send(str.encode())
print(s.recv(1024))
s.close()