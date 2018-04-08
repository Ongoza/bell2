import numpy as np
import threading
import cv2
import os
import random
import face_recognition
import logging
import sys


class Camera(threading.Thread):
    def __init__(self, name, url):
        self.cameraName = name
        self.url = url
        self.log1 = ""
        self.cap = 0
        self.ramp_frames = 20
        self.location = os.getcwd()  # get present working directory location here
        self.known_face_encodings = []
        self.known_face_names = []
        self.detected_faces = []
        threading.Thread.__init__(self)

    def run(self):
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)

        self.log1 = logging.getLogger('Camera_' + self.cameraName)
        fileHandler1 = logging.FileHandler('log/camera_' + self.cameraName + '.log', mode='a+')
        fileHandler1.setFormatter(formatter)
        self.log1 = logging.getLogger('Camera_' + self.cameraName)
        self.log1.setLevel("DEBUG")
        self.log1.addHandler(fileHandler1)
        self.log1.addHandler(streamHandler)

        self.log2 = logging.getLogger('Camera_face_' + self.cameraName)
        self.log2.setLevel("DEBUG")
        fileHandler2 = logging.FileHandler('log/camera_face_' + self.cameraName + '.log', mode='a+')
        fileHandler2.setFormatter(formatter)
        self.log2.addHandler(fileHandler2)
        self.log2.addHandler(streamHandler)

        location_faces = os.path.join(self.location, "faces/")
        count = 0
        count_err = 0
        for file in os.listdir(location_faces):
            abs_file_path = os.path.join(location_faces, file)
            try:
                picture = face_recognition.load_image_file(abs_file_path)
                encoding = face_recognition.face_encodings(picture)[0]
                self.known_face_encodings.append(encoding)
                self.known_face_names.append(os.path.splitext(file)[0])
                count += 1
            except:
                count_err += 1
                self.log1.error("error open file: " + abs_file_path)
        self.log1.info("Knowned faces loaded successefull. Faces: " + str(count) + ". Errors: " + str(count_err))
        start_counter = 4
        counter = start_counter
        self.log1.info("start camera " + str(self.url))
        self.log2.info("start camera " + str(self.url))
        self.cap = cv2.VideoCapture(self.url)
        self.log1.debug("opened=" + str(self.cap.isOpened()))
        if(self.cap.isOpened()):
            while(True):
                if(counter > 0):
                    counter -= 1
                else:
                    counter = start_counter
                    ret, frame_sm = self.cap.read()
                    if(ret):
                        # frame_sm = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
                        face_locations = face_recognition.face_locations(frame_sm)
                        face_encodings = face_recognition.face_encodings(frame_sm, face_locations)
                        face_names = []
                        # print("faces:", len(face_locations))
                        if (len(face_locations) > 0):
                            for face_encoding, face_location in zip(face_encodings, face_locations):
                                # See if the face is a match for the known face(s)
                                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, 0.6)
                                name = "unknown_"
                                top, right, bottom, left = face_location
                                # print("face location:", left, top, right, bottom)
                                if True in matches:
                                    # facesFounded = True
                                    first_match_index = matches.index(True)
                                    name = self.known_face_names[first_match_index]
                                    if(not name in self.detected_faces):
                                        self.log2.info("Detect face " + name)
                                        self.detected_faces.append(name)
                                else:
                                    delta = 40
                                    height, width, channels = frame_sm.shape
                                    if (top - delta < 0):
                                        top = 0
                                    else:
                                        top = top - delta
                                    if (left - delta < 0):
                                        left = 0
                                    else:
                                        left = left - delta
                                    if (bottom + delta > height):
                                        bottom = height
                                    else:
                                        bottom = bottom + delta
                                    if (right + delta > width):
                                        right = width
                                    else:
                                        right = right + delta
                                    dig = str(random.randint(10000, 1000000))
                                    name = "unknown_" + dig + "_0"
                                    abs_file_path_save = os.path.join(self.location, "faces/" + name + ".png")
                                    crop_img = frame_sm[top:bottom, left:right]
                                    height_sm, width_sm, channels_sm = crop_img.shape
                                    if(height_sm > 0 and width_sm > 0):
                                        cv2.imwrite(abs_file_path_save, crop_img)
                                    else:
                                        self.log1.error("Error create file with face")
                                    self.known_face_encodings.append(face_encoding)
                                    self.known_face_names.append(name)
                                    self.log2.info("Done add new face " + name)
                                face_names.append(name)
                                cv2.rectangle(frame_sm, (left, top), (right, bottom), (0, 0, 255), 2)
                                # Draw a label with a name below the face
                                cv2.rectangle(frame_sm, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                                font = cv2.FONT_HERSHEY_DUPLEX
                                cv2.putText(frame_sm, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)
                            for n in self.detected_faces:
                                if (not n in face_names):
                                    self.detected_faces.remove(n)
                                    self.log2.info("Leave face " + n)
                        else:
                            if(len(self.detected_faces) > 0):
                                self.log2.info("Leave faces " + ",".join(self.detected_faces))
                                del self.detected_faces[:]
                        cv2.imshow(self.cameraName, frame_sm)
                    else:
                        self.log1.error("can not connect ot camera")
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.stop()
                    break
            self.stop()
        else:
            self.log1.error("no cameras")

    def stop(self):
        self.log1.info("stop camera " + self.cameraName)
        self.log2.info("stop camera " + self.cameraName)
        if(self.cap):
            self.cap.release()
        cv2.destroyAllWindows()
        self.alive = False
        self.join()


camera = Camera("webCam_0", 0).start()

# start_camera("rtsp://os:Bluher11_@192.168.1.108:554")
