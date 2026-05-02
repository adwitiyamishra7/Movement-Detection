import sys
import cv2
from datetime import datetime

# // caapture live || 0 default signal h
capt = cv2.VideoCapture(0)

if not capt.isOpened():
     print("the camera cannot be accessed")
     sys.exit()


# implementing bg subtractor
mog = cv2.createBackgroundSubtractorMOG2()




print("TO BREAK CLICK 'q'")

while True:
   
    # will read frames 
    rate,frame = capt.read()

    if not rate:
        print("Failed to grab frame")
        break
    # convert fram to grey scl
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # apply mog
    fgmask = mog.apply(gray)


    # remove noise
    kernal = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6,6))
    fgmask = cv2.erode(fgmask, kernal, iterations=1)
    fgmask = cv2.dilate(fgmask, kernal , iterations=1)

    #capture contours
    contours, hierarchy = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # have to caputure big contour
    for i in contours:
        # have to ignore small contour
        if cv2.contourArea(i) < 500:
            continue

        #if detection found then form rectangle
        x, y , w, h = cv2.boundingRect(i)
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255),2)


        # for the display of time in the frame
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cv2.putText(
        frame,
        current_time, 
        (10,30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0,0,255),
        2
    )

    cv2.imshow('Motion Detection', fgmask)
    cv2.imshow("Motion Detection", frame)
    # cv2.imshow("MOG Mask", fgmask)

    # to break loop ya cam 
    if cv2.waitKey(1) == ord('q'):
        break

# free the cam
capt.release()
cv2.destroyAllWindows()