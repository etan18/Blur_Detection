"""
Valentin Siderskiy 10/22/2019
Integrative Human Physiology Lab
Rutgers University
split.py
This function takes the video input recorded by the
Night Owel Security stystem, splits the left and right
and assigns a timestamp based on the night owel clock.
"""

import sys
import math
import cv2
import matplotlib.pyplot as plt
from find_pupil import pupillometry
import numpy
import pandas as pd
#text
FONT = cv2.FONT_HERSHEY_SIMPLEX
SMI_DIM = (720, 480) # Dimension from SMI System
DEFAULT_FILE_NAME = '/Users/ErinTan/Downloads/pupil_clip1.mp4'


def plot_radial_perimeter(rads, radius, fitted):
    """plots radians over radius for the left and right eye"""
    # plt.subplot(121)
    plt.clf()
    # plt.subplot(121)
    plt.ion()
    plt.axis([-4, 4, 45, 65])
    plt.plot(rads, radius, 'ro', marker=".", markersize=5)
    plt.ylabel('radius (pixels)')
    plt.xlabel('angle (radians)')

    x = numpy.arange(min(rads).astype(int), max(rads).astype(int), 0.1)
    y = numpy.asarray([eval_fitted(fitted, x_num) for x_num in x])
    plt.plot(x, y)
    plt.show()
    plt.pause(0.05)

def eval_fitted(fitted, x):
    x7 = fitted[0] * (x**7)
    x6 = fitted[1] * (x**6)
    x5 = fitted[2] * (x**5)
    x4 = fitted[3] * (x**4)
    x3 = fitted[4] * (x**3)
    x2 = fitted[5] * (x**2)
    x1 = fitted[6] * x
    x0 = fitted[7]
    return x7+x6+x5+x4+x3+x2+x1+x0


def resize_with_aspect_ratio(image, width=None, height=None, inter=cv2.INTER_AREA):
    """Resizes image to particular width or height but keeps aspect ratio"""
    dim = None
    (image_h, image_w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        ratio = height / float(image_h)
        dim = (int(image_w * ratio), height)
    else:
        ratio = width / float(image_w)
        dim = (width, int(image_h * ratio))

    return cv2.resize(image, dim, interpolation=inter)

def display_main(frame, cap):
    """Display Main"""
    fcount = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    resized_frame = resize_with_aspect_ratio(frame, width=640) #Resize by
    # resized_frame = ResizeWithAspectRatio(frame, height = 480)

    frame_position = cap.get(cv2.CAP_PROP_POS_FRAMES)
    fp_string = "Frame " + str(frame_position) + '/' + str(fcount)
    cv2.putText(resized_frame, fp_string, (230, 350), FONT, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
    # pylint: disable=C0103
    QUIT_STRING = "Press Q to Quit"
    cv2.putText(resized_frame, QUIT_STRING, (230, 250), FONT, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

    # Display the resulting frame
    cv2.imshow('Frame', resized_frame)
    #cv2.waitKey(0)

def best_fit(rads, radius):
    fitted = numpy.polyfit(rads, radius, 7)
    #print('best fit: ', fitted)
    differences=[]
    temp=0
    plot_radial_perimeter(rads, radius, fitted)
    for x in range(0, len(radius)):
        polyval=(fitted[0]*numpy.power(rads[x], 7))+(fitted[1]*numpy.power(rads[x], 6))+(fitted[2]*numpy.power(rads[x], 5))+(fitted[3]*numpy.power(rads[x], 4))+(fitted[4]*numpy.power(rads[x], 3))+(fitted[5]*rads[x]**2)+(fitted[6]*rads[x])+(fitted[4])
        differences.append(x-polyval)
    for x in differences:
        temp += x**2
        temp /= len(differences)
    temp = math.sqrt(temp)
    print(temp)
    #print(fitted)

def main(frame=-1, filename=DEFAULT_FILE_NAME):
    """#input frame: -1, the whole file, else a particular frame"""
    if int(framenum) == -1:
        debug = 0
    else:
        debug = 3

    # Create a VideoCapture object and read from input file
    # If the input is the camera, pass 0 instead of the video file name
    cap = cv2.VideoCapture(filename)

    frame_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fcount = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    is_before_first = True

    print("WIDTH: ", frame_w)
    print("HEIGHT: ", frame_h)
    print("FPS: ", fps)
    print("FCOUNT: ", fcount)

    # Check if camera opened successfully
    if not cap.isOpened():
        print("Error opening video stream or file")
    #   Read until video is completed
    while cap.isOpened():
      # Capture frame-by-frame
        if int(framenum) != -1:
            cap.set(cv2.CAP_PROP_POS_FRAMES, int(framenum)-1)

        ret, frame = cap.read()

        if ret:
            #print(cap.get(cv2.CAP_PROP_POS_FRAMES))
              #save nth frame to a file
            if framenum == -1:
                if(is_before_first and cap.get(cv2.CAP_PROP_POS_FRAMES) == 45):
                    is_before_first = False
                    cv2.imwrite("frame.bmp", frame)
            else:
                if(is_before_first and cap.get(cv2.CAP_PROP_POS_FRAMES) == framenum):
                    is_before_first = False
                    cv2.imwrite("frame.bmp", frame)


            _, rads, radius = pupillometry(frame, debug)

            display_main(frame, cap)
            try:
                best_fit(rads, radius)
            except numpy.linalg.LinAlgError as er:
                print('skip')

            # Press Q on keyboard to  exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

              # Break the loop
        else:
            break

        if cap.get(cv2.CAP_PROP_POS_FRAMES) == int(framenum):
            break

    # When everything done, release the video capture object
    cap.release()

    # Closes all the frames
    cv2.destroyAllWindows()

if __name__ == "__main__":
    print(len(sys.argv))
    if len(sys.argv) > 1 :
        if len(sys.argv) == 2:
            framenum = int(sys.argv[1])
            filename = DEFAULT_FILE_NAME
        if len(sys.argv) == 3:
            framenum = int(sys.argv[1])
            filename = sys.argv[2]
    else:
        framenum = -1
        filename = DEFAULT_FILE_NAME
    print("Frame Number: ", framenum)
    print("File Name", filename)
    main(framenum, filename)
