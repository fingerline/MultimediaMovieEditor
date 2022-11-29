## Contains function definitions that are to be applied on frames.
import cv2

def frResChange(frame, desw, desh):
    return cv2.resize(frame, (desw, desh), interpolation=cv2.INTER_AREA)

def frBlend(frame1, frame2, adv):
    return cv2.addWeighted(frame1, (1 - adv), frame2, adv, 0)

def manualVideoCrop(vidFrame, pixLeft, pixRight, pixTop, pixBottom):
    editFrame = vidFrame[pixTop:pixBottom, pixLeft:pixRight]
    
    return editFrame
    
def manualVideoTrim(vidFrame, firstFrame, lastFrame): #unused as a list is no longer used, just here for formalities
    checker = True
    
    frameCounter = 0
    
    frameSizer = vidFrame[0]
    dimensions = frameSizer.shape
    
    height = dimensions[0]
    width = dimensions[1]
    
    output = []
    
    for i in vidFrame:
        if((frameCounter >= firstFrame) and (frameCounter < lastFrame)):
            output.append(i)
            
        frameCounter = frameCounter + 1
    
    return output
    

