"""
Tells whether video input is in focus in real time
"""
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

def blur_output(bool_blur, int_blur):
    """Prints green window for not blurred, red for blurred plus numeral"""
     # Create black blank image
    image = np.zeros((100, 100, 3), np.uint8)
    if bool_blur:
        # Fill image with green color
        image[:] = (0, 255, 0)
    else:
        image[:] = (0, 0, 255)
        print(int_blur)

    cv2.namedWindow('light', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('light', image)
    cv2.waitKey(0)

# def variance_of_laplacian(image):
#     """ code to determine how blurry something is """
#
# 	# compute the Laplacian of the image and then return the focus
# 	# measure, which is simply the variance of the Laplacian
#     threshold = 100
#
# 	# might need to change
#     # converts to gray
#     # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#
#     # variance of laplacian
#     fm = variance_of_laplacian(image)
#     text = "Not Blurry"
#     flag = True
#
# 	# if the focus measure is less than the supplied threshold,
# 	# then the image should be considered "blurry"
#     if fm < threshold:
#         text = "Blurry"
#         flag = False
# 	# show the image
#     cv2.putText(image, "{}: {:.2f}".format(text, fm), (10, 30),
# 				cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
#     blur_output(flag, fm)
#     return cv2.Laplacian(image, cv2.CV_64F).var()

if __name__ == "__main__":
    fvs = FileVideoStream(1).start()
    time.sleep(1)

    fps = FPS().start()

    while fvs.more():
        frame = fvs.read()
        frame = imutils.resize(frame, width=450)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = np.dstack([frame, frame, frame])
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        fps.update()

    cv2.destroyAllWindows()
    fvs.stop()
