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
    try:
        for strName in time_files:
            path = "./config/update/" + strName
            log1.info("update config from file=" + path)
            action_type = strName[0: strName.index('_')]
            tr_cam = False
            try:
                with open(path, "r") as f:
                    for line in f:
                        actionArr = line.rstrip("\n").split(';:;')
                        strText = action_type + '_' + actionArr[1]
                        list_updated.append(strText)
                        if(action_type == 'face'):
                            tr_cam = True
                        elif(action_type == 'camera'):
                            tr_cam = True
                        else:
                            log.error("can not recogize command: " + strName)

                if(tr_cam):
                    load_config()
                    print("start camera")
                    # stop_cam(name, True)
                    # print("line4=", list_updated)
                # os.remove(path)
                os.rename(path, "./config/updated/" + strName)
            except:
                log1.error("can load file " + strName)
    except:
        log1.error("can load updates ")


def stop_cam(name, restart):
    try:
        if(threads[name]):
            if(restart):
                threads[name] = threads[name].restart()
            else:
                threads[name].stop()
                del threads[name]
            log1.info("was stopped camera:" + name)
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
    url = cam + value["Port"]
    if(value["Recognation"].lower() == "true"):
        log1.info("Try open camera " + url)
        if(values["Port"] == ""):
            url = int(cam)
        name = values["Name"]
        # c = camera.Camera(name, url)
        # c.start()
        # threads[name] = c
        log1.info("Started camera " + url)


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
    # for dirname, dirnames, filenames in os.walk('./config/update/', topdown=False):
    #     for filename in filenames:
    #         path = "./config/update/" + filename
    #         os.remove(path)
    # load config
    load_config()
    # print("config", config)
    if 'cameras' in config:
        for cam in config['cameras']:
            start_cam(cam)
        check_update()
        while 1:
            time.sleep(60)
            # check_update()
            pass
        # print("main running ", len(threads), threads[0].name)
    else:
        log1.error("can not open config file ")

except KeyboardInterrupt:
    size = len(threads) - 1
    log1.info("\n Stopping active cameras: " + str(size + 1))
    for name, cameraObj in threads:
        print("stoping=", x)
        print("kill=", name)
        stop_cam(name, False)
    log1.info("End keyboard stop main cam manager")
