'''
To be used as a real-time tool for determining if camera input is blurry

Created by Erin Tan and Aneesha Kodati as part of the 2020 MCA Mentorship
Program, in collaboration with the Integrative Human Physiology Lab of Rutgers
New Jersey Medical School
'''
import cv2
import numpy as np
import imutils
import sys
from imutils.video import FPS
from imutils.video import FileVideoStream

THRESHOLD = 300

def find_coors(event,x,y,flags,param):
    global mouseX,mouseY
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(gray_frame,(x,y),100,(255,0,0),-1)
        mouseX,mouseY = x,y

def variance_of_laplacian(gray_image):
    '''returns bool True if blurry and associated blurriness factor'''

    small = cv2.resize(gray_image, (0, 0), fx=0.5, fy=0.5)
    blur_num = cv2.Laplacian(small, cv2.CV_64F).var()
    blurry = False
    if blur_num < THRESHOLD:
        blurry = True
    return blurry, blur_num

if __name__ == "__main__":
    if(len(sys.argv) > 1):
        PATH = sys.argv[1]
    else:
        PATH = 1 # default webcam

    fvs = FileVideoStream(PATH).start()
    fps = FPS().start()


    while fvs.more():

        frame = fvs.read()
        if frame.all() is not None:
            frame = imutils.resize(frame, width=450)
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if 'mouseX' and 'mouseY' in globals():
            height,width = gray_frame.shape
            mask = np.zeros((height,width), np.uint8)
            cv2.circle(frame, (mouseX, mouseY), 200, (0, 0, 0), -1)
            _,thresh = cv2.threshold(mask,1,255,cv2.THRESH_BINARY)
            contours = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            #x,y,w,h = cv2.boundingRect(contours[0])
            #cropped_image = masked_data[y:y+h,x:x+w]
            #boolean, blurriness = variance_of_laplacian(cropped_image)
        else:
            boolean, blurriness = variance_of_laplacian(gray_frame)

        # frame = numpy.dstack([frame, frame, frame])

        if not boolean:
            TEXT = "Not blurry, press q to quit\n"
            cv2.putText(gray_frame, "{}: {:.2f}".format(TEXT, blurriness), (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 3)
        else:
            TEXT = "Blurry, press q to quit\n"
            cv2.putText(gray_frame, "{}: {:.2f}".format(TEXT, blurriness), (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
        cv2.imshow("Frame", gray_frame)

        if 'cropped_image' in locals():
            cv2.imshow("circle", cropped_image)

        cv2.setMouseCallback("Frame", find_coors)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        fps.update()

    cv2.destroyAllWindows()
    fvs.stop()
