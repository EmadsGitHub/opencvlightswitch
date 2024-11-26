import numpy as np
import cv2
from simple_facerec import SimpleFacerec
import serial
import time
arduinoData=serial.Serial('com5', 9600)

timeout= 120
last_known_time = time.time() #Variables to initalize time and light states.
light_state = "OFF"

sfr = SimpleFacerec()
sfr.load_encoding_images(r"C:\Users\emad_\OneDrive\Pictures\Images") #folder of images
cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
#loads built in references for face and eye detection
while True:
    ret,frame = cap.read()
    frame = cv2.resize(frame, (0, 0), fx=1, fy=1)

    face_locations, face_names = sfr.detect_known_faces(frame) #receives face name and location
    face_detected = False
    for face_loc, name in zip(face_locations, face_names):
        top, right, bottom, left = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #creates a box around the face location and displays the name
        cv2.rectangle(frame, (right, top), (left, bottom), (255, 0, 0), 5)
        cv2.putText(frame, name, (left, top-10), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        if name in face_names:
            #If the name is in the known names, then send data to the arduino. Also records current time.
            last_known_time = time.time()
            face_detected = True
            if light_state == "OFF":
                cmd='ON'+'\r'
                arduinoData.write(cmd.encode())
                light_state = "ON"
                #light state turns on, which prevents this code from running over and over.
    if face_detected == False:
        current_time = time.time()
        #records current time and checks to see if 2 minutes have passed since it's read a known face.
        if current_time - last_known_time >= timeout:
            if light_state == "ON":
                print("Message Sent") #If so, it sends a command to the arduino and turns off the light.
                cmd='OFF'+'\r'
                arduinoData.write(cmd.encode())
                light_state = "OFF" #this prevents the code from looping over and over.
 

    cv2.imshow('frame', frame) #Optional, if you want a window to see the face detections.

    if cv2.waitKey(1) == ord('q'): #press q to exit out of it.
        cap.release()
        cv2.destroyAllWindows()
        exit()  # Exit the program
        break

cap.release()
cv2.destroyAllWindows()
