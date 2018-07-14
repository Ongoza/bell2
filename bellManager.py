import threading
import time
import os
import logging
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

from bellCamera import BellCamera
from bellServer import BellHandler, BellHTTPServer

# import subprocess
threads = {}
config = {}
addresses = []
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
streamHandler = logging.StreamHandler()
streamHandler.setFormatter(formatter)
log1 = logging.getLogger('Cam_manager')
fileHandler1 = logging.FileHandler('log/camera_manager.log', mode='a+')
fileHandler1.setFormatter(formatter)
log1.setLevel("DEBUG")
log1.addHandler(fileHandler1)
log1.addHandler(streamHandler)
log1.info("start main cam manager")

# fromaddr = 'oleg223171@gmail.com'
# toaddr = ['oleg@ongoza.com']
# password = 'z'


# def sendMsgAlert(text, img_path):
#     print("start send email")
#     try:
#         msg = MIMEMultipart()
#         msg['Subject'] = 'Test'
#         # me == the sender's email address
#         # family = the list of all recipients' email addresses
#         msg['From'] = ', '.join(fromaddr)
#         msg['To'] = ', '.join(toaddr)
#         msg.preamble = 'Multipart massage.\n'
#         part = MIMEText(text)
#         msg.attach(part)
#         if(img_path != ""):
#             with open(img_path, 'rb') as fp:
#               img_data = fp.read()
#             part = MIMEApplication(img_data)
#             part.add_header('Content-Disposition', 'attachment', filename="Photo.png")
#             msg.attach(part)
#         # print("send mail 1")
#         # Send the email via our own SMTP server.
#         with smtplib.SMTP_SSL('smtp.gmail.com:465') as s:
#             s.ehlo()
#             s.login(fromaddr, password)
#             s.send_message(msg)
#             print("send mail")
#     except:
#         print("Error: unable to send email")


# img_data = "img/Oleg_Sylver_0.png"
# img_data = ""
# sendMsgAlert("text ggggg", img_data)


class ServiceExit(Exception):
    """
    Custom exception which is used to trigger the clean exit
    of all running threads and the main program.
    """
    pass


def service_shutdown(signum, frame):
    print('Caught signal %d' % signum)
    raise ServiceExit


def check_update():
    print("start update")
    list_updated = []
    files = os.listdir("./config/update/")
    time_files = sorted(files)
    tr_cam = False
    tr_alert = False
    try:
        for strName in time_files:
            path = "./config/update/" + strName
            log1.info("update config from file=" + path)
            try:
                with open(path, 'r') as fh:
                    data = fh.read()
                jsonData = json.loads(data)
                action_type = jsonData['type']
                list_updated.append(strName)
                if(action_type == 'face'):
                    tr_cam = True
                elif(action_type == 'camera'):
                    tr_cam = True
                elif(action_type == 'alert'):
                    tr_alert = True
                else:
                    log.error("can not recogize command: " + strName)
                    # print("line4=", list_updated)
                # os.remove(path)
                os.rename(path, "./config/updated/" + strName)
            except:
                log1.error("can not load file " + strName)
    except:
        log1.error("can not load updates ")
    if(tr_cam):
        log1.info("Start cameras restarting...")
        load_config()
        stop_cam(name, True)
    if(tr_alert):
        print("start alert update")
        load_alarms()
        for key, item in threads.items():
            print("start alert update for cam ", key)
            item.toaddr = addresses


def stop_cam(name, restart):
    # print(" try start stop ", name)
    try:
        if(threads[name]):
            if(restart):
                threads[name] = threads[name].restart()
                log1.info("Try restart camera:" + name)
            else:
                threads[name].stop()
                threads[name].join()
                del threads[name]
                log1.info("Try stop camera:" + name)
        else:
            print("camera did not start")
            if(restart):
                start_cam(name)
            else:
                log1.error("can not stop/start camera " + name)
    except:
        log1.error("can not stop camera " + name)


