import time
import fcntl
import signal
import socket
import os
import mimetypes
import threading
# import pyinotify
import inotify.adapters


class HTTPServer:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    allResponses = {}
    uri = ""
    def __init__(self, IP, port):
        super().__init__()
        # with socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP) as self.s:
        self.s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        # print('Connected by', addr)
        self.s.bind((IP, port))
        print('server created')
        self.s.listen(5)
        t = threading.Thread(target = self.changeofFile, args = "").start()
        

    
    def changeofFile(self):
        i = inotify.adapters.Inotify()
        i.add_watch(FNAME)
        for event in i.event_gen(yield_nones = False):
            (_,type_names,path,filename) = event
            if (type_names[0] == "IN_MODIFY" and self.sampleUri in self.allResponses):
                print("change occured.-----------------------------")
                del self.allResponses[self.sampleUri]

    def get_data(self, uri):
        # TODO: This function has to be updated for M2'
        if uri == "":
            data = "<h1>Webserver Under construction</h1>"
            return 200, "text/html", len(data), data.encode()

        path = root_Directory + str(uri)
        if(os.path.isfile(path)):
            data = open(path,'rb').read()
            type = mimetypes.MimeTypes().guess_type(path)[0]
            return 200,type,len(data),data
        else:
            data = "<h1>File Not Found</h1>"
            return 404, "text/html", len(data), data.encode()
    
    def response_headers(self, status_code, content_type, length):
        # TODO update this dictionary for 404 status codes
        response_code = {200: "200 OK", 404: "404 Not Found"}
        headers = ""
        headers += "HTTP/1.1 " + response_code[status_code] + line
        headers += "Content-Type: " + content_type + line
        headers += "Content-Length: " + str(length) + line
        headers += "Connection: close" + line
        headers += line
        return headers

    def getUri(self,http_response):
        tempArray = http_response.split(" ")[1]
        self.sampleUri = tempArray        
        return tempArray

    def listenThread(self):
        while True:
            conn, addr = self.s.accept()
            print('Connected by', addr)
            conn.settimeout(60)
            threading.Thread(target = self.serveRequest, args = (conn,addr)).start()

    def verify(self,uri):
        if(uri in self.allResponses.keys()):
            return True
        return False
    
    def serveRequest(self,conn,addr):
        data = conn.recv(1024).decode()
        if("favicon" in data):
            return
        uri = self.getUri(data)
        if(self.verify(uri)):
            if(len(self.allResponses) >= Max_Size):
                temporary = self.allResponses[uri]
                del(self.allResponses[uri])
                self.allResponses[uri] = temporary
            print("in dict")
        else:
            print("not in dict")
            files_List = ""
            response = ""
            if(uri == "/"):
                allFiles = os.listdir(root_Directory)
                files_List += '<a href = "/" > .. </a>' + "<br>"
                for eachFile in allFiles:
                    if not (eachFile == ".DS_Store"):
                        # info = os.stat(root_Directory + "/" + eachFile)
                        eachFile = "<a href =" + "/"+ str(eachFile) + ">" + str(eachFile) + "</a>"
                        files_List += eachFile + "<br>"
                code = 200 
                c_length = len(files_List)
                c_type = ".directory"
                response = self.response_headers(code, c_type, c_length).encode() + files_List.encode()
            else:
                try:
                    path = root_Directory + uri
                    allFiles = os.listdir(path)
                    parent =  uri
                    parent = parent.split("/")
                    if len(parent) == 2:
                        parent = "/"
                    else:
                        parent = parent[0:-1]
                        parent = "/".join(parent)
                    files_List += "<a href = " + parent + " >.. </a>" + "<br>"
                    for eachFile in allFiles:
                        eachFile = "<a href =" + uri + "/" + eachFile + ">" + str(eachFile) + "</a>"
                        files_List += eachFile + "<br>"
                    code = 200 
                    c_length = len(files_List)
                    c_type = ".directory"
                    response = self.response_headers(code, c_type, c_length).encode() + files_List.encode()
                except:
                    code, c_type ,c_length, dataOne = self.get_data(uri)
                    response = self.response_headers(code, c_type, c_length).encode() + dataOne
            if(len(self.allResponses) >= Max_Size):
                temp = list(self.allResponses.keys())
                print(temp[0])
                print("------------------")
                print(self.allResponses[temp[0]])
                del(self.allResponses[temp[0]])
            self.allResponses[uri] = response
        # print("uri: " + uri)
        # print(self.allResponses.keys())
        conn.sendall(self.allResponses[uri])
        conn.close()


def main():
    # test harness checks for your web server on the localhost and on port 8888
    # do not change the host and port
    # you can change  the HTTPServer object if you are not following OOP
    HTTPServer('10.10.10.160', 8888).listenThread()


line = "\n"
root_Directory = os.getcwd() + "/www"
FNAME = "/home/sirapu/Downloads/tiny_web_server/version_7/www"
Max_Size = 2
Enable_DirectoryBrowsing = True

if __name__ == "__main__":
    main()
