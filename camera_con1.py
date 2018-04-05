import numpy as np
import cv2
import os
import random
import face_recognition

cap = 0
ramp_frames = 20
location = os.getcwd()  # get present working directory location here
known_face_encodings = []
known_face_names = []


def loadLocalData():
    # get present working directory location here
    global known_face_encodings, known_face_names
    location_faces = os.path.join(location, "faces/")
    print("location:", location_faces)
    count = 0
    for file in os.listdir(location_faces):
        # print(file)
        abs_file_path = os.path.join(location_faces, file)
        print("abs_file_path:", abs_file_path)
        try:
            picture = face_recognition.load_image_file(abs_file_path)
            encoding = face_recognition.face_encodings(picture)[0]
            known_face_encodings.append(encoding)
            known_face_names.append(os.path.splitext(file)[0])
            count += 1
        except:
            print("error open file")
    print("Knowned faces loaded successefull. Count=" + str(count))
    return


def get_image():
    # read is the easiest way to get a full image out of a VideoCapture object.
    retval, im = cap.read()
    im_sm = cv2.resize(im, (0, 0), fx=0.25, fy=0.25)
    # im_sm_rgb = im_sm[:, :, ::-1]
    return im_sm


def start_camera(url):
    global cap
    start_counter = 4
    counter = start_counter
    print("start camera")
    cap = cv2.VideoCapture(url)
    print("opened=" + str(cap.isOpened()))
    if(cap.isOpened()):
        # for i in range(ramp_frames):
        #     temp = get_image()
        # print("Taking image...")
        # Take the actual image we want to keep
        # camera_capture = get_image()
        # cv2.imwrite(abs_file_path, camera_capture)

        # Capture frame-by-frame
        while(True):
            if(counter > 0):
                counter -= 1
            else:
                counter = start_counter
                ret, frame_sm = cap.read()
                if(ret):
                    # frame_sm = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
                    face_locations = face_recognition.face_locations(frame_sm)
                    face_encodings = face_recognition.face_encodings(frame_sm, face_locations)
                    face_names = []
                    # print("faces:", len(face_locations))
                    for face_encoding, face_location in zip(face_encodings, face_locations):
                        # See if the face is a match for the known face(s)
                        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                        name = "Unknown"
                        # If a match was found in known_face_encodings, just use the first one.
                        top, right, bottom, left = face_location
                        # print("face location:", left, top, right, bottom)
                        if True in matches:
                            facesFounded = True
                            first_match_index = matches.index(True)
                            name = known_face_names[first_match_index]

                        else:
                            dig = str(random.randint(10000, 1000000))
                            name = "unknown_" + dig
                            delta = 30
                            height, width, channels = frame_sm.shape
                            print("Start add new face", name, width, height)
                            print("face location:", left, top, right, bottom)
                            abs_file_path_save = os.path.join(location, "faces/" + name + ".png")
                            if (top - delta < 0):
                                top = 0
                            if (left - delta < 0):
                                left = 0
                            if (bottom + delta > height):
                                bottom = height
                            if (right + delta > width):
                                right = width
                            crop_img = frame_sm[top:bottom, left:right]
                            height_sm, width_sm, channels_sm = crop_img.shape
                            print("new face location:", left, top, right, bottom)
                            if(height_sm > 0 and width_sm > 0):
                                cv2.imwrite(abs_file_path_save, crop_img)
                            else:
                                print("Error create file with face")
                            known_face_encodings.append(face_encoding)
                            known_face_names.append(name)
                            print("Done add new face")

                        print("face:", name)
                        cv2.rectangle(frame_sm, (left, top), (right, bottom), (0, 0, 255), 2)
                        # Draw a label with a name below the face
                        cv2.rectangle(frame_sm, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                        font = cv2.FONT_HERSHEY_DUPLEX

                        cv2.putText(frame_sm, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

                    cv2.imshow('WebCamera1', frame_sm)
                else:
                    print("can not connect ot camera")
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
    else:
        print("no cameras")


loadLocalData()
# start_camera("rtsp://os:Bluher11_@192.168.1.108:554")
start_camera(0)
