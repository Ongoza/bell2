import cv2
import face_recognition
import os
import time


def loadFaces():
    location_faces = os.path.join(os.getcwd(), "faces/")
    count = 0
    count_err = 0
    for fileName in os.listdir(location_faces):
        abs_file_path = os.path.join(location_faces, fileName)
        try:
            picture = face_recognition.load_image_file(abs_file_path)
            encoding = face_recognition.face_encodings(picture)[0]
            known_face_encodings.append(encoding)
            known_face_names.append(os.path.splitext(fileName)[0])
            count += 1
        except:
            count_err += 1
            print("error open file: <img src=\"faces/" + str(fileName) + "\"/>")
    print("Knowned faces loaded successefull. Faces: " + str(count) + ". Errors: " + str(count_err))


known_face_encodings = []
known_face_names = []
loadFaces()
counter = 0
counterF = 4
startTime = time.time()
font = cv2.FONT_HERSHEY_DUPLEX
cap = cv2.VideoCapture("rtsp://admin:12345qwer@192.168.1.202")
if(cap.isOpened()):
    while(True):
        counterF = -1
        if (counterF > 0):
            time.sleep(0.1)
        else:
            counterF = 4
            ret, frame_sm = cap.read()
            if(ret):
                # frame_sm = cv2.cvtColor(frame_sm, cv2.COLOR_BGR2GRAY)
                frame_sm = cv2.resize(frame_sm, (0, 0), fx=0.5, fy=0.5)
                # frame_sm = cv2.cvtColor(frame_sm, cv2.COLOR_RGB2GRAY)
                # frame_sm = cv2.cvtColor(frame_sm, cv2.COLOR_BGR2RGB)
                haar_face_cascade = cv2.CascadeClassifier('data/haarcascades/haarcascade_frontalface_alt.xml')
                print("test ok 1")
                face_locations = haar_face_cascade.detectMultiScale(frame_sm, scaleFactor=1.1, minNeighbors=5)

                # go over list of faces and draw them as rectangles on original colored
                # for (x, y, w, h) in face_locations:
                #     cv2.rectangle(frame_sm, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # print("new frame ", ret)
                counter += 1
                print("start frame", counter)
                # face_locations = face_recognition.face_locations(frame_sm, 1, 'hog')
                # print("frame 01", counter, time.time() - startTime)
                face_encodings = face_recognition.face_encodings(frame_sm, face_locations)
                # print("number faces", len(face_locations))
                for face_encoding, face_location in zip(face_encodings, face_locations):
                    x, y, w, h = [v for v in face_location]
                    # cv2.rectangle(frame_sm, (left, top), (right, bottom), (0, 0, 255), 2)
                    cv2.rectangle(frame_sm, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding, 0.6)
                    name = "undef"
                    if True in matches:
                        first_match_index = matches.index(True)
                        name = known_face_names[first_match_index]
                    cv2.putText(frame_sm, name, (x + 6, y - 6), font, 0.5, (255, 255, 255), 1)
                    print("detect person " + name)

                #
                #     # Draw a label with a name below the face
                #
                #     cv2.rectangle(frame_sm, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                #     font = cv2.FONT_HERSHEY_DUPLEX
                #     cv2.putText(frame_sm, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)
                cv2.imshow("test", frame_sm)
                # print("show cam 2")
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
