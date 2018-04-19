import threading
import time
import os
import logging
import json
import camera

threads = {}
config = {}


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


def load_config():
    global config
    print("start open config file")
    filename = os.path.dirname(os.path.abspath(__file__)) + "/config/camConfig.json"
    try:
        with open(filename, 'r') as fh:
            data = fh.read()
        config = json.loads(data)
        log1.info("Successful load config file.")
    except:
        log1.error("Can not load config file.")


def start_cam(cam):
    value = config['cameras'][cam]
    try:
        if(value["Recognation"].lower() == "true"):
            url = value["IP"] + ':' + value["Port"]
            log1.info("Try open camera url:" + url)
            name = value["Name"]
            cam_id = url
            if(value["Port"] == '0' or value["Port"] == ''):
                try:
                    url = int(value["IP"])
                except:
                    log1.error("Error start usb camera:" + name + ' url:' + url)
            print("usb=", url)
            c = camera.Camera(name, url)
            c.start()
            threads[cam_id] = c
            log1.info("Try start camera:" + name + ' url:' + str(url))
    except:
        log1.error("Error start camera:" + name + ' url:' + str(url))


def check_active_cams():
    # print("Tik cam")
    for key in list(threads.keys()):
        # print("check=", key, threads[key])
        if(threads[key]):
            if(not threads[key].isActive):
                log1.info("try restart cam: ", threads[key].url)
                threads[key].start()
                # stop_cam(key, False)


try:
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
    listDirs = ['config/', 'config/update/', 'config/updated/', 'faces/', 'log/', 'log/img/', 'img/', 'forRecognation/', 'resultFaces/']
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
    log1.info("End keyboard stop main cam manager")
