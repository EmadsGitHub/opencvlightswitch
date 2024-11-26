import face_recognition
import cv2
import os
import glob
import numpy as np

class SimpleFacerec:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = [] #inititalizes array of matches, empty currently

        # Resize frame for a faster speed
        self.frame_resizing = 0.25

    def load_encoding_images(self, images_path): #pass is directory of my images
        """
        Load encoding images from path
        :param images_path:
        :return:
        """
        # Load Images
        images_path = glob.glob(os.path.join(images_path, "*.*")) #finds matching files

        print("{} encoding images found.".format(len(images_path)))

        # Store image encoding and names
        for img_path in images_path:
            img = cv2.imread(img_path) 
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #converts each image to necesary color scale.

            # Get the filename only from the initial file path.
            basename = os.path.basename(img_path)
            (filename, ext) = os.path.splitext(basename)
            # Get encoding; pass in the image, and number of resamples before matching.
            img_encoding = face_recognition.face_encodings(rgb_img, None, 1)[0]

            # Store file name and file encoding
            self.known_face_encodings.append(img_encoding)
            self.known_face_names.append(filename)
        print("Encoding images loaded")

    def detect_known_faces(self, frame):
        small_frame = cv2.resize(frame, (0, 0), fx=self.frame_resizing, fy=self.frame_resizing)
        # Find all the faces and face encodings in the current frame of video
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        #records the encoding of a detected face, alogn with it's location.

        face_names = []
        for face_encoding in face_encodings:
            # Compare the known encodings provided with the face on camera. Last parameter is 
            # tolerance and can be adjusted
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, 1)
            name = "Unknown"

            #a face distance is a metric similiarity of each given face to the camera'a reading.
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            #argmin takes the array and picks the smallest face distance.
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                #receives the name of the best match through the self.known array of names.
                name = self.known_face_names[best_match_index]
            face_names.append(name)

        # Convert to numpy array to adjust coordinates with frame resizing quickly
        face_locations = np.array(face_locations)
        face_locations = face_locations / self.frame_resizing
        #returns data of name of best match and it's location.
        return face_locations.astype(int), face_names
