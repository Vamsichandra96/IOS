'''
    Disclaimer
    tiny httpd is a web server program for instructional purposes only
    It is not intended to be used as a production quality web server
    as it does not fully in compliance with the 
    HTTP RFC https://tools.ietf.org/html/rfc2616

    This task is designed by Praveen Garimella and is to be used
    as part of the Learning by Doing, Project Based Course on Operating Systems
    Write to pg@fju.us for any questions or comments
'''

'''
    == Task 2 ==
    This file has the solution for M1 and the description for M2.
    Review this solution before you start implementing the M2.
    If you don't like our solution for M1 then
    tell us why so that we can improve it.

    In the M2 you have to write code to handle http requests for static content.
    Web servers maintain static content in a directory called document root.
    We have provided you with a directory with the name www.
    This directory has some html files and images.
    A web server may receive a request to access one of these files.

    When such a request is received you have to parse the HTTP request
    and extract the name of the file in the request aka Uniform Resourse Indicator    
    Learn the format of the http requests from the tutorial given below.
    https://www.tutorialspoint.com/http/http_requests.htm

    After extracting the URI,
    check if the file exists in the document root directory i.e., www

    If it exists, you have to read the file contents as the response data.
    If not you have to send a 404 file not found response.

    Construct the http response by invoking response_headers method
    This method is provided in the HTTPServer class
    Passing the appropriate response code, content type and length to the method
    
    A tricky part to the response construction is to identify the content type.
    Set the content type text/html for files that end with the extension .html
    
    What would be the content type for images? Review the link below.
    https://www.iana.org/assignments/media-types/media-types.xhtml#image

    How do we figure out the content subtype of an image?
    Explore the use of the library mimetype in python.
    https://www.tutorialspoint.com/How-to-find-the-mime-type-of-a-file-in-Python
'''

import socket
import os
import mimetypes
class HTTPServer:
    def __init__(self, IP, port):
        super().__init__()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP) as self.s:
            # self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
            # print('Connected by', addr)
            self.s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            self.s.bind((IP, port))
            print('server created')
            self.s.listen(5)
            uri = ""
            dirPath =""
            parent = ""
            while True:
                conn, addr = self.s.accept()
                print('Connected by', addr)
                with conn:
                    http_response = conn.recv(1024)
                    uri = self.getUri(http_response)
                    print("uri: " + uri)
                    files_List = ""
                    if(uri == "/"):
                        allFiles = os.listdir(root_Directory)
                        files_List += '<a href = "/" > .. </a>' + "<br>"
                        for eachFile in allFiles:
                            print(eachFile)
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
                            print("parent is: " + parent)
                            files_List += "<a href = " + parent + " >.. </a>" + "<br>"
                            for eachFile in allFiles:
                                eachFile = "<a href =" + uri + "/" + eachFile + ">" + str(eachFile) + "</a>"
                                files_List += eachFile + "<br>"
                            code = 200 
                            c_length = len(files_List)
                            # c_type = ".directory"
                            c_type = "text/html"
                            response = self.response_headers(code, c_type, c_length).encode() + files_List.encode()
                        except:
                            print("exception raised")
                            code, c_type ,c_length, dataOne = self.get_data(uri)
                            print("type: " + c_type)
                            response = self.response_headers(code, c_type, c_length).encode() + dataOne
                    conn.sendall(response)
                    conn.close()

    def get_data(self, uri):
        # TODO: This function has to be updated for M2'
        if uri == "":
            data = "<h1>Webserver Under construction</h1>"
            return 200, "text/html", len(data), data.encode()

        path = root_Directory + str(uri)
        print("path: " + path)
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
        tempArray = http_response.decode().split(" ")[1]
        # fileName = tempArray[1].split(" ")[0]
        return tempArray
def main():
    # test harness checks for your web server on the localhost and on port 8888
    # do not change the host and port
    # you can change  the HTTPServer object if you are not following OOP
    HTTPServer('127.0.0.1', 8888)

line = "\n"
root_Directory = os.getcwd() + "/www"
Enable_DirectoryBrowsing = True
if __name__ == "__main__":
    main()
