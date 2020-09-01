'''
To be used as a real-time tool for determining if camera input is blurry
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
    blurry = False
    if blur_num < THRESHOLD:
        blurry = True
    return blurry, blur_num

if __name__ == "__main__":
    if(len(sys.argv) > 1):
        PATH = sys.argv[1]
    else:
        PATH = 1

    fvs = FileVideoStream(PATH).start()
    fps = FPS().start()

    while fvs.more():

        frame = fvs.read()
        if frame.all() is not None:
            frame = imutils.resize(frame, width=450)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = numpy.dstack([frame, frame, frame])
        boolean, blurriness = variance_of_laplacian(frame)
        if not boolean:
            TEXT = "Not blurry, press q to quit\n"
            cv2.putText(frame, "{}: {:.2f}".format(TEXT, blurriness), (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 3)
        else:
            TEXT = "Blurry, press q to quit\n"
            cv2.putText(frame, "{}: {:.2f}".format(TEXT, blurriness), (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        fps.update()

    cv2.destroyAllWindows()
    fvs.stop()
