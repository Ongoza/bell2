import threading
import time
import os
import logging
import json
import camera

threads = []


class ServiceExit(Exception):
    """
    Custom exception which is used to trigger the clean exit
    of all running threads and the main program.
    """
    pass


def service_shutdown(signum, frame):
    print('Caught signal %d' % signum)
    raise ServiceExit


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

filename = rootPath = os.path.dirname(os.path.abspath(__file__)) + "/config/camConfig.json"
try:
    with open(filename, 'r') as fh:
        data = fh.read()
    config = json.loads(data)
    cameras = config["cameras"]
    log1.info("Successful load config file.")
    for cam in cameras:
        url = cam + cameras[cam]["Port"]
        if(cameras[cam]["Recognation"].lower() == "true"):
            log1.info("Try open camera " + url)
            if(cameras[cam]["Port"] == ""):
                url = int(cam)
            name = cameras[cam]["Name"]
            c = camera.Camera(name, url)
            c.start()
            threads.append(c)
            # camera("rtsp://name:pass@192.168.1.108:554")
except Exception as e:
    print("error open file", e)

try:
    while 1:
        pass
        # print("main running ", len(threads), threads[0].name)

except KeyboardInterrupt:
    size = len(threads) - 1
    log1.info("\n Stopping active cameras: " + str(size))
    for x in range(size, -1, -1):
        print("x=", x, threads[x].name)
        if(threads[x]):
            # print("kill", threads[x].name)
            threads[x]._stopevent.set()
            threads[x].stop()
        del threads[x]
    log1.info("End keyboard stop main cam manager")
