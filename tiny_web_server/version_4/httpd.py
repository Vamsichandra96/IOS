import socket
import os
import mimetypes
import sys
import time
import signal
class HTTPServer:
    hasBin = False
    def __init__(self, IP, port):
        super().__init__()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP) as self.s:
            self.s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            # print('Connected by', addr)
            self.s.bind((IP, port))
            print('server created')
            self.s.listen(5)
            uri = ""
            dirPath =""
            parent = ""
            while True:
                self.hasBin = False
                conn, addr = self.s.accept()
                print('Connected by', addr)
                with conn:
                    response = ""
                    http_response = conn.recv(1024)
                    uri = self.getUri(http_response)
                    # print(self.hasBin)
                    # print("uri: " + uri)
                    files_List = ""
                    if(not self.hasBin):
                        if(uri == "/"):
                            allFiles = os.listdir(root_Directory)
                            files_List += '<a href = "/" > .. </a>' + "<br>"
                            for eachFile in allFiles:
                                # print(eachFile)
                                if not (eachFile == ".DS_Store"):
                                    # info = os.stat(root_Directory + "/" + eachFile)
                                    eachFile = "<a href =" + dirPath + "/"+ str(eachFile) + ">" + str(eachFile) + "</a>"
                                    files_List += eachFile + "<br>"
                            code = 200 
                            c_length = len(files_List)
                            c_type = ".directory"
                            response = self.response_headers(code, c_type, c_length).encode() + files_List.encode()
                        else:
                            try:
                                path = root_Directory + uri
                                allFiles = os.listdir(path)
                                parent = dirPath + uri
                                parent = parent.split("/")
                                if len(parent) == 2:
                                    parent = "/"
                                else:
                                    parent = parent[0:-1]
                                    parent = "/".join(parent)
                                # print("parent is: " + parent)
                                files_List += "<a href = " + parent + " >.. </a>" + "<br>"
                                for eachFile in allFiles:
                                    eachFile = "<a href =" + uri + "/" + eachFile + ">" + str(eachFile) + "</a>"
                                    files_List += eachFile + "<br>"
                                code = 200 
                                c_length = len(files_List)
                                c_type = ".directory"
                                response = self.response_headers(code, c_type, c_length).encode() + files_List.encode()
                            except:
                                print("exception raised")
                                code, c_type ,c_length, dataOne = self.get_data(uri)
                                # print(c_type)
                                # if(c_type == ".py"):
                                response = self.response_headers(code, c_type, c_length).encode() + dataOne
                    else:
                        print("check")
                        temp = root_Directory + uri
                        # code, c_type ,c_length, dataOne = self.get_data(uri)
                        code = 200
                        c_type = "text/plain"
                        data = self.execute(temp)
                        response = self.response_headers(code, c_type, len(data)).encode() + data.encode()
                    conn.sendall(response)
                    conn.close()

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
        print("http response: " + http_response.decode())
        tempArray = http_response.decode().split(" ")[1]
        # code, c_type ,c_length, dataOne = self.get_data(tempArray)
        # print("c_type: " + str(tempArray) + "-----" + str(c_type))
        if (tempArray.find("/bin/ls") == 0 or tempArray.find("/bin/du") == 0 or tempArray.find("/bin/forever") == 0):
            self.hasBin = True
        # fileName = tempArray[1].split(" ")[0]
        return tempArray

    def execute(self,uri):
        pr, cw = os.pipe()
        stdin  = sys.stdin.fileno() # usually 0
        stdout = sys.stdout.fileno() # usually 1
        pid = os.fork()
        if pid:
            # parent
            os.close(cw)
            os.dup2(pr, stdin)
            st =""
            for line in sys.stdin:
                st+= line
            return st
        else:
            # child
            os.close(pr)
            os.dup2(cw, stdout)
            args = [uri]
            os.execvp(args[0],args)

def main():
    HTTPServer('127.0.0.1', 8888)

line = "\n"
root_Directory = os.getcwd()
# Enable_DirectoryBrowsing = True
if __name__ == "__main__":
    main()
