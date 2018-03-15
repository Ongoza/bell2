import face_recognition
import os
from PIL import Image, ImageDraw
import random
import sys
import traceback

location = os.path.join(os.getcwd(), "faces/")
known_face_encodings = []
known_face_names = []
# dig = str(random.randint(10000, 1000000))


def loadLocalData():
    # get present working directory location here
    print(location)
    count = 0
    for file in os.listdir(location):
        # print(file)
        abs_file_path = os.path.join(location, file)
        # print(abs_file_path)
        picture = face_recognition.load_image_file(abs_file_path)
        encoding = face_recognition.face_encodings(picture)[0]
        known_face_encodings.append(encoding)
        known_face_names.append(os.path.splitext(file)[0])
        count += 1
    print("Knowned faces loaded successefull. Count=" + str(count))
    return


def findFace(fName, newName):
    print("start find 0 =", fName)
    try:
        unknown_image = face_recognition.load_image_file(fName)
        face_locations = face_recognition.face_locations(unknown_image)
        face_encodings = face_recognition.face_encodings(unknown_image, face_locations)
        pil_image = Image.fromarray(unknown_image)
        # # Create a Pillow ImageDraw Draw instance idth=800px to draw with
        draw = ImageDraw.Draw(pil_image)
        # # Loop through each face found in the unknown image
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            #     # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            #     # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
            #     # Draw a box around the face using the Pillow module
            delta = 20
            draw.rectangle(((left - delta, top - delta), (right + delta, bottom + delta)), outline=(100, 100, 100))
            #     # Draw a label with a name below the face
            text_width, text_height = draw.textsize(name)
            draw.rectangle(((left - delta, bottom - text_height + 20), (right + delta, bottom + delta)),
                           fill=(100, 100, 100), outline=(100, 100, 100))
            draw.text((left + 20, bottom - text_height + 20), name, fill=(255, 255, 255, 255))
        # # Remove the drawing library from memory as per the Pillow docs
        del draw
        # # Display the resulting image
        # pil_image.show()
        # print("start find 2", newName)
        # , dpi=(600, 600)
        pil_image.save(newName)
        return 1
    except:
        print("Error face recognation", traceback.print_exc())
        return 0
