#!/usr/bin/python3
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
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
from file_read_backwards import FileReadBackwards
import base64

PORT_NUMBER = 8080
USER_LOGIN = 'demo'
USER_PASS = 'demo'
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
    parsed_path = urlparse(self.path)
    filename = rootPath + parsed_path.path
    query = parse_qs(parsed_path.query)
    # print("\n\n!!!start open==", filename, query, query['start'])
    data = ""
    start = 0
    end = 100
    cnt = 0
    try:
        if(query['start'][0]):
            start = int(query['start'][0])
        if(query['end'][0]):
            end = int(query['end'][0])
    except:
        log.error("can not get query parameters " + str(self.path))
    print("query=", start, end)
    try:
        with FileReadBackwards(filename, encoding="utf-8") as fh:
            for line in fh:
                if(cnt >= start and cnt < end):
                    data += line + "\n"
                cnt += 1
        data += "Total lines===" + str(cnt) + "\n"
        # print(cnt, "data=", filename, "\n=", data)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(str.encode(data))
    except:
        log.error("".join(traceback.format_stack()))
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes("Error open log", "utf8"))
    return


class myHandler(BaseHTTPRequestHandler):

    def do_AUTHHEAD(self):
        self.send_response(200)
        self.send_header('WWW-Authenticate', 'Basic realm="BellRealm"')
        self.send_header('Content-type', 'application/json')
        self.end_headers()

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
        self.send_header('Content-type', 'application/json')
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
                        strTime = str(int(round(time.time() * 100000)))
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
            num = str(int(round(time.time() * 100000)))
            strNum = "face_" + num
            answer = {"UploadPhoto": "Success", "fileId": strNum, "Type": "info"}
            try:
                file_data = form['file']
                fileName = form.getvalue('fileName')
                file_type = file_data.type.split('/')
                file_data = file_data.file.read()
                file_len = len(file_data)
                print("formName=", file_type[0], " fileName=", fileName, " fileSize=", file_len)
                if (file_len < 2000000):
                    if(file_type[0] == 'image'):
                        if(fileName != ""):
                            with open("./faces/" + fileName + "." + file_type[1], "wb+") as f:
                                f.write(file_data)
                        else:
                            answer.update({"UploadPhoto": "Error Photo name type", "Type": "danger"})
                    else:
                        answer.update({"UploadPhoto": "Error file type", "Type": "danger"})
                else:
                    answer.update({"UploadPhoto": "File is bigger then 2MB", "Type": "danger"})
                del file_data
                with open("./config/update/face_" + num, "w+") as f:
                    newTxt = {'type': 'face', 'new': [fileName]}
                    json.dump(newTxt, f2, ensure_ascii=False)
                    # f.write("new;:;" + fileName)
            except:
                # print("error sace file",  traceback.print_exc())
                log.error("".join(traceback.format_stack()))
                answer.update({"UploadPhoto": "Error file type", "Type": "danger"})
            log.debug(answer)
            self.wfile.write(bytes(json.dumps(answer), "utf8"))
        elif("/updateFace" == self.path):
            # print("start updateFace")
            num = str(int(round(time.time() * 100000)))
            strNum = "face_" + num
            answer = {"resultUpdate": "Success", "fileId": strNum, "Type": "info"}
            trOk = 0
            try:
                fileName = form.getvalue('fileName')
                ffile = form.getvalue('file')
                fileOld = form.getvalue('fileOld')
                filesList = form.getvalue('filesList')
                num = str(int(round(time.time() * 100000)))
                print("filesList", ffile)
                if (ffile):
                    print("filesList 1", ffile)
                    file_type = file_data.type.split('/')
                    file_data = file_data.file.read()
                    file_len = len(file_data)
                    if (file_len < 2000000):
                        if(file_type[0] == 'image'):
                            if(fileName != ""):
                                with open("./faces/" + fileName + "." + file_type[1], "wb+") as f:
                                    f.write(file_data)
                                answer['updateFile'] = 'ok'
                            else:
                                answer.update({"UploadPhoto": "Error Photo name type", "Type": "danger"})
                        else:
                            answer.update({"UploadPhoto": "Error file type", "Type": "danger"})
                    else:
                        answer.update({"UploadPhoto": "File is bigger then 2MB", "Type": "danger"})
                    del file_data
                if(fileName != fileOld):
                    filesArr = json.loads(filesList)
                    readyFiles = []
                    for item in filesArr:
                        root, ext = os.path.splitext(item)
                        newFileName = fileName + '_' + num + ext
                        os.replace(rootPath + "/faces/" + root + ext, rootPath + "/faces/" + newFileName)
                        readyFiles.append(newFileName)
                    answer.update({'oldName': filesArr, 'newFiles': readyFiles})
                    with open("./config/update/face_" + num, "w+") as f2:
                        newTxt = {'type': 'face', 'oldName': filesArr, 'newFiles': readyFiles}
                        print("newTxt", newTxt)
                        json.dump(newTxt, f2, ensure_ascii=False)
                        # f.write("update;:;" + fileName + ";:;" + fileOld)
            except:
                log.error("".join(traceback.format_stack()))
                answer.update({"UploadPhoto": "Error update face", "Type": "danger"})
                # answer += "\"Error update face\",\"Type\":\"danger\"}"
            log.debug(answer)
            self.wfile.write(bytes(json.dumps(answer), "utf8"))
        elif("/updateAlert/" == self.path):
            # print("/updateAlert/")
            answer = {}
            num = str(int(round(time.time() * 100000)))
            fileIdStr = "alert_" + num
            try:
                txtData = form.getvalue('body')
                idData = form.getvalue('id')
                actData = form.getvalue('action')
                newName = idData
                if(newName == "new"):
                    newName = num
                with open("./config/alerts.json", 'r') as fh:
                    data = fh.read()
                config = json.loads(data)
                if(actData == 'delete'):
                    del config['alerts'][newName]
                else:
                    newData = json.loads(txtData)
                    config['alerts'].update({newName: newData})
                os.rename('./config/alerts.json', './config/backup/alerts.json.' + num)
                with open('./config/alerts.json', 'w+') as f:
                    json.dump(config, f, ensure_ascii=False)
                answer.update({"updateAlertsResult": "ok", "name": newName, "fileId": fileIdStr, "Type": "info"})
                log.debug(answer)
                with open("./config/update/alert_" + num, "w+") as f2:
                    newTxt = {'type': 'alert', 'update': [newName], 'action': [actData]}
                    json.dump(newTxt, f2, ensure_ascii=False)
                    # f.write("update;:;" + newName)
            except:
                answer.update({"updateAlertsResult": "Error update alerts.json", "fileId": fileIdStr, "Type": "danger"})
                log.error("".join(traceback.format_stack()))
            self.wfile.write(bytes(json.dumps(answer), "utf8"))
        elif("/updateCamera/" == self.path):
            answer = "{\"updateCameraResult\":"
            try:
                with open("./config/camConfig.json", 'rb+') as fh:
                    data = fh.read()
                config = json.loads(data)
                txtData = form.getvalue('body')
                newName = form.getvalue('id')
                newCam = json.loads(txtData)
                num = str(int(round(time.time() * 100000)))
                os.rename('./config/camConfig.json', './config/backup/camConfig.json.' + num)
                config['cameras'].update(newCam)
                with open('./config/camConfig.json', 'w+') as f:
                    json.dump(config, f, ensure_ascii=False)
                answer += "\"ok\",\"name\":\"" + newName + "\",\"fileId\":\"camera_" + num + "\",\"Type\":\"info\"}"
                log.debug(answer)
                self.wfile.write(bytes(answer, "utf8"))
                with open("./config/update/camera_" + num, "w+") as f2:
                    newTxt = {'type': 'camera', 'update': [newName]}
                    json.dump(newTxt, f2, ensure_ascii=False)
                    # f.write("update;:;" + newName)
            except:
                answer += "\"File does not exist.\",\"Type\":\"danger\"}"
                log.error("".join(traceback.format_stack()))
                self.wfile.write(bytes(answer, "utf8"))
        elif("/deleteFace" == self.path):
            answer = "{\"deleteFacesResult\":"
            try:
                name = form['name'].value
                listNames = []
                print("delFace=", name)
                for dirname, dirnames, filenames in os.walk('./faces', topdown=False):
                    for filename in filenames:
                        nameArr = filename.split('_')
                        key = nameArr[0] + "_" + nameArr[1]
                        if(key == name):
                            print("del=", filename)
                            os.remove("./faces/" + filename)
                            listNames.append(filename)
                num = str(int(round(time.time() * 100000)))
                answer += "\"ok\",\"name\":\"" + name + "\",\"fileId\":\"face_" + num + "\",\"Type\":\"info\"}"
                log.debug(answer)
                self.wfile.write(bytes(answer, "utf8"))
                with open("./config/update/face_" + num, "w+") as f2:
                    newTxt = {'type': 'face', 'delete': listNames}
                    json.dump(newTxt, f2, ensure_ascii=False)
                    # f.write(listNames)
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
            # not ready yet
            try:
                with open("./config/camConfig.json", 'rb+') as fh:
                    data = fh.read()
                config = json.loads(data)
                delName = form.getvalue('body')
                print("delname=", delName)
                num = str(int(round(time.time() * 100000)))
                os.rename('./config/camConfig.json', './config/backup/camConfig.json.' + num)
                del config['cameras'][delName]
                with open('./config/camConfig.json', 'w+') as f:
                    json.dump(config, f, ensure_ascii=False)
                answer += "\"ok\",\"name\":\"" + delName + "\",\"fileId\":\"camera_" + num + "\",\"Type\":\"info\"}"
                log.debug(answer)
                self.wfile.write(bytes(answer, "utf8"))
                with open("./config/update/camera_" + num, "w+") as f2:
                    newTxt = {'type': 'camera', 'delete': [delName]}
                    json.dump(newTxt, f2, ensure_ascii=False)
                    # f.write("delete;:;" + delName)
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
                newName = str(randint(1000000, 10000000))
                num = str(int(round(time.time() * 100000)))
                os.rename('./config/camConfig.json', './config/backup/camConfig.json.' + num)
                config['cameras'].update({newName: newCam})
                with open('./config/camConfig.json', 'w+') as f:
                    json.dump(config, f, ensure_ascii=False)
                answer += "\"ok\",\"name\":\"" + newName + "\",\"fileId\":\"camera_" + num + "\",\"Type\":\"info\"}"
                log.debug(answer)
                self.wfile.write(bytes(answer, "utf8"))
                with open("./config/update/camera_" + num, "w+") as f2:
                    newTxt = {'type': 'camera', 'new': [newName]}
                    json.dump(newTxt, f2, ensure_ascii=False)
                    # f.write("new;:;" + newName)
            except:
                answer += "\"Can not add to cam config.\",\"Type\":\"danger\"}"
                log.error("".join(traceback.format_stack()))
                self.wfile.write(bytes(answer, "utf8"))
        else:
            answer = "{urlNotFound:\"Url is not exist.\",\"Type\":\"danger\"}"
            log.error("404 can not path=" + str(self.path))
            self.wfile.write(bytes(answer, "utf8"))

    def do_GET(self):
        key = self.server.get_auth_key()
        print("auth=", self.headers.get('Authorization'))
        self.send_response(200)
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        log.info("Start Get request " + str(self.path))
        print("get key=", key, self.headers.get('Authorization'))
        # ''' Present frontpage with user authentication. '''
        if("/faces" in path):
            showImg(self)
        elif("/log/img/" in path):
            showImg(self)
        elif("/img/" in path):
            showImg(self)
        elif("/login/" in path):
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            query = parse_qs(parsed_path.query)
            user_id = ''
            user_pass = ''
            print("\n\n!!!start open==", query)
            try:
                if(query['id'][0]):
                    user_id = query['id'][0]
                if(query['pass'][0]):
                    user_pass = query['pass'][0]
            except:
                log.error("can not get query parameters " + str(self.path))
            print("id=", user_id, user_pass)
            if(user_id == USER_LOGIN and user_pass == USER_PASS):
                response = {'success': True, 'key': str(key)}
                self.wfile.write(bytes(json.dumps(response), 'utf-8'))
            else:
                response = {'success': False, 'error': 'User is not exist!'}
                self.wfile.write(bytes(json.dumps(response), 'utf-8'))
        elif self.headers.get('Authorization') == None:
            print("start none")
            self.do_AUTHHEAD()
            response = {'success': False, 'error': 'No auth header received'}
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes(json.dumps(response), 'utf-8'))
            print("start get ", json.dumps(response))
        elif self.headers.get('Authorization') == 'Basic ' + str(key):
            print("start auth")
            if("/stream" in path):
                try:
                    # vlc rtsp://os@Bluher11_@192.168.1.108:554
                    # rtsp://os:Bluher11_@192.168.1.108:554/cam/realmonitor?channel=1&subtype=0
                    # rtsp://os:Bluher11_@192.168.1.108:554/cam/realmonitor?channel=1&subtype=1
                    # strUrl = "rtsp://os:Bluher11_@192.168.1.108:554/cam/realmonitor?channel=1&subtype=1"
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
            # elif("/ifupdate/" in path):
            #     filename = rootPath + '/config/updated/' + path
            #     self.send_header('Content-type', 'Content-type', 'application/json')
            #     self.end_headers()
            #     try:
            #         result = "False"
            #         if filename.exists():
            #             result = "True"
            #         print("check result = " + result)
            #         self.wfile.write(bytes("{\"name\":\"" + path + "\",\"ifupdate\":\"" + result + "\",\"success\":\"true\"}", "utf8"))
            #     except:
            #         # log.error("".join(traceback.format_stack()))
            #         self.wfile.write(bytes("{\"name\":\"" + path + "\",\"ifupdate\":\"" + result + "\",\"success\":\"error\"}", "utf8"))
            elif("/log/" in path):
                showLog(self)
            elif("/config/" in path):
                filename = rootPath + path
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                try:
                    with open(filename, 'rb') as fh:
                        data = fh.read()
                    # print("data=", data)
                    self.wfile.write(data)
                    log.info("return config file")
                except:
                    # log.error("".join(traceback.format_stack()))
                    self.wfile.write(bytes("{\"success\":\"Error open\"}", "utf8"))
                return
            elif("/resultFaces" in path):
                showImg(self)
            elif("/getCamConfig/" in path):
                print("!!!!/ getCamConfig /")
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                try:
                    with open("./config/camConfig.json", 'rb') as fh:
                        data = fh.read()
                    self.wfile.write(data)
                except:
                    log.error("".join(traceback.format_stack()))
                    self.wfile.write(bytes("{\"success\":\"Error open config\"}", "utf8"))
            elif("/getAlerts/" in path):
                # print("!!!!/ getAlerts /")
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                data = 0
                try:
                    with open("./config/alerts.json", 'rb') as fh:
                        data = fh.read()
                except:
                    log.error("".join(traceback.format_stack()))
                    data = bytes("{\"success\":\"Error open alert config\"}", "utf8")
                # print("getAlertData=", data)
                self.wfile.write(data)
            elif("/getOneFace" == path):  # deleteFace
                query = parsed_path.query
                print("query=", query)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                try:
                    listFiles = []
                    for dirname, dirnames, filenames in os.walk('./faces', topdown=False):
                        for filename in filenames:
                            name = filename.split('_')
                            key = name[0] + "_" + name[1]
                            if(key == query):
                                listFiles.append(filename)
                    # print("listFiles=", listFiles)
                    answer = json.dumps({"getFaceResult": listFiles})
                    log.debug(answer)
                except:
                    log.error("".join(traceback.format_stack()))
                    answer = json.dumps({"getFaceResult": []})
                self.wfile.write(bytes(answer, "utf8"))
            elif("/getFaces/" == path):  # deleteFace
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                try:
                    listNames = defaultdict(list)
                    for dirname, dirnames, filenames in os.walk('./faces', topdown=False):
                        for filename in filenames:
                            name = filename.split('_')
                            key = name[0] + "_" + name[1]
                            listNames[key].append(filename)
                    answer = json.dumps({"getFacesResult": listNames})
                    log.debug(answer)
                except:
                    log.error("".join(traceback.format_stack()))
                    answer = json.dumps({"getFacesResult": []})
                self.wfile.write(bytes(answer, "utf8"))
            # elif("/setRecognation" in path):
            #     query = parsed_path.query
            #     self.send_header('Content-type', 'application/json')
            #     self.end_headers()
            #     print("setRecognation:", query)
            #     try:
            #         with open("./config/camConfig.json", 'r') as jsonFile:
            #             data = json.load(jsonFile)
            #         self.send_header('Content-type', 'text/html')
            #         self.end_headers()
            #         self.wfile.write(bytes("Ok", "utf8"))
            #         log.debug(answer)
            #     except:
            #         log.error("".join(traceback.format_stack()))
            #         self.send_header('Content-type', 'text/html')
            #         self.end_headers()
            #         self.wfile.write(bytes("Error open img", "utf8"))
            elif("/favicon.ico" in path):
                self.end_headers()
            elif("/clearLog/" == path):
                self.send_header('Content-type', 'application/json')
                self.end_headers()
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
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                log.error("404 get can not find file " + str(self.path))
                self.wfile.write(bytes("{\"Result\":\"404! File not found.\"}", "utf8"))
        else:
            print("start none else")
            self.do_AUTHHEAD()
            response = {'success': False, 'error': 'Invalid credentials'}
            self.wfile.write(bytes(json.dumps(response), 'utf-8'))
            print(json.dumps(response))
            return


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""
    key = ''

    def __init__(self, address, handlerClass=myHandler):
        super().__init__(address, handlerClass)

    def set_auth(self, username, password):
        self.key = base64.b64encode(bytes('%s:%s' % (username, password), 'utf-8')).decode('ascii')

    def get_auth_key(self):
        return self.key


if __name__ == '__main__':
    try:
        listDirs = ['config/', 'config/update/', 'config/backup/', 'config/updated/',
                    'faces/', 'log/', 'log/img/', 'img/', 'forRecognation/', 'resultFaces/']
        for directory in listDirs:
            if not os.path.exists(directory):
                print("create new dir " + directory)
                os.makedirs(directory)
        server = ThreadedHTTPServer(('localhost', PORT_NUMBER), myHandler)
        server.set_auth(USER_LOGIN, USER_PASS)
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
