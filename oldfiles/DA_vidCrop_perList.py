import cv2 as cv

def manualVideoCrop(vid, pixLeft, pixRight, pixTop, pixBottom): #crop a video (vid) to output a video cropped from a specific distance of pixels
    output = []
    
    for i in vid:
        editFrame = i[pixTop:pixBottom, pixLeft:pixRight]
        
        output.append(editFrame)
            
    return output
    
