import PySimpleGUI as sg
import cv2
from oldfiles.ChangeResolution import resChange
from oldfiles.FrameRateChange import rateChange
from oldfiles.DA_vidCrop_perList import manualVideoCrop
from oldfiles.DA_vidTrim_perList import manualVideoTrim

def getThumb(movie, frame):
    movie.set(cv2.CAP_PROP_POS_FRAMES, frame)
    success, outframe = movie.read()
    if not success:
        print(f"Error getting thumbnail at frame {frame}")
    else:
        movie.set(cv2.CAP_PROP_POS_FRAMES, 0)
        return cv2.imencode('.png', cv2.resize(outframe, (426, 240)))[1].tobytes()

curmovie = None
defaultimage = cv2.resize(cv2.imread('default.png'), (426, 240))
defaultimageb = cv2.imencode('.png', defaultimage)[1].tobytes()
playing = False
cm_height = None
cm_width = None
cm_fps = None
cm_left = None
cm_right = None
cm_top = None
cm_bottom = None
cm_start = None
cm_end = None

col_left = [
    [sg.Text('Framerate:', s = (12, 1), justification='left', font ='Helvetica 12'),
     sg.Combo([120, 60, 45, 30, 15, 10, 5, 1], default_value = 60, key = "FPS", s = (16, 1))],
    [sg.Text('Resolution:', s = (12, 1), justification = 'left', font = 'Helvetica 12'),
     sg.Combo(['2560', '1920', '1280', '854', '640', '426'], default_value = '640', key = "RSW", s = (5, 1)),
     sg.Text("x", s = (1, 1), justification = 'left', font = "Helvetica 12"),
     sg.Combo(['1440', '1080', '720', '480', '360', '240'], default_value = '480', key = "RSH", s = (5, 1))],

    [sg.Text('Crop Fields:', s = (12, 1), justification = 'left', font = 'Helvetica 12'),
     sg.Input(s = (8, 1), key = "CR1"),
     sg.Input(s = (8, 1), key = "CR2"),
     sg.Input(s = (8, 1), key = "CR3"),
     sg.Input(s = (8, 1), key = "CR4")],
    [sg.Text('Trim Fields:', s = (12, 1), justification = 'left', font = 'Helvetica 12'),
     sg.Input(s = (8, 1), key = "TR1"),
     sg.Input(s = (8, 1), key = "TR2")],
    [sg.Button('Process')]
]

col_right = [
    [sg.Image(key = "THUMB", data = defaultimageb, s = (426, 240))],
    [   sg.Button(image_filename = 'smallplay.png', key = "PLAYPAUSE", font = 'Helvetica 11'),
        sg.Slider(range = (0, 1), orientation = "h", default_value = 0, expand_x = True, disable_number_display = True,
        relief = sg.RELIEF_FLAT, key = "SLIDER", enable_events = True),
        sg.Input("0", s = (7, 1), key = "FRAMEINPUT"),
        sg.Text("1", s = (7, 1), relief = sg.RELIEF_SUNKEN, border_width = 2, key = "MAXFRAMES")]
]

layout = [
    [   
        sg.Menu([
            ['&File', ['&Open', 'E&xit']]
        ]),
        sg.Column([
            [sg.Push(), sg.Text('Movie Editor', size = (20, 1), justification = 'center', font = 'Helvetica 20'), sg.Push()],
            [sg.HorizontalSeparator()],
            [sg.Column(col_left), sg.Column(col_right)]
        ],)
    ]
]

window = sg.Window(title = "Movie Editor", layout = layout, finalize = True)
window['SLIDER'].bind('<ButtonRelease-1>', 'RELEASE')
window['FRAMEINPUT'].bind("<Return>", "SUBMIT")

window["CR1"].update("left")
window["CR2"].update("right")
window["CR3"].update("top")
window["CR4"].update("bottom")
window["TR1"].update("start")
window["TR2"].update("end")

