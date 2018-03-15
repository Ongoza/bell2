import numpy as np
import cv2
import os
import random

cap = cv2.VideoCapture(0)
ramp_frames = 30
location =  os.getcwd()  # get present working directory location here

dig = str(random.randint(10000, 1000000))
abs_file_path = os.path.join(location, "pic_"+dig+".png")
print ("opened="+str(cap.isOpened()))

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

    # while(True):
    #     # Capture frame-by-frame
    #     ret, frame = cap.read()
    #
    #     # Our operations on the frame come here
    #     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #     if cv2.waitKey(30) & 0xFF == ord('q'): # you can increase delay to 2 seconds here
    #         break
        # Display the resulting frame
        # cv2.imshow('frame',gray)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
else:
    print("no cameras")
