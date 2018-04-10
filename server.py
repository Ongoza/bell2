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
import logging

PORT_NUMBER = 8080
rootPath = os.path.dirname(os.path.abspath(__file__))
cameras = []
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
streamHandler = logging.StreamHandler()
streamHandler.setFormatter(formatter)
log = logging.getLogger('WebServer')
fileHandler1 = logging.FileHandler('log/webServer.log', mode='a+')
fileHandler1.setFormatter(formatter)
log.setLevel("DEBUG")
log.addHandler(fileHandler1)
log.addHandler(streamHandler)

log.info("starting web server")
# This class will handles any incoming request from
# the browser


def camera_detection(name):
    print("start camera ", name)


def showImg(self):
    filename = rootPath + self.path
    try:
        with open(filename, 'rb') as fh:
            data = fh.read()
        self.send_header('Content-type', 'image/jpeg')
        self.end_headers()
        self.wfile.write(data)
    except:
        log.error("".join(traceback.format_stack()))
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes("Error open img", "utf8"))
    return


def showLog(self):
    filename = rootPath + self.path
    try:
        with open(filename, 'rb+') as fh:
            data = fh.read()
        # print("data=", filename, "\n=", data.decode('utf-8'))
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(data)
    except:
        log.error("".join(traceback.format_stack()))
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes("Error open log", "utf8"))
    return


