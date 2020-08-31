import cv2
import time
import numpy
from imutils.video import FPS
from imutils.video import FileVideoStream


def variance_of_laplacian(image):
    Threshold=100

#image = cv2.imread(path)

        #start = time.time()


        #end =time.time()
        #print(end-start)
    #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #height, width=image.shape
    height=image.shape[0]
    width=image.shape[1]
    x=int(height/5)
    y=int(width/5)
    croppedImage = image[x:height-x, y:width-y]
    small = cv2.resize(croppedImage, (0,0), fx=0.5, fy=0.5)
    bluriness = cv2.Laplacian(small, cv2.CV_64F).var()
    text= "Not Blurry "
    if bluriness < Threshold:
        text="Blurry "
    text+=str(bluriness)
    return text


if __name__ == "__main__":
    path = r'C:\Users\prashanthi\GitHub\Blur_Detection\HalfOpen_LookingAround.mp4'
    stream = cv2.VideoCapture(path)
    fvs = FileVideoStream(path).start()
    #time.sleep(1)

    fps = FPS().start()

    while fvs.more():

        frame = fvs.read()
        if frame.all()!=None:
            #frame = imutils.resize(frame, width=450)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = numpy.dstack([frame, frame, frame])
        bluriness = variance_of_laplacian(frame)
        cv2.putText(frame, "{}: {:.2f}".format(bluriness, 0), (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        fps.update()

    cv2.destroyAllWindows()
    fvs.stop()

#bluriness = cv2.Laplacian(gray, cv2.CV_64F).var()#second partial derivative of x/y direction
#replacement for .var()?
#resize+make threshold lower or crop out (u can control during data collectio)



    #output number + boolean

                # show the image
#put text on after this function (return the stuff)

    #cv2.putText(croppedImage, "{}: {:.2f}".format(text, bluriness), (10, 30),
        #cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)

        #cv2.imshow("Image", croppedImage)
        #key = cv2.waitKey(0)
    #return bluriness
        #`how long does this take to do
