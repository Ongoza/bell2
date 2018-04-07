#!/usr/bin/python3
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import mainFace
# import camera_con
import sys
import traceback
import os
import io
import cgi
import time
import json
from PIL import Image, ImageDraw
import cv2
from socketserver import ThreadingMixIn
import threading
from multiprocessing import Process, Manager
from collections import defaultdict
from random import randint

PORT_NUMBER = 8080
rootPath = os.path.dirname(os.path.abspath(__file__))
cameras = []

# This class will handles any incoming request from
# the browser


def camera_detection(name):
    print("start camera ", name)


def showImg(self):
    filename = rootPath + self.path
    # print("try open image " + filename)
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
    return


def showLog(self):
    filename = rootPath + self.path
    print("try open log " + filename)
    try:
        with open(filename, 'ab+') as fh:
            data = fh.read()
        # print("data=",data)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(data)
    except:
        print("error open file")
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes("Error open log", "utf8"))
    return


class myHandler(BaseHTTPRequestHandler):

    # Handler for the GET requests
    def do_POST(self):
        print("start post time=", self.path, str(int(round(time.time() * 1000))))
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
                print("formName=", file_type[0], " fileNa=",  fileName, " fileSize=", file_len)
                if (file_len < 2000000):
                    if(file_type[0] == 'image'):
                        strTime = str(int(round(time.time() * 1000)))
                        newName = "./resultFaces/result_" + strTime + "." + file_type[1]
                        print("start save image 0 time=", strTime, newName)
                        pathFile = "./forRecognation/" + fileName
                        baseWidth = 1000
                        baseWidthDelta = baseWidth * 1.2
                        pil_image = Image.open(io.BytesIO(file_data))
                        if(baseWidthDelta < pil_image.size[0]):
                            # scale image to 1000px width
                            wPercent = (baseWidth / float(pil_image.size[0]))
                            hsize = int((float(pil_image.size[1]) * float(wPercent)))
                            print("scale to ", baseWidth, hsize)
                            pil_image = pil_image.resize((baseWidth, hsize), Image.ANTIALIAS)
                        pil_image.save(pathFile)
                        # with open(pathFile, "wb+") as f:
                        #     f.write(file_data)
                        # try:
                        print("save ready 1 time=", str(int(round(time.time() * 1000))))
                        mainFace.loadLocalData()
                        print("save ready 2 time=", str(int(round(time.time() * 1000))))
                        res = mainFace.findFace(pathFile, newName)
                        print("send ready 3 time=", str(int(round(time.time() * 1000))))
                        if(res == 1):
                            answer += "\"" + newName + "\",\"Type\":\"info\"}"
                        else:
                            answer += "\"Error recognize photo\",\"Type\":\"danger\"}"
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
                file_type = file_data.type.split('/')
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
            except:
                print("error sace file",  traceback.print_exc())
                answer += "\"Error file type\",\"Type\":\"danger\"}"
            print("file=", answer)
            self.wfile.write(bytes(answer, "utf8"))
        elif("/updateFace" == self.path):
            print("start updateFace")
            answer = "{\"resultUpdate\":"
            try:
                fileName = form.getvalue('fileName')
                print(form)
                ffile = form.getvalue('file')
                fileOld = form.getvalue('fileOld')
                filesList = form.getvalue('filesList')
                print("filesList", filesList)
                if (ffile):
                    file_type = file_data.type.split('/')
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
                if(fileName != fileOld):
                    filesArr = json.loads(filesList)
                    for item in filesArr:
                        root, ext = os.path.splitext(item)
                        num = str(randint(100000, 1000000))
                        os.replace(rootPath + "/faces/" + root + ext, rootPath + "/faces/" + fileName + '_' + num + ext)
                    answer += "\"Renamed\",\"Type\":\"info\"}"
            except:
                print("error sace file",  traceback.print_exc())
                answer += "\"Error update face\",\"Type\":\"danger\"}"
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
            except:
                answer += "\"File does not exist.\",\"Type\":\"danger\"}"
                print("error delete image=",  traceback.print_exc())
                self.wfile.write(bytes(answer, "utf8"))
        elif("/getVideo" == self.path):
            answer = "{\"Result\":"
            try:
                camIP = form.getvalue('ip')
                camActive = form.getvalue('active')
                if(camActive == "true"):
                    pass
                else:
                    pass

                print("camIP=", camIP)
                answer += "\"ok\",\"name\":\"" + camIP + "\",\"Type\":\"info\"}"
                print("answer=", answer)
                self.wfile.write(bytes(answer, "utf8"))
            except:
                answer += "\"Can not connect to camera.\",\"Type\":\"danger\"}"
                print("error get video=",  traceback.print_exc())
                self.wfile.write(bytes(answer, "utf8"))
        elif("/deleteCamConfig" == self.path):
            answer = "{\"deleteCamConfigResult\":"
            try:
                name = form['name'].value

                answer += "\"ok\",\"name\":\"" + name + "\",\"Type\":\"info\"}"
                print("answer=", answer)
                self.wfile.write(bytes(answer, "utf8"))
            except:
                answer += "\"File does not exist.\",\"Type\":\"danger\"}"
                print("error delete camConfig=",  traceback.print_exc())
                self.wfile.write(bytes(answer, "utf8"))
        elif("/addCamConfig" == self.path):
            answer = "{\"addCamConfigResult\":"
            try:
                with open("./config/camConfig.json", 'rb+') as fh:
                    data = fh.read()
                config = json.loads(data)
                txtData = form.getvalue('body')
                newCam = json.loads(txtData)
                config['cameras'].append(newCam)
                with open('./config/camConfig.json', 'w') as f:
                    json.dump(config, f, ensure_ascii=False)
                # print("newJson=", newCam)
                answer += "\"ok\",\"name\":\"" + newCam["Name"] + "\",\"Type\":\"info\"}"
                print("answer=", answer)
                self.wfile.write(bytes(answer, "utf8"))
            except:
                answer += "\"Can not add to cam config.\",\"Type\":\"danger\"}"
                print("error addCamConfig=", traceback.print_exc())
                self.wfile.write(bytes(answer, "utf8"))

        else:
            answer = "{urlNotFound:\"Url is not exist.\",\"Type\":\"danger\"}"
            print("404 can not path=", self.path)
            self.wfile.write(bytes(answer, "utf8"))

    def do_GET(self):
        # print("photos=", )
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        self.send_response(200)
        if("/faces" in path):
            print("start face")
            showImg(self)
        if("/stream" in path):
            try:
                # vlc rtsp://os@Bluher11_@192.168.1.108:554
                # rtsp://os:Bluher11_@192.168.1.108:554/cam/realmonitor?channel=1&subtype=0
                # rtsp://os:Bluher11_@192.168.1.108:554/cam/realmonitor?channel=1&subtype=1
                #strUrl = "rtsp://os:Bluher11_@192.168.1.108:554/cam/realmonitor?channel=1&subtype=1"
                strUrl = 0
                cap = cv2.VideoCapture(strUrl)
                print("Camera ", cap.isOpened())
                if (cap.isOpened()):
                    self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=--jpgboundary')
                    self.end_headers()
                    print("Connected to camera 0=")
                    while True:
                        try:
                            retval, im = cap.read()
                            ret, jpg = cv2.imencode('.jpg', im)
                            jpg_bytes = jpg.tobytes()
                            print("bute ret=", ret)
                            self.wfile.write("--jpgboundary\r\n".encode())
                            self.send_header('Content-type', 'image/jpeg')
                            self.send_header('Content-length', len(jpg_bytes))
                            self.end_headers()
                            self.wfile.write(jpg_bytes)
                            time.sleep(0.5)
                        except:
                            print("error stream camera")
                            with open(rootPath + "/img/error.png", 'rb') as fh:
                                data = fh.read()
                            self.send_header('Content-type', 'image/jpeg')
                            self.end_headers()
                            self.wfile.write(data)
                            break
                        # time.sleep(self.server.read_delay)
                else:
                    print("Error connect to camera")
                    cap.release()
                    with open(rootPath + "/img/error.png", 'rb') as fh:
                        data = fh.read()
                    self.send_header('Content-type', 'image/jpeg')
                    self.end_headers()
                    self.wfile.write(data)
                if (cap):
                    cap.release()
            except:
                if (cap):
                    cap.release()
                print("Error open page for camera", traceback.print_exc())
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes("Error open page for connect to camera", "utf8"))
        elif("/img" in path):
            showImg(self)
        elif("/log" in path):
            showLog(self)
        elif("/config" in path):
            showLog(self)
            print("get config")
        elif("/resultFaces" in path):
            showImg(self)
        elif("/getCamConfig" in path):
            try:
                with open("./config/camConfig.json", 'rb') as fh:
                    data = fh.read()
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(data)
            except:
                print("error open file ",  traceback.print_exc())
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes("Error open img", "utf8"))
        elif("/getOneFace" == path):  # deleteFace
            query = parsed_path.query
            print("query=", query)
            answer = "{\"getFaceResult\":["
            try:
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                listFiles = []
                for dirname, dirnames, filenames in os.walk('./faces', topdown=False):
                    for filename in filenames:
                        name = filename.split('_')
                        key = name[0] + "_" + name[1]
                        if(key == query):
                            listFiles.append(filename)
                print("listFiles=", listFiles)
                strFiles = ','.join('"' + item + '"' for item in listFiles)
                answer += strFiles + "]}"
                print("listPhotos=" + answer)
                self.wfile.write(bytes(answer, "utf8"))
            except:
                print("error get list images for person")
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                answer += "]}"
                self.wfile.write(bytes(answer, "utf8"))
        elif("/getFaces" == path):  # deleteFace
            answer = "{\"getFacesResult\":"
            try:
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                listNames = defaultdict(list)
                for dirname, dirnames, filenames in os.walk('./faces', topdown=False):
                    for filename in filenames:
                        name = filename.split('_')
                        key = name[0] + "_" + name[1]
                        listNames[key].append(filename)
                answer += json.dumps(listNames) + "}"
                print("listPhotos=" + answer)
                self.wfile.write(bytes(answer, "utf8"))
            except:
                print("error get list images")
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                answer += "{}}"
                self.wfile.write(bytes(answer, "utf8"))
        elif("/favicon.ico" in path):
            self.end_headers()
        elif("/clearLog" == path):
            answer = "{\"Result\":"
            try:
                num = str(randint(100000, 1000000))
                os.replace(rootPath + "/log/server.log", rootPath + "/log/server_" + num + ".log")
                answer += "\"ok\",\"Type\":\"info\"}"
                print("answer=", answer)
                self.wfile.write(bytes(answer, "utf8"))
            except:
                answer += "\"File does not exist.\",\"Type\":\"danger\"}"
                print("error delete image=",  traceback.print_exc())
                self.wfile.write(bytes(answer, "utf8"))
        else:
            print("404 get can not find file " + self.path)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes("404! File not found.", "utf8"))
        return


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


if __name__ == '__main__':
    try:
        server = ThreadedHTTPServer(('localhost', PORT_NUMBER), myHandler)
        # print('Starting cameras processes')
        # p = Process(target=camera_detection, args=('bob',))
        # p.start()
        # cameras.append(p)
        # p.join()
        print('Starting server, use <Ctrl-C> to stop. Port:', PORT_NUMBER)
        server.serve_forever()

    except KeyboardInterrupt:
        print("Stop cmd received, shutting down the web server")
        server.socket.close()
