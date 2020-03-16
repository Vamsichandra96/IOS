import socket
import os
import mimetypes
import sys
import time
import signal
import threading

class HTTPServer:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    def __init__(self, IP, port):
        super().__init__()
        # with socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP) as self.s:
        self.s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        # print('Connected by', addr)
        self.s.bind((IP, port))
        print('server created')
        self.s.listen(5)

    def listen(self):
        while True:
            conn, addr = self.s.accept()
            print('Connected by', addr)
            conn.settimeout(60)
            threading.Thread(target = self.serveRequest, args = (conn,addr)).start()

    def serveRequest(self,conn,addr):
        data = conn.recv(1024).decode()
        if "favicon" not in data:
            print("recieved from the client" + data)
            conn.send(data.encode())
            conn.close()

def main():
    HTTPServer('10.10.10.160', 8888).listen()

line = "\n"
root_Directory = os.getcwd()
Enable_DirectoryBrowsing = True
if __name__ == "__main__":
    main()