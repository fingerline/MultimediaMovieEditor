import cv2
from ChangeResolution import resChange
from FrameRateChange import rateChange

## takes in an list of frames and displays them as a video
def readout(framelist,fps):
    framedelay = (int) (1000 / fps)
    print(f"Output:\n\tFrames: {len(framelist)}")
    for frame in framelist:
        cv2.imshow("Output Movie", frame)
        cv2.waitKey(framedelay)
    cv2.destroyAllWindows()

def composeFrameList(movie):
    cap = cv2.VideoCapture(movie)
    fps = cap.get(cv2.CAP_PROP_FPS)
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    print(f"INPUT:\n\tFPS:{fps}\n\tResolution:{w}x{h}")
    frameout = []
    while cap.isOpened():
        success, frame = cap.read()
        if success:
            frameout.append(frame)
        else:
            break
    cap.release()
    print(f"\tFrames:{len(frameout)}")
    return fps, frameout

moviename = 'sample.avi'
fps, framelist = composeFrameList(moviename)
changedres = resChange(framelist, 640, 360)
changedfps = rateChange(changedres, fps, 15)
changedfps2 = rateChange(changedfps, 15, 30, True)

readout(changedfps2, 30)
    