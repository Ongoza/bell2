import numpy as np
import cv2
import os
import random

# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture("rtsp://os:Bluher11_@192.168.1.108:554")
ramp_frames = 20
location = os.getcwd()  # get present working directory location here

dig = str(random.randint(10000, 1000000))
abs_file_path = os.path.join(location, "pic_" + dig + ".png")
print("opened=" + str(cap.isOpened()))


def get_image():
    # read is the easiest way to get a full image out of a VideoCapture object.
    retval, im = cap.read()
    return im


if(cap.isOpened()):
    for i in range(ramp_frames):
        temp = get_image()
    print("Taking image...")
    # Take the actual image we want to keep
    camera_capture = get_image()
    cv2.imwrite(abs_file_path, camera_capture)

    # Capture frame-by-frame
    while(True):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('frame', gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
else:
    print("no cameras")
