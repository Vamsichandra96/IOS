import socket

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(("127.0.0.1",8888))

temp = "Hello world"
s.send(temp.encode())
print(s.recv(1024))
