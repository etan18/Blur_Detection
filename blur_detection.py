import cv2
import time
import numpy
from imutils.video import FPS
from imutils.video import FileVideoStream

Path = r'C:\Users\prashanthi\GitHub\Blur_Detection\HalfOpen_LookingAround.mp4'

def variance_of_laplacian(grayImage):
    Threshold=100
    #height=grayImage.shape[0]
    #width=grayImage.shape[1]
    #x=int(height/5)
    #y=int(width/5)
    #croppedImage = grayImage[x:height-x, y:width-y]
    small = cv2.resize(grayImage, (0,0), fx=0.5, fy=0.5)
    bluriness = cv2.Laplacian(small, cv2.CV_64F).var()
    blurry= False
    if bluriness < Threshold:
        blurry= True
    return blurry, bluriness


if __name__ == "__main__":
    #path to video stream
    fvs = FileVideoStream(Path).start()
    #time.sleep(1)

    fps = FPS().start()

    while fvs.more():

        frame = fvs.read()
        if frame.all()!=None:
            frame= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = numpy.dstack([frame, frame, frame])
        boolean, bluriness = variance_of_laplacian(frame)
        if boolean==False:
            text="Not blurry, press q to quit\n"
            cv2.putText(frame, "{}: {:.2f}".format(text, blurriness), (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 3)
        else:
            text="Blurry, press q to quit\n"
            cv2.putText(frame, "{}: {:.2f}".format(text, blurriness), (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        fps.update()

    cv2.destroyAllWindows()
    fvs.stop()