while True:
    event, values = window.read(timeout = 33)

    if event in (sg.WINDOW_CLOSED, 'Exit'):
        break

    elif(event == 'Open'):
        retval = sg.popup_get_file("Please choose a movie to edit:")
        curmovie = cv2.VideoCapture(retval)
        frameout = []

        cm_fps = curmovie.get(cv2.CAP_PROP_FPS)
        cm_height = int(curmovie.get(cv2.CAP_PROP_FRAME_HEIGHT))
        cm_width = int(curmovie.get(cv2.CAP_PROP_FRAME_WIDTH))
        cm_left = 0
        cm_right = int(curmovie.get(cv2.CAP_PROP_FRAME_WIDTH))
        cm_top = 0
        cm_bottom = int(curmovie.get(cv2.CAP_PROP_FRAME_HEIGHT))
        cm_start = 0
        cm_end = int(curmovie.get(cv2.CAP_PROP_FRAME_COUNT))

        thumbnail = getThumb(curmovie, 0)
        window["THUMB"].update(data = thumbnail)
        window["SLIDER"].update(range = (0, curmovie.get(cv2.CAP_PROP_FRAME_COUNT) - 1))
        window["MAXFRAMES"].update(str(int(curmovie.get(cv2.CAP_PROP_FRAME_COUNT))))
        window["RSW"].update(int(cm_width))
        window["RSH"].update(int(cm_height))
        window["FPS"].update(cm_fps)
        window["CR1"].update(cm_left)
        window["CR2"].update(cm_right)
        window["CR3"].update(cm_top)
        window["CR4"].update(cm_bottom)
        window["TR1"].update(cm_start)
        window["TR2"].update(cm_end)

        print("loaded movie and thumbnail.")

    elif(event == 'Process'):
        desiredframerate = values["FPS"]
        
        desiredresolutionH = int(values["RSH"])
        desiredresolutionW = int(values["RSW"])
        
        desiredCropL = int(values["CR1"])
        desiredCropR = int(values["CR2"])
        desiredCropT = int(values["CR3"])
        desiredCropB = int(values["CR4"])
        
        desiredStart = int(values["TR1"])
        desiredEnd = int(values["TR2"])
        
        xMinus = desiredCropR - desiredCropL
        yMinus = desiredCropB - desiredCropT
        frameMinus = desiredEnd - desiredStart
        
        print(f"Processing...\n\tDesired Frame Rate: {desiredframerate}\n\tDesired Resolution: {xMinus} x {yMinus}\n\tDesired length: {frameMinus} frames")

        ## Composing Framelist
        framelist = []
        curmovie.set(cv2.CAP_PROP_POS_FRAMES, 0)
        while curmovie.isOpened():
            success, frame = curmovie.read()
            if success:
                framelist.append(frame)
            else:
                break
        print(f"Successfully loaded frames. Original frame count: {len(framelist)}")
        
        ## Perform actions upon framelist
        if desiredframerate == cm_fps:
            print("Ignoring unchanged fps.")
        else:
            framelist = rateChange(framelist, cm_fps, desiredframerate, True)
        
        #if desiredresolutionH == cm_height and desiredresolutionW == cm_width:
        #    print("Ignoring unchanged resolution.")
        #else:
        #    framelist = resChange(framelist, desiredresolutionW, desiredresolutionH)
        
        if((desiredCropL == cm_left) and (desiredCropR == cm_right) and (desiredCropT == cm_top) and (desiredCropB == cm_bottom)):
            print("Ignoring unchanged cropping regions.")
        else:
            framelist = manualVideoCrop(framelist, desiredCropL, desiredCropR, desiredCropT, desiredCropB)
         
        if((desiredStart == cm_start) and (desiredEnd == cm_end)):
            print("Ignoring unchanged trimming times.")
        else:
            framelist = manualVideoTrim(framelist, desiredStart, desiredEnd)
       
        ## Export Framelist
        writer = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), desiredframerate, (xMinus, yMinus))
        for i, frame in enumerate(framelist):
            writer.write(frame)
        print("Processing done.")
        writer.release()

    elif(event == 'SLIDERRELEASE'):
        window["FRAMEINPUT"].update(value = int(values["SLIDER"]))
        if(curmovie == None):
            continue
        else:
            thumbnail = getThumb(curmovie, int(values["SLIDER"]))
            window["THUMB"].update(data = thumbnail)

    elif(event == 'FRAMEINPUTSUBMIT'):
        window["SLIDER"].update(value = int(values["FRAMEINPUT"]))
        if(curmovie == None):
            continue
        else:
            thumbnail = getThumb(curmovie, int(values["FRAMEINPUT"]))
            window["THUMB"].update(data = thumbnail)

    elif(event == 'PLAYPAUSE'):
        if curmovie == None:
            continue
        if playing:
            window["PLAYPAUSE"].update(image_filename = "smallplay.png")
            print("pausing")
            playing = False
        else:
            window["PLAYPAUSE"].update(image_filename = "smallpause.png")
            print("playing")
            playing = True

    if playing:
        status, frame = curmovie.read()
        if not status:
            playing = False
            print("End of movie")
        else:
            outframe = cv2.imencode('.png', cv2.resize(frame, (426, 240)))[1].tobytes()
            window["THUMB"].update(data = outframe)
            window["SLIDER"].update(value = curmovie.get(cv2.CAP_PROP_POS_FRAMES))
            window["FRAMEINPUT"].update(value = int(curmovie.get(cv2.CAP_PROP_POS_FRAMES)))

    elif (event != '__TIMEOUT__'):
        print(event)

