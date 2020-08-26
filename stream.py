import cv2
import matplotlib.pyplot as plt
import numpy as np
from imutils import paths
import ffmpeg_streaming
import ffmpeg

CAM = "/Users/ErinTan/Projects/SMI_Pupillometry/V1219_20850228_234726_Dilation2.mp4"

if __name__ == "__main__":
    cap = cv2.VideoCapture(CAM)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    if not cap.isOpened():
        print("Error opening video")
        break

    frame = cap.grab()
    fno = 0
    while frame:
        if fno % 2 == 0:
            _, img = cap.retrieve()
            cv2.imshow('frame', img)
        frame, img = cap.grab()

    cap.release()