class myHandler(BaseHTTPRequestHandler):

    # Handler for the GET requests
    def do_POST(self):
        log.info("start post request " + str(self.path))
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
            answer = "{\"uploadRecognation\":"
            try:
                file_data = form['file']
                fileName = file_data.filename
                file_type = text = file_data.type.split('/')
                file_data = file_data.file.read()
                file_len = len(file_data)
                # print("formName=", file_type[0], " fileNa=",  fileName, " fileSize=", file_len)
                if (file_len < 2000000):
                    if(file_type[0] == 'image'):
                        strTime = str(int(round(time.time() * 1000)))
                        newName = "./resultFaces/result_" + strTime + "." + file_type[1]
                        # print("start save image 0 time=", strTime, newName)
                        pathFile = "./forRecognation/" + fileName
                        baseWidth = 1000
                        baseWidthDelta = baseWidth * 1.2
                        pil_image = Image.open(io.BytesIO(file_data))
                        if(baseWidthDelta < pil_image.size[0]):
                            # scale image to 1000px width
                            wPercent = (baseWidth / float(pil_image.size[0]))
                            hsize = int((float(pil_image.size[1]) * float(wPercent)))
                            # print("scale to ", baseWidth, hsize)
                            pil_image = pil_image.resize((baseWidth, hsize), Image.ANTIALIAS)
                        pil_image.save(pathFile)
                        # with open(pathFile, "wb+") as f:
                        #     f.write(file_data)
                        # try:
                        # print("save ready 1 time=", str(int(round(time.time() * 1000))))
                        mainFace.loadLocalData()
                        # print("save ready 2 time=", str(int(round(time.time() * 1000))))
                        res = mainFace.findFace(pathFile, newName)
                        # print("send ready 3 time=", str(int(round(time.time() * 1000))))
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
                log.error("".join(traceback.format_stack()))
                answer += "\"Error file type\",\"Type\":\"danger\"}"
            log.debug(answer)
            self.wfile.write(bytes(answer, "utf8"))
        elif("/upload" == self.path):
            # print("start upload")
            answer = "{\"UploadPhoto\":"
            try:
                file_data = form['file']
                fileName = form.getvalue('fileName')
                file_type = file_data.type.split('/')
                file_data = file_data.file.read()
                file_len = len(file_data)
                # print("formName=", file_type[0], " fileName=", fileName, " fileSize=", file_len)
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
                # print("error sace file",  traceback.print_exc())
                log.error("".join(traceback.format_stack()))
                answer += "\"Error file type\",\"Type\":\"danger\"}"
            log.debug(answer)
            self.wfile.write(bytes(answer, "utf8"))
        elif("/updateFace" == self.path):
            # print("start updateFace")
            answer = "{\"resultUpdate\":"
            try:
                fileName = form.getvalue('fileName')
                # print(form)
                ffile = form.getvalue('file')
                fileOld = form.getvalue('fileOld')
                filesList = form.getvalue('filesList')
                # print("filesList", filesList)
                if (ffile):
                    file_type = file_data.type.split('/')
                    file_data = file_data.file.read()
                    file_len = len(file_data)
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
                log.error("".join(traceback.format_stack()))
                answer += "\"Error update face\",\"Type\":\"danger\"}"
            log.debug(answer)
            self.wfile.write(bytes(answer, "utf8"))
        elif("/updateCamera" == self.path):
            answer = "{\"updateCameraResult\":"
            # Not finished yet!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            try:
                answer += "\"ok\",\"Type\":\"info\"}"
                log.debug(answer)
                self.wfile.write(bytes(answer, "utf8"))
            except:
                answer += "\"File does not exist.\",\"Type\":\"danger\"}"
                log.error("".join(traceback.format_stack()))
                self.wfile.write(bytes(answer, "utf8"))
        elif("/deleteFace" == self.path):
            answer = "{\"deleteFacesResult\":"
            try:
                name = form['name'].value
                path = rootPath + "/faces/" + name
                os.remove(path)
                answer += "\"ok\",\"name\":\"" + name + "\",\"Type\":\"info\"}"
                log.debug(answer)
                self.wfile.write(bytes(answer, "utf8"))
            except:
                answer += "\"File does not exist.\",\"Type\":\"danger\"}"
                log.error("".join(traceback.format_stack()))
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

                # print("camIP=", camIP)
                answer += "\"ok\",\"name\":\"" + camIP + "\",\"Type\":\"info\"}"
                log.debug(answer)
                self.wfile.write(bytes(answer, "utf8"))
            except:
                answer += "\"Can not connect to camera.\",\"Type\":\"danger\"}"
                log.error("".join(traceback.format_stack()))
                self.wfile.write(bytes(answer, "utf8"))
        elif("/deleteCamConfig" == self.path):
            answer = "{\"deleteCamConfigResult\":"
            try:
                name = form['name'].value
                answer += "\"ok\",\"name\":\"" + name + "\",\"Type\":\"info\"}"
                log.debug(answer)
                self.wfile.write(bytes(answer, "utf8"))
            except:
                answer += "\"File does not exist.\",\"Type\":\"danger\"}"
                log.error("".join(traceback.format_stack()))
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
                log.debug(answer)
                self.wfile.write(bytes(answer, "utf8"))
            except:
                answer += "\"Can not add to cam config.\",\"Type\":\"danger\"}"
                log.error("".join(traceback.format_stack()))
                self.wfile.write(bytes(answer, "utf8"))
        else:
            answer = "{urlNotFound:\"Url is not exist.\",\"Type\":\"danger\"}"
            log.error("404 can not path=" + str(self.path))
            self.wfile.write(bytes(answer, "utf8"))

    def do_GET(self):
        # print("photos=", )
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        log.info("Start Get request " + str(self.path))
        self.send_response(200)
        if("/faces" in path):
            showImg(self)
        if("/stream" in path):
            try:
                # vlc rtsp://os@Bluher11_@192.168.1.108:554
                # rtsp://os:Bluher11_@192.168.1.108:554/cam/realmonitor?channel=1&subtype=0
                # rtsp://os:Bluher11_@192.168.1.108:554/cam/realmonitor?channel=1&subtype=1
                #strUrl = "rtsp://os:Bluher11_@192.168.1.108:554/cam/realmonitor?channel=1&subtype=1"
                strUrl = 0
                cap = cv2.VideoCapture(strUrl)
                # print("Camera ", cap.isOpened())
                if (cap.isOpened()):
                    self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=--jpgboundary')
                    self.end_headers()
                    # print("Connected to camera 0=")
                    while True:
                        try:
                            retval, im = cap.read()
                            ret, jpg = cv2.imencode('.jpg', im)
                            jpg_bytes = jpg.tobytes()
                            # print("bute ret=", ret)
                            self.wfile.write("--jpgboundary\r\n".encode())
                            self.send_header('Content-type', 'image/jpeg')
                            self.send_header('Content-length', len(jpg_bytes))
                            self.end_headers()
                            self.wfile.write(jpg_bytes)
                            time.sleep(0.5)
                        except:
                            log.error("".join(traceback.format_stack()))
                            with open(rootPath + "/img/error.png", 'rb') as fh:
                                data = fh.read()
                            self.send_header('Content-type', 'image/jpeg')
                            self.end_headers()
                            self.wfile.write(data)
                            break
                        # time.sleep(self.server.read_delay)
                else:
                    log.error("Error connect to camera")
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
                log.error("".join(traceback.format_stack()))
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes("Error open page for connect to camera", "utf8"))
        elif("/img" in path):
            showImg(self)
        elif("/log" in path):
            showLog(self)
        elif("/config" in path):
            filename = rootPath + path
            try:
                with open(filename, 'rb') as fh:
                    data = fh.read()
                # print("data=", data)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(data)
                log.info("return config file")
            except:
                log.error("".join(traceback.format_stack()))
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes("Error open ", "utf8"))
            return
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
                log.error("".join(traceback.format_stack()))
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
                # print("listFiles=", listFiles)
                strFiles = ','.join('"' + item + '"' for item in listFiles)
                answer += strFiles + "]}"
                log.debug(answer)
                self.wfile.write(bytes(answer, "utf8"))
            except:
                log.error("".join(traceback.format_stack()))
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
                log.debug(answer)
                self.wfile.write(bytes(answer, "utf8"))
            except:
                log.error("".join(traceback.format_stack()))
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                answer += "{}}"
                self.wfile.write(bytes(answer, "utf8"))
        elif("/setRecognation" in path):
            query = parsed_path.query
            # print("setRecognation:", query)
            try:
                with open("./config/camConfig.json", 'r') as jsonFile:
                    data = json.load(jsonFile)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes("Ok", "utf8"))
                log.debug(answer)
            except:
                log.error("".join(traceback.format_stack()))
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes("Error open img", "utf8"))
        elif("/favicon.ico" in path):
            self.end_headers()
        elif("/clearLog" == path):
            answer = "{\"Result\":"
            try:
                num = str(randint(100000, 1000000))
                os.replace(rootPath + "/log/server.log", rootPath + "/log/server_" + num + ".log")
                answer += "\"ok\",\"Type\":\"info\"}"
                log.debug(answer)
                self.wfile.write(bytes(answer, "utf8"))
            except:
                answer += "\"File does not exist.\",\"Type\":\"danger\"}"
                log.error("".join(traceback.format_stack()))
                self.wfile.write(bytes(answer, "utf8"))
        else:
            log.error("404 get can not find file " + str(self.path))
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
        log.info('Starting server, use <Ctrl-C> to stop. Port:' + str(PORT_NUMBER))
        server.serve_forever()

    except KeyboardInterrupt:
        log.info("Stop cmd received, shutting down the web server")
        server.socket.close()
