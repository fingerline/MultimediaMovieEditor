import cv2 as cv

def manualVideoTrim(name, firstFrame, lastFrame): #trim a video (name) to output a video from firstFrame to lastFrame
    vid = cv.VideoCapture(name)
    
    checker = True
    
    frameCounter = 0
    
    hasFrames, image = vid.read()
    dimensions = image.shape
    
    height = dimensions[0]
    width = dimensions[1]
    
    output = cv.VideoWriter("trimmedVideo.avi", 0x7634706d, 30, (width, height))
    
    while(checker):
        if(hasFrames):
            if((frameCounter >= firstFrame) and (frameCounter < lastFrame)):
                
                output.write(image)
                
            frameCounter = frameCounter + 1
            
        else:
            break
        
        hasFrames, image = vid.read()
    output.release()
########################################################################


#get input
fileName = input("What is the name of the file? (name.extension)\n")
frameF = input("What is the frame you want to start on? (give the number only)\n")
frameF = int(frameF)
frameL = input("What is the frame you want to end on? (give the number only)\n")
frameL = int(frameL)

manualVideoTrim(fileName, frameF, frameL)

