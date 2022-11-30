import cv2 as cv

def manualVideoCrop(name, pixLeft, pixRight, pixTop, pixBottom): #crop a video (name) to output a video cropped from a specific distance of pixels
    vid = cv.VideoCapture(name)
    
    checker = True
    
    frameCounter = 0
    
    width = (pixRight - pixLeft)
    height = (pixBottom - pixTop)
    
    output = cv.VideoWriter("croppedVideo.avi", 0x7634706d, 30, (width, height))
    
    while(checker):
        hasFrames, image = vid.read()
        
        if(hasFrames):
            image = image[pixTop:pixBottom, pixLeft:pixRight]
            
            output.write(image)
                
            frameCounter = frameCounter + 1
            
        else:
            break
            
    output.release()
    
########################################################################

#get input
fileName = input("What is the name of the file? (name.extension)\n")
left = input("What is the first x coordinate you want the frame to capture? (give the number only)\n")
left = int(left)
right = input("What is the last x coordinate you want the frame to capture? (give the number only)\n")
right = int(right)
top = input("What is the first y coordinate you want the frame to capture? (give the number only)\n")
top = int(top)
bottom = input("What is the last y coordinate you want the frame to capture? (give the number only)\n")
bottom = int(bottom)

manualVideoCrop(fileName, left, right, top, bottom)

