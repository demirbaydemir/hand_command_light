import cv2
import time
import numpy as np 
import hand_tracking_module as htm 
import math
from pyfirmata import Arduino, util 
from time import sleep
########################################
wCam, hCam, = 640, 480
########################################


port = 'COM8'
pin = 8
board = Arduino(port)

ext = False
num = 1


cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.9)
#ortamdaki isiga gore ayarla sunu (detectionCon=0.9)



while True:
    _, img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findPosition(img, draw=False)
    if len(lmlist) !=0:
        #print(lmlist[4], lmlist[8])

        x1, y1 = lmlist[4][1], lmlist[4][2]
        x2, y2 = lmlist[12][1], lmlist[12][2]
        cx, cy = (x1 + x2)//2, (y1 + y2)//2


        cv2.circle(img, (x1,y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2,y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (255, 0, 255), 3)
        cv2.circle(img, (cx,cy), 7, (255, 0, 255), cv2.FILLED)

        lenght = math.hypot(x2 - x1, y2 - y1)

        if lenght < 30:
            ext = True        
        elif lenght > 30:
            ext = False
              
        if num == -1: 
            board.digital[8].write(1)
        elif num == 1:
            board.digital[8].write(0)


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (10,70), cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)

    cv2.imshow("Img", img)
    cv2.waitKey(1)