import time

import cv2
import numpy as np

from djitellopy import tello
#connect to the tello (object)
me = tello.Tello()
me.connect()

#print out battery percentage
print(me.get_battery())

#Get Stream
me.streamon()
me.takeoff()
me.send_rc_control(0, 0, 30, 0)
time.sleep(2.2)

w, h = 360, 240
fbRange  = [4200, 4800]
pid = [0.4 , 0.4, 0]
pError = 0

def findFace(img):
    faceCascade = cv2.CascadeClassifier("resources/haarcascade_frontalface_alt.xml")
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #convert color to grayscale
    faces = faceCascade.detectMultiScale(imgGray, 1.2, 8)

    #a list of all faces
    myFaceListC = []  #center point CxCy
    myFaceListArea = []

    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x, y),(x+w, y+h),(0,0,255 ), 2)
        cx = x+w // 2
        cy = y+h // 2
        area = w * h

        cv2.circle(img, (cx,cy), 5, (0,255,0),(cv2.FILLED))
        myFaceListC.append([cx, cy]) #rotate
        myFaceListArea.append(area) # fb inputs

    if len(myFaceListArea) != 0:
        i = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListC[i], myFaceListArea[i]]
        print("发现人脸！")
    else:
        return img, [[0, 0], 0]

#Track face function.
def trackFace( info, w, pid, pError):
    area = info[1]
    x,y = info[0]
    fb = 0

    error = x - w // 2 #Distance away from the center
    speed = pid[0] * error + pid[1] * (error - pError)#pid equation
    speed = int(np.clip(speed, -100, 100)) #speed of our yaw

    #Stationary factor [GREEN ZONE]
    if area > fbRange[0] and area < fbRange[1]:
        fb = 0
    # Move Back [Too Close or Big]
    elif area > fbRange[1]:
        fb = -20
    # Move Forward [Too Far or Small]
    elif area < fbRange[0] and area != 0:
        fb = 20



    if x == 0:
        speed = 0
        error = 0
    print(speed, fb)
    me.send_rc_control(0, fb, 0, speed)
    return error


#Run WebCam
# cap = cv2.VideoCapture(0) #attach the webcam you want to use  0 stands for webcam for testing purposes

while True:
    # _, img = cap.read() #get image
    img = me.get_frame_read().frame
    img = cv2.resize(img, (w,h))
    img, info = findFace(img)
    pError = trackFace( info, w, pid, pError)
    # print("Centre:", info[0], "Area:", info[1])
    cv2.imshow("Output", img)
    # Landing  - Tello
    if cv2.waitKey(1) & 0xFF == ord('q'):
        me.land()
        cv2.destroyAllWindows()
        break

