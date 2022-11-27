## Contains function definitions that are to be applied on frames.
import cv2

def frResChange(frame, desw, desh):
    return cv2.resize(frame, (desw, desh), interpolation=cv2.INTER_AREA)

def frCrop(frame, top, bottom, left, right):
    return frame[top:bottom, left:right]

def frBlend(frame1, frame2, adv):
    return cv2.addWeighted(frame1, (1 - adv), frame2, adv, 0)



