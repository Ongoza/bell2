import numpy as np
import threading
import cv2
import os
import traceback
import random
import face_recognition
import logging
import sys


class Camera(threading.Thread):
    def __init__(self, name, url):
        self.cameraName = name
        self.log1 = logging.getLogger('Camera_' + self.cameraName)
        self.url = url
        self.cap = 0
        self.delay_before_add = 2  # number of frames with face before add
        self.delay_before_leave = 5  # number of frames with face before leave
        # self.ramp_frames = 20
        self.start_counter = 4  # proceed only each n frame
        self.location = os.getcwd()  # get present working directory location here
        self._stopevent = threading.Event()
        threading.Thread.__init__(self)

    def run(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.detected_faces = {}
        self.detected_faces_new = {}
        self.unknown_face_encodings = []
        self.unknown_face_names = []
        # self.unknown_face_imgs = []
        # self.detected_faces_unknown = {}
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)
        fileHandler1 = logging.FileHandler('log/camera_' + self.cameraName + '.log', mode='a+')
        fileHandler1.setFormatter(formatter)
        self.log1.setLevel("DEBUG")
        self.log1.addHandler(fileHandler1)
        self.log1.addHandler(streamHandler)

        self.log2 = logging.getLogger('Camera_face_' + self.cameraName)
        fileHandler2 = logging.FileHandler('log/camera_' + self.cameraName + '_face.log', mode='a+')
        fileHandler2.setFormatter(formatter)
        self.log2.setLevel("DEBUG")
        self.log2.addHandler(fileHandler2)
        self.log2.addHandler(streamHandler)

        location_faces = os.path.join(self.location, "faces/")
        count = 0
        count_err = 0
        for fileName in os.listdir(location_faces):
            abs_file_path = os.path.join(location_faces, fileName)
            try:
                picture = face_recognition.load_image_file(abs_file_path)
                encoding = face_recognition.face_encodings(picture)[0]
                self.known_face_encodings.append(encoding)
                self.known_face_names.append(os.path.splitext(fileName)[0])
                count += 1
            except:
                count_err += 1
                self.log1.error("error open file: <img src=\"faces/" + str(fileName) + "\"/>")
        self.log1.info("Knowned faces loaded successefull. Faces: " + str(count) + ". Errors: " + str(count_err))
        counter = self.start_counter
        self.log1.info("start camera " + str(self.url))
        self.cap = cv2.VideoCapture(self.url)
        if(self.cap.isOpened()):
            self.log2.info("started camera " + str(self.url))
            while not self._stopevent.isSet():
                try:
                    if(counter > 0):
                        counter -= 1
                    else:
                        counter = self.start_counter
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
                                    name = ""
                                    saveImgPath = ""
                                    if True in matches:
                                        first_match_index = matches.index(True)
                                        name = self.known_face_names[first_match_index]
                                        if(not name in self.detected_faces):
                                            self.log2.info("Detect face " + name)
                                            saveImgPath = "log/img/" + name + ".png"
                                        self.detected_faces[name] = self.delay_before_leave
                                    else:
                                        # new face is detected
                                        name = "unknown_" + str(random.randint(100000, 1000000)) + "_0"
                                        # print("start for unknown " + name)
                                        if(len(self.unknown_face_encodings) > 0):
                                            matches_u = face_recognition.compare_faces(self.unknown_face_encodings, face_encoding, 0.6)
                                            if True in matches_u:
                                                first_match_index_u = matches_u.index(True)
                                                name = self.unknown_face_names[first_match_index_u]
                                                # print("detect name for unknown " + name)
                                                # save photo if present during several frames !!!!!!
                                                self.detected_faces_new[name] = self.detected_faces_new[name] - 1
                                                if(self.detected_faces_new[name] < 0):
                                                    saveImgPath = "faces/" + name + ".png"
                                                    del self.detected_faces_new[name]
                                                    if(name in self.unknown_face_names):
                                                        index = self.unknown_face_names.index(name)
                                                        del self.unknown_face_names[index]
                                                        del self.unknown_face_encodings[index]
                                                    # print("delete unknow==", self.detected_faces_new, "==",
                                                    #       self.unknown_face_names, "==", self.unknown_face_encodings)
                                                    self.detected_faces[name] = self.delay_before_leave
                                                    self.known_face_names.append(name)
                                                    self.known_face_encodings.append(face_encoding)
                                                    self.log2.info("Done add new face " + name)
                                            else:
                                                self.unknown_face_encodings.append(face_encoding)
                                                self.unknown_face_names.append(name)
                                                self.detected_faces_new[name] = self.delay_before_add
                                                self.log2.info("Done 1 add unknown face " + name)
                                        else:
                                            self.unknown_face_encodings.append(face_encoding)
                                            self.unknown_face_names.append(name)
                                            self.detected_faces_new[name] = self.delay_before_add
                                            self.log2.info("Done 2 add unknown face " + name)
                                    face_names.append(name)
                                    if(saveImgPath != ""):
                                        print("start save img " + saveImgPath)
                                        fullPath = os.path.join(self.location, saveImgPath)
                                        top, right, bottom, left = face_location
                                        delta = 60
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
                                        crop_img = frame_sm[top:bottom, left:right]
                                        height_sm, width_sm, channels_sm = crop_img.shape
                                        if(height_sm > 0 and width_sm > 0):
                                            cv2.imwrite(fullPath, crop_img)
                                            self.log2.info("Saved new image " + saveImgPath + " <img src=\"" + saveImgPath + "\"/>")
                                        else:
                                            self.log1.error("Error create file with face " + saveImgPath)
                                    # Draw a label with a name below the face
                                    # cv2.rectangle(frame_sm, (left, top), (right, bottom), (0, 0, 255), 2)
                                    # cv2.rectangle(frame_sm, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                                    # font = cv2.FONT_HERSHEY_DUPLEX
                                    # cv2.putText(frame_sm, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)
                                del_names = []
                                for key, value in self.detected_faces.items():
                                    if (not key in face_names):
                                        if(self.detected_faces[key] > 0):
                                            self.detected_faces[key] = value - 1
                                        else:
                                            del_names.append(key)
                                for i in del_names:
                                    del self.detected_faces[i]
                                    self.log2.info("Leave know face: " + i)
                                del_names2 = []
                                for key2, value2 in self.detected_faces_new.items():
                                    if (not key2 in face_names):
                                        del_names2.append(key2)
                                for j in del_names2:
                                    print("remove 0 start unknow face: ", j, self.detected_faces_new)
                                    del self.detected_faces_new[j]
                                    if(j in self.unknown_face_names):
                                        index = self.unknown_face_names.index(j)
                                        print("remove 1 start unknow face: ", index)
                                        del self.unknown_face_names[index]
                                        print("remove 3 start unknow face: ", index)
                                        del self.unknown_face_encodings[index]
                                    self.log2.info("remove unknow face: " + j)
                            else:
                                del_names = []
                                for key, value in self.detected_faces.items():
                                    if(self.detected_faces[key] > 0):
                                        self. detected_faces[key] = value - 1
                                    else:
                                        del_names.append(key)
                                for i in del_names:
                                    del self.detected_faces[i]
                                    self.log2.info("Leave know face: " + i)
                                if(len(self.detected_faces_new) > 0):
                                    self.detected_faces_new.clear()
                                    del self.unknown_face_names[:]
                                    del self.unknown_face_encodings[:]
                                    print("clear unknown", self.detected_faces_new, self.unknown_face_names, self.unknown_face_encodings)
                            # cv2.imshow(self.cameraName, frame_sm)
                        else:
                            self.log1.error("can not connect ot camera")
                except:  # Exception as e
                    print("stop camera ".join(traceback.format_stack()))
                    # self.stop()
        else:
            self.log1.error("no connected cameras")

    def stop(self):
        self.log1.info("stop 1 camera " + self.cameraName)
        self.log2.info("stop 2 camera " + self.cameraName)
        if(self.cap):
            self.cap.release()
        cv2.destroyAllWindows()
        self.alive = False
        self.join()


Camera("webCamera", 0).start()