def load_alarms():
    global addresses
    # print("start open config file")
    try:
        filename = os.path.dirname(os.path.abspath(__file__)) + "/config/alerts.json"
        with open(filename, 'r') as fh:
            data = fh.read()
        alarms = json.loads(data)
        for key, item in alarms['alerts'].items():
            if (item['Type'] == 'email'):
                if not item['Email'] in addresses:
                    addresses.append(item['Email'])
        log1.info("Successful load config file.", config, alerts)
    except:
        log1.error("Can not load alarms file.")


def load_config():
    global config
    # print("start open config file")
    try:
        filename = os.path.dirname(os.path.abspath(__file__)) + "/config/camConfig.json"
        with open(filename, 'r') as fh:
            data = fh.read()
        config = json.loads(data)
        # log1.info("Successful load config file.", config, alerts)
    except:
        log1.error("Can not load config file.")


def start_cam(cam):
    value = config['cameras'][cam]
    try:
        # log1.info("config " + str(value))
        if(value["Recognation"].lower() == "true"):
            url = 'rtsp://'
            if "Login" in value:
                login = value["Login"].replace(" ", "")
                if(login != ''):
                    url += login + ":" + value["Password"] + "@"
            url += value["IP"] + ':' + value["Port"]
            if "camURL" in value:
                camURL = value["camURL"].replace(" ", "")
                if(camURL != ''):
                    url += "/" + value["camURL"]
            log1.info("Try open camera url:" + url)
            name = value["Location"] + "_" + cam
            cam_id = url
            if(value["Port"] == '0' or value["Port"] == ''):
                try:
                    url = int(value["IP"])
                    print("usb=", url)
                except:
                    log1.error("Error start usb camera:" + name + ' url:' + url)
            c = BellCamera(name, url, addresses)
            c.start()
            threads[cam_id] = c
            log1.info("Try start camera:" + name + ' url:' + str(url))
    except:
        log1.error("Error start camera:" + name + ' url:' + str(url))


def check_active_cams():
    # print("Tik cam")
    for key, item in threads.items():
        # print("check=", key, "=item=", item, "=")
        try:
            if(item):
                # print("check 2 =", key, "=item=", item, "=", item.isActive)
                if(not item.isActive):
                    log1.info("try restart cam: " + str(key))
                    # print("check 3 =", key, "=item=", item, "=")
                    item.start()
                    # stop_cam(key, False)
        except:
            log1.error("Error check camera " + str(key))


if __name__ == '__main__':
    try:
        web_server = BellHTTPServer(('localhost', 8080), BellHandler)
        web_server.set_auth("demo", "demo")
        # print('Starting cameras processes')
        # p = Process(target=camera_detection, args=('bob',))
        # p.start()
        # cameras.append(p)
        # p.join()
        # web_server.serve_forever()
        thread = threading.Thread(target=web_server.serve_forever)
        thread.daemon = True
        thread.start()
        print("!!!!!!!!!!!!")
        listDirs = ['config/', 'config/update/', 'config/backup/', 'config/updated/',
                    'faces/', 'log/', 'log/img/', 'img/', 'forRecognation/', 'resultFaces/']
        for directory in listDirs:
            if not os.path.exists(directory):
                print("create new dir " + directory)
                os.makedirs(directory)
        # clean update data on start
        for dirname, dirnames, filenames in os.walk('./config/update/', topdown=False):
            for filename in filenames:
                path = "./config/update/" + filename
                os.remove(path)
        # load config
        load_alarms()
        load_config()
        # print("config", config)
        if 'cameras' in config:
            for cam in config['cameras']:
                start_cam(cam)
            check_update()
            while 1:
                # print("Tik 0")
                time.sleep(60)
                check_update()
                check_active_cams()
                # pass
            # print("main running ", len(threads), threads[0].name)
        else:
            log1.error("can not open config file ")

    except KeyboardInterrupt:
        size = len(threads) - 1
        log1.info("\n Stopping active cameras: " + str(size + 1))
        for key in list(threads.keys()):
            # print("stoping=", key)
            stop_cam(key, False)
        web_server.socket.close()
        log1.info("End keyboard stop main cam manager")
