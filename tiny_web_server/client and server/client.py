import socket
import datetime

x = datetime.datetime.now()
HOST = ''
PORT = 50001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))
str = input()
s.send(str.encode())
print('sent Time is: ', x)
print(s.recv(1024))
s.close()