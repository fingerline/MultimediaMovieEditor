import cv2
from ChangeResolution import resChange

## takes in an list of frames and displays them as a video
def readout(framelist,fps):
    framedelay = (int) (1000 / fps)
    for frame in framelist:
        cv2.imshow("Output Movie", frame)
        cv2.waitKey(framedelay)
    cv2.destroyAllWindows()

def composeFrameList(movie):
    cap = cv2.VideoCapture(movie)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frameout = []
    while cap.isOpened():
        success, frame = cap.read()
        if success:
            frameout.append(frame)
        else:
            break
    cap.release()
    return fps, frameout

moviename = 'sample.avi'
fps, framelist = composeFrameList(moviename)
changedmovie = resChange(framelist, 640, 360)
readout(changedmovie, fps)
    