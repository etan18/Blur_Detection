'''
To be used as a real-time tool for determining if camera input is blurry

Created by Erin Tan and Aneesha Kodati as part of the 2020 MCA Mentorship
Program, in collaboration with the Integrative Human Physiology Lab of Rutgers
New Jersey Medical School
'''
import cv2
import numpy
import imutils
import sys
from imutils.video import FPS
from imutils.video import FileVideoStream

THRESHOLD = 300

def variance_of_laplacian(gray_image):
    '''returns bool True if blurry and associated blurriness factor'''

    small = cv2.resize(gray_image, (0, 0), fx=0.5, fy=0.5)
    blur_num = cv2.Laplacian(small, cv2.CV_64F).var()
    isBlurry = False
    if blur_num < THRESHOLD:
        isBlurry = True
    return isBlurry, blur_num

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
        # frame = numpy.dstack([frame, frame, frame])
        boolean, blurriness = variance_of_laplacian(gray_frame)
        if not boolean:
            TEXT = "SHARP Score: \n"
            cv2.putText(frame, "{}: {:.2f}".format(TEXT, blurriness), (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 3)
        else:
            TEXT = "SHARP Score: \n"
            cv2.putText(frame, "{}: {:.2f}".format(TEXT, blurriness), (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
        cv2.imshow("Frame", frame)
        print(blurriness)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        fps.update()

    cv2.destroyAllWindows()
    fvs.stop()
