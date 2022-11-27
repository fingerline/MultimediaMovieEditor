import cv2
import numpy as np
from FrameUtils import frResChange, frCrop, frBlend
from memory_profiler import profile

startframe = 0
endframe = 900
desheight = 360
deswidth = 640
desfps = 60
desleft = 0
desright = 500
destop = 0
desbottom = 500
blending = False

written = 0

moviein = cv2.VideoCapture('sample.avi')
movieout = cv2.VideoWriter('outputopti.avi', 
    cv2.VideoWriter_fourcc('M','J','P','G'), desfps, (deswidth, desheight))
print("Loaded video.")

def modifyAndWrite(frame):
    ##frame = frCrop(frame, destop, desbottom, desleft, desright)
    frame = frResChange(frame, deswidth, desheight)
    movieout.write(frame)
    
startrate = moviein.get(cv2.CAP_PROP_FPS)
frameratio = startrate / desfps
upsampling = (frameratio < 1)
success, thisframe = moviein.read()
success, nextframe = moviein.read()
targetframe = 0
frameindex = 0

@profile
def selectAndDispatch():
    global targetframe
    global thisframe
    global nextframe
    global frameindex
    global written
    while moviein.isOpened():
        ## determining desirable frames to modify and encode
        if not upsampling:
            if frameindex < targetframe: ## Skip this frame
                thisframe = nextframe
                success, nextframe = moviein.read()
                frameindex += 1
                if not success:
                    break
                continue
            else: ## take this frame
                modifyAndWrite(thisframe)
                written += 1
                thisframe = nextframe
                success, nextframe = moviein.read()
                frameindex += 1
                if not success:
                    break

        else: ##upsampling
            floored = int(np.floor(targetframe))
            while floored == frameindex:
                selectframe = None;
                if blending:
                    selectframe = frBlend(thisframe, nextframe, targetframe-floored)
                else:
                    selectframe = thisframe
                modifyAndWrite(selectframe)
                written += 1
                targetframe += frameratio
                floored = int(np.floor(targetframe))
            thisframe = nextframe
            success, nextframe = moviein.read()
            frameindex += 1
            if not success:
                break
selectAndDispatch()
print(f"Completed. Wrote {written} frames.")