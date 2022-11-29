import cv2 as cv

def manualVideoTrim(vid, firstFrame, lastFrame): #trim a video (vid) to output a video from firstFrame to lastFrame
    checker = True
    
    frameCounter = 0
    
    frameSizer = vid[0]
    dimensions = frameSizer.shape
    
    height = dimensions[0]
    width = dimensions[1]
    
    output = []
    
    for i in vid:
        if((frameCounter >= firstFrame) and (frameCounter < lastFrame)):
            output.append(i)
            
        frameCounter = frameCounter + 1
    
    return output
    

