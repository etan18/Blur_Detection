import cv2
import time
import numpy



Threshold=200 #notime


#images and threshold for how blurry is really blurry
#sepereate main function?
#def variance_of_laplacian(image):
path = r'C:\Users\prashanthi\GitHub\Blur_Detection\blurry.jpg' #notime
image = cv2.imread(path)

start = time.time()


    #put checkpoint for finding time after this and after image is outputted
        #make constants start w/ capital(use pylint to make sure)

    #might need to change, put in beginning of code/before function
        #converts to gray
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
height, width=gray.shape
x=int(height/5)
y=int(width/5)
croppedImage = gray[x:height-x, y:width-y]

#alsocanbechanged
small = cv2.resize(croppedImage, (0,0), fx=0.5, fy=0.5)

 #let erin handle this?? **
        #variance of laplacian
#bluriness = cv2.Laplacian(gray, cv2.CV_64F).var()#second partial derivative of x/y direction
#replacement for .var()?
#make image smaller? crop image to just the pupil/ approximately
#CONTOURS= SLOW.
#resize+make threshold lower or crop out (u can control during data collectio)
#code that finds estimated circles???
bluriness = cv2.Laplacian(small, cv2.CV_64F).var()

text= "Not Blurry "
        # if the focus measure is less than the supplied threshold,
        # then the image should be considered "blurry"
if bluriness < Threshold:
    text="Blurry "
text+=str(bluriness)
end =time.time()
print(end-start)

    #output number + boolean

                # show the image
#put text on after this function (return the stuff)

cv2.putText(croppedImage, "{}: {:.2f}".format(text, bluriness), (10, 30),
    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)

cv2.imshow("Image", croppedImage)
key = cv2.waitKey(0)
    #return bluriness
        #`how long does this take to do

if __name__ == "__main__":
    fvs = FileVideoStream(1).start()
    time.sleep(1)

    fps = FPS().start()

    while fvs.more():
        frame = fvs.read()
        frame = imutils.resize(frame, width=450)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = np.dstack([frame, frame, frame])
        blurriness = variance_of_laplacian(frame)

        if blurry==1:
            text="Blurry"
        if blurry==0:
            text="Not Blurry"
        cv2.putText(gray, "{}: {:.2f}".format(text, bluriness), (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        fps.update()

    cv2.destroyAllWindows()
    fvs.stop()       
