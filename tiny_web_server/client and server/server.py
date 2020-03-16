import socket

HOST = ''
PORT = 50001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST,PORT))
print('server created')
s.listen()

while 1:
    conn,addr = s.accept()
    print('connected by' ,addr)
    data = conn.recv(1024)
    if not data:break
    conn.send(data)

conn.close()