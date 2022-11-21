import cv2
import numpy as np


def rateChange(framelistin, startrate, endrate, frameblend = False):
    ## Input framelist is played at startrate. Frames need to be skipped to maintain video length
    ## (and, ideally, content) to fit to a new, lower frame rate.
    frameratio = startrate / endrate
    framelistout = []
    targetframe = 0
    if frameratio < 1: ##upconversion
        while targetframe < len(framelistin)-1:
            flooredint = int( np.floor(targetframe)) 
            if frameblend:
                blendweight = targetframe - flooredint
                blendedframe = cv2.addWeighted(framelistin[flooredint], (1 - blendweight), framelistin[flooredint + 1], blendweight, 0)
                framelistout.append(blendedframe)
            else:
                framelistout.append(framelistin[flooredint])
            targetframe += frameratio

    else: ##Downconversion
        for frameindex, frame in enumerate(framelistin):
            if frameindex >= targetframe:
                framelistout.append(frame)
                targetframe += frameratio
        
    return framelistout