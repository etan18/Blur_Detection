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
import numpy
from find_pupil import pupillometry
from blur_detection import variance_of_laplacian

#text
FONT = cv2.FONT_HERSHEY_SIMPLEX
SMI_DIM = (720, 480) # Dimension from SMI System
DEFAULT_FILE_NAME = '/Users/ErinTan/Downloads/pupil_clip1.mp4'


def plot_radial_perimeter(rads, radius, fitted):
    """plots radians over radius for the left and right eye"""
    plt.figure(1)
    # plt.subplot(121)
    plt.clf()
    # plt.subplot(121)
    plt.ion()
    plt.axis([-4, 4, 45, 65])
    plt.plot(rads, radius, 'ro', marker=".", markersize=5)
    plt.ylabel('radius (pixels)')
    plt.xlabel('angle (radians)')

    x = numpy.arange(min(rads), max(rads), 0.01)
    y = numpy.asarray([eval_fitted(fitted, x_num) for x_num in x])
    plt.plot(x, y)
    plt.show()
    plt.pause(0.05)

def eval_fitted(fitted, x):
    x7  = fitted[0]  * (x**7)
    x6  = fitted[1]  * (x**6)
    x5  = fitted[2]  * (x**5)
    x4  = fitted[3]  * (x**4)
    x3  = fitted[4]  * (x**3)
    x2  = fitted[5] * (x**2)
    x1  = fitted[6] * x
    x0  = fitted[7]
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

def display_left(left):
    """ Display the Left Eye"""
    resized_left = resize_with_aspect_ratio(left, width=640) #Resize by\
    # pylint: disable=C0103
    L_STRING = "Left"
    cv2.putText(resized_left, L_STRING, (0, 20), FONT, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.imshow('Left Eye', resized_left)
    #cv2.waitKey(0)
    # resized_frame = ResizeWithAspectRatio(frame, height = 480)

# returns the R value of the polyfit to the data
def best_fit(rads, radius):

    #Normalizing
    #radius_avg = numpy.mean(radius)
    #radius = radius/radius_avg

    fitted = numpy.polyfit(rads, radius, 7)
    #print('best fit: ', fitted)
    differences = []
    polyval_array = []
    temp = 0
    #plot_radial_perimeter(rads, radius, fitted)
    for x in range(0, len(radius)):
        polyval = eval_fitted(fitted, rads[x])
        polyval_array.append(polyval)
        differences.append(radius[x]-polyval)

    if(False):
        plt.figure(2)
        plt.ion()
        plt.clf()
        plt.plot(rads,polyval_array, 'ro', marker=".", markersize=5)
        plt.plot(rads,radius, 'bo', marker=".", markersize=5)
        plt.show()
        plt.pause(0.05)

    for x in differences:
        temp += x**2
    temp /= len(differences)
    RMS = math.sqrt(temp)
    print(RMS)
    return RMS
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

    #start a csv file
    csvdata = open('sharp_and_polyfit_data'+'.csv', "w")
    csvdata.write('frame,sharp,polyfit_variance\n')

    blurriness_array = []
    R_array = []

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

            frame = frame[90:380,150:500] #Zoom in on the pupil

            image_edit, rads, radius = pupillometry(frame, debug)
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            boolean, blurriness = variance_of_laplacian(gray_frame)
            print("SHARP SCORE: ", blurriness)

            display_main(frame, cap)
            display_left(image_edit)
            frame_position = cap.get(cv2.CAP_PROP_POS_FRAMES)
            try:
                R = best_fit(rads, radius)
                csvdata.write(str(frame_position)+','+str(blurriness)+','+str(R)+'\n')
                R_array.append(R)
                blurriness_array.append(blurriness)
            except numpy.linalg.LinAlgError as er:
                print('skip')
                csvdata.write(str(frame_position)+','+str(blurriness)+','+'none'+'\n')

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
    plt.figure(3)
    plt.plot(blurriness_array,R_array, 'ro', marker=".", markersize=5)
    plt.show()
    input("Press Enter to continue...")

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
