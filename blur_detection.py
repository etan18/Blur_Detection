import cv2
import time
import matplotlib.pyplot as plt
import numpy as np
from imutils import paths
import ffmpeg_streaming
import sys
import imutils
from imutils.video import FileVideoStream
from imutils.video import FPS

# CAM = "/Users/ErinTan/Projects/SMI_Pupillometry/V1219_20850228_234726_Dilation2.mp4"
Threshold=200 #notime

#images and threshold for how blurry is really blurry
#sepereate main function?
def variance_of_laplacian(image):
    start = time.time()


    #put checkpoint for finding time after this and after image is outputted
        #make constants start w/ capital(use pylint to make sure)

    #might need to change, put in beginning of code/before function
        #converts to gray
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    small = cv2.resize(gray, (0,0), fx=0.5, fy=0.5)

 #let erin handle this?? **
        #variance of laplacian
#bluriness = cv2.Laplacian(gray, cv2.CV_64F).var()#second partial derivative of x/y direction
#replacement for .var()?
#make image smaller? crop image to just the pupil/ approximately
#CONTOURS= SLOW.
#resize+make threshold lower or crop out (u can control during data collectio)
#code that finds estimated circles???
    bluriness = cv2.Laplacian(small, cv2.CV_64F).var()

    blurry = 0
        # if the focus measure is less than the supplied threshold,
        # then the image should be considered "blurry"
    if bluriness < Threshold:
        blurry=1

    end =time.time()
    print(end-start)

if __name__ == "__main__":
    fvs = FileVideoStream(1).start()
    time.sleep(1)

    fps = FPS().start()

    while fvs.more():
        frame = fvs.read()
        frame = imutils.resize(frame, width=450)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = np.dstack([frame, frame, frame])

        blurriness = variance_of_laplacian(frame)

        if blurry==1:
            text="Blurry"
        if blurry==0:
            text="Not Blurry"
        cv2.putText(gray, "{}: {:.2f}".format(text, bluriness), (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        fps.update()

cv2.destroyAllWindows()
fvs.stop()
