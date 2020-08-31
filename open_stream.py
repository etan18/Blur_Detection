import imutils
import cv2
from imutils.video import FPS

if __name__ == "__main__":
    fvs = FileVideoStream(1).start()
    time.sleep(1)

    fps = FPS().start()

    while fvs.more():
        frame = fvs.read()
        #frame = imutils.resize(frame, width=450)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = np.dstack([frame, frame, frame])
        blurriness = variance_of_laplacian(frame)
        cv2.putText(gray, "{}: {:.2f}".format(text), (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        fps.update()

    cv2.destroyAllWindows()
    fvs.stop()
