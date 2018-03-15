#!/usr/bin/python
from http.server import BaseHTTPRequestHandler, HTTPServer
import mainFace
import sys
import traceback
import os
import cgi

PORT_NUMBER = 8080
rootPath = os.path.dirname(os.path.abspath(__file__))

# This class will handles any incoming request from
# the browser


class myHandler(BaseHTTPRequestHandler):

    # Handler for the GET requests
    def do_POST(self):
        print("start post ", self.path)
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        # for field in form.keys():
        #     print("key=", field, form[field])
        self.send_response(200)  # OK
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        if("/uploadRecognation" == self.path):
            print("start recognation")
            print("start upload for recognation")
            answer = "{\"uploadRecognation\":"
            try:
                file_data = form['file']
                fileName = file_data.filename
                file_type = text = file_data.type.split('/')
                file_data = file_data.file.read()
                file_len = len(file_data)
                # print("formName=", file_type[0], " fileNa=",
                #       fileName, " fileSize=", file_len)
                if (file_len < 2000000):
                    if(file_type[0] == 'image'):
                        with open("./forRecognation/" + fileName + "." + file_type[1], "wb+") as f:
                            f.write(file_data)
                        # try:
                        #     res = mainFace.findFace("start")
                        # except:
                        #     print("error get start")
                        # self.wfile.write(bytes("Hello World !", "utf8"))
                        answer += "\"Success\",\"Type\":\"info\"}"
                    else:
                        answer += "\"Error file type\",\"Type\":\"danger\"}"
                else:
                    answer += "\"File is bigger then 2MB\",\"Type\":\"danger\"}"
                del file_data
            except:
                print("error sace file", traceback.print_exc())
                answer += "\"Error file type\",\"Type\":\"danger\"}"
            print("file=", answer)
            self.wfile.write(bytes(answer, "utf8"))
        elif("/upload" == self.path):
            print("start upload")
            answer = "{\"UploadPhoto\":"
            try:
                file_data = form['file']
                fileName = form.getvalue('fileName')
                file_type = text = file_data.type.split('/')
                file_data = file_data.file.read()
                file_len = len(file_data)
                print("formName=", file_type[0], " fileName=",
                      fileName, " fileSize=", file_len)
                if (file_len < 2000000):
                    if(file_type[0] == 'image'):
                        if(fileName != ""):
                            with open("./faces/" + fileName + "." + file_type[1], "wb+") as f:
                                f.write(file_data)
                            answer += "\"Success\",\"Type\":\"info\"}"
                        else:
                            answer += "\"Error Photo name type\",\"Type\":\"danger\"}"
                    else:
                        answer += "\"Error file type\",\"Type\":\"danger\"}"
                else:
                    answer += "\"File is bigger then 2MB\",\"Type\":\"danger\"}"
                del file_data
            except error:
                # print("error sace file", error)
                answer += "\"Error file type\",\"Type\":\"danger\"}"
            print("file=", answer)
            self.wfile.write(bytes(answer, "utf8"))
        elif("/deleteFace" == self.path):
            answer = "{\"deleteFacesResult\":"
            try:
                name = form['name'].value
                path = rootPath + "/faces/" + name
                os.remove(path)
                answer += "\"ok\",\"name\":\"" + name + "\",\"Type\":\"info\"}"
                print("answer=", answer)
                self.wfile.write(bytes(answer, "utf8"))
            except error:
                answer += "\"File does not exist.\",\"Type\":\"danger\"}"
                print("error delete image=", error)
                self.wfile.write(bytes(answer, "utf8"))
        else:
            answer = "{urlNotFound:\"Url is not exist.\",\"Type\":\"danger\"}"
            print("404 can not path=", self.path)
            self.wfile.write(bytes(answer, "utf8"))

    def do_GET(self):
        # print("photos=", )
        # print("path=" + self.path)
        self.send_response(200)
        if("/faces" in self.path):
            # print("Start faces ")
            filename = rootPath + self.path
            try:
                with open(filename, 'rb') as fh:
                    data = fh.read()
                    self.send_header('Content-type', 'image/jpeg')
                    self.end_headers()
                    self.wfile.write(data)
            except:
                print("error open file")
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes("Error open img", "utf8"))
        elif("/img" in self.path):
            filename = rootPath + self.path
            try:
                with open(filename, 'rb') as fh:
                    data = fh.read()
                    self.send_header('Content-type', 'image/jpeg')
                    self.end_headers()
                    self.wfile.write(data)
            except:
                print("error open file")
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes("Error open img", "utf8"))
        elif("/getFaces" == self.path):  # deleteFace
            answer = "{\"geFacesResult\":["
            try:
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                listFiles = []
                for dirname, dirnames, filenames in os.walk('./faces', topdown=False):
                    for filename in filenames:
                        listFiles.append(filename)
                strFiles = ','.join('"' + item + '"' for item in listFiles)
                answer += strFiles + "]}"
                print("listPhotos=" + answer)
                self.wfile.write(bytes(answer, "utf8"))
            except:
                print("error get list images")
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                answer += "]}"
                self.wfile.write(bytes(answer, "utf8"))
        elif("/favicon.ico" in self.path):
            self.end_headers()
        else:
            print("404 can not find file " + self.path)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes("404! File not found.", "utf8"))
        return


try:
    # Create a web server and define the handler to manage the
    # incoming request
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print("Started httpserver on port ", PORT_NUMBER)
    # Wait forever for incoming htto requests
    server.serve_forever()

except KeyboardInterrupt:
    print("^C received, shutting down the web server")
    server.socket.close()
