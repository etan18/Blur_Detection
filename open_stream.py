"""
Includes 2 of 3 functions needed to detect if input video is blurred
"""
import cv2
import numpy as np

CAM = "/Users/ErinTan/Projects/SMI_Pupillometry/SMI_Pupilometry_Test.mp4"
cap = cv2.VideoCapture(cam)

def blur_output(bool_blur, int_blur):
    """Prints green window for not blurred, red for blurred plus numeral"""
     # Create black blank image
    image = np.zeros((100, 100, 3), np.uint8)
    if boolBlur:
        # Fill image with green color
        image[:] = (0, 255, 0)
    else:
        image[:] = (0, 0, 255)
        print(intBlur)

    cv2.imshow('light', image)
    cv2.waitKey(0)

if __name__ == "__main__":
    while cap.isOpened():
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        blur_detect(frame)
    cap.release()
