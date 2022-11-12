import cv2

def resChange(framelistin,desw,desh):

    outframes = []

    for frame in framelistin:
            outframe = cv2.resize(frame, (desw, desh), interpolation=cv2.INTER_AREA)
            outframes.append(outframe)

    return outframes