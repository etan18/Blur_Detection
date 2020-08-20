from imutils import paths
import argparse
import cv2

threshold=100

#images and threshold for how blurry is really blurry
def variance_of_laplacian(image):
        #make constants start w/ capital(use pylint to make sure)
        #might need to change, put in beginning of code/before function
        #converts to gray
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #variance of laplacian
	blurriness = cv2.Laplacian(gray, cv2.CV_64F).var()#second partial derivative of x/y direction
	text = "Not Blurry"
	# if the focus measure is less than the supplied threshold,
	# then the image should be considered "blurry"
	if bluriness < threshold:
		text = "Blurry"
	# show the image
	cv2.putText(image, "{}: {:.2f}".format(text, bluriness), (10, 30),
		cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
	cv2.imshow("Image", image)
	key = cv2.waitKey(0)
	return bluriness
#how long does this take to do
