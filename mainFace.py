import face_recognition
import os
from PIL import Image, ImageDraw
import random


def findFace(photo):
    print("start find")
    rel_path = "photos/"
    # get present working directory location here
    location = os.path.join(os.getcwd(), rel_path)
    known_face_encodings = []
    known_face_names = []
    dig = str(random.randint(10000, 1000000))
    print(location)
    for file in os.listdir(location):
        # print(file)
        abs_file_path = os.path.join(location, file)
        print(abs_file_path)
        picture = face_recognition.load_image_file(abs_file_path)
        encoding = face_recognition.face_encodings(picture)[0]
        known_face_encodings.append(encoding)
        known_face_names.append(os.path.splitext(file)[0])
    unknown_image = face_recognition.load_image_file(
        "testPhoto/found_2.jpg")
    face_locations = face_recognition.face_locations(unknown_image)
    face_encodings = face_recognition.face_encodings(
        unknown_image, face_locations)
    pil_image = Image.fromarray(unknown_image)
    # # Create a Pillow ImageDraw Draw instance to draw with
    draw = ImageDraw.Draw(pil_image)
    # # Loop through each face found in the unknown image
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        #     # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(
            known_face_encodings, face_encoding)
        name = "Unknown"
        #     # If a match was found in known_face_encodings, just use the first one.
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
        #     # Draw a box around the face using the Pillow module
        draw.rectangle(((left, top), (right, bottom)),
                       outline=(100, 100, 100))
        #     # Draw a label with a name below the face
        text_width, text_height = draw.textsize(name)
        draw.rectangle(((left, bottom - text_height - 15), (right, bottom)),
                       fill=(100, 100, 100), outline=(100, 100, 100))
        draw.text((left + 6, bottom - text_height - 5),
                  name, fill=(255, 255, 255, 255))
    # # Remove the drawing library from memory as per the Pillow docs
    del draw
    # # Display the resulting image
    # pil_image.show()
    pil_image.save("result_" + dig + ".jpg")
    return "OK"
