import PySimpleGUI as sg
import cv2
import numpy as np
from FrameUtils import *

curmovie = None
defaultimage = cv2.resize(cv2.imread('default.png'), (426,240))
defaultimageb = cv2.imencode('.png', defaultimage)[1].tobytes()
playing = False
cm_height = None
cm_width = None
cm_fps = None

col_left = [
    [sg.Text('Framerate:', s=(12,1), justification='left', font ='Helvetica 12'),
     sg.Combo([120,60,45,30,15,10,5,1], default_value=60, key ="FPS", s=(8, 1)),
     sg.Checkbox("Blend?", key = "BLN", tooltip="Enable Frame Blending")],
    [sg.Text('Resolution:', s=(12,1), justification='left', font ='Helvetica 12'),
     sg.Combo(['2560','1920', '1280', '854', '640', '426'],default_value='640', key ="RSW", s=(5,1)),
     sg.Text("x",s=(1,1), justification='left', font="Helvetica 12"),
     sg.Combo(['1440','1080', '720', '480', '360', '240'],default_value='480', key ="RSH", s=(5,1))],

    [sg.Text('Crop Fields:', s=(12,1), justification='left', font ='Helvetica 12'),
    sg.Input(s=(8,1), key="CRT", default_text='0'),
    sg.Input(s=(8,1), key ="CRL", default_text = '0')],

    [sg.Input(s=(8,1), key="CRB", default_text = '0'),
    sg.Input(s=(8,1), key ="CRR", default_text = '0')],
     
    [sg.Text('Trim Fields:', s=(12,1), justification='left', font ='Helvetica 12'),
     sg.Input(s=(8,1), key ="TR1", default_text = '0'),
     sg.Input(s=(8,1), key ="TR2", default_text = '0')],
    [sg.Button('Process')]
]

col_right = [
    [sg.Image(key = "THUMB", data = defaultimageb, s=(426,240))],
    [   sg.Button(image_filename='smallplay.png', key="PLAYPAUSE", font = 'Helvetica 11'),
        sg.Slider(range=(0,1),orientation="h",default_value=0,expand_x=True,disable_number_display=True,
        relief=sg.RELIEF_FLAT,key="SLIDER", enable_events=True),
        sg.Input("0", s=(7,1),key="FRAMEINPUT"),
        sg.Text("1",s = (7,1), relief=sg.RELIEF_SUNKEN, border_width=2,key="MAXFRAMES")]
]

layout = [
    [   
        sg.Menu([
            ['&File', ['&Open','E&xit']]
        ]),
        sg.Column([
            [sg.Push(), sg.Text('Movie Editor', size=(20,1), justification='center', font='Helvetica 20'), sg.Push()],
            [sg.HorizontalSeparator()],
            [sg.Column(col_left), sg.Column(col_right)]
        ],)
    ]
]

window = sg.Window(title="Movie Editor", layout=layout, finalize=True)
window['SLIDER'].bind('<ButtonRelease-1>', 'RELEASE')
window['FRAMEINPUT'].bind("<Return>", "SUBMIT")

## Grabs a screenshot of a given frame from a VideoCapture. Used
## to make thumbnails for the video explorer.
def getThumb(movie, frame):
    movie.set(cv2.CAP_PROP_POS_FRAMES, frame)
    success, outframe = movie.read()
    if not success:
        print(f"Error getting thumbnail at frame {frame}")
    else:
        movie.set(cv2.CAP_PROP_POS_FRAMES, 0)
        return cv2.imencode('.png', cv2.resize(outframe, (426,240)))[1].tobytes()

## Picks source frames that will make it into the final video based
## on the chosen FPS, and composes in-between frames if blending is enabled.
def framePick(reader, values):
    framestart = int(values["TR1"])
    frameend = int(values["TR2"])
    desfps = values["FPS"]
    startfps = reader.get(cv2.CAP_PROP_FPS)
    frameratio = startfps/desfps
    upsampling = (frameratio < 1)
    success, thisframe = reader.read()
    success, nextframe = reader.read()
    targetframe = 0
    frameindex = 0
    writer = cv2.VideoWriter('output.avi', 
        cv2.VideoWriter_fourcc('M','J','P','G'), desfps,
        (int(values['RSW']), int(values['RSH'])))
    written = 0
    
    while reader.isOpened():
        ## Trimming
        if frameindex < framestart:
            frameindex += 1
            thisframe = nextframe
            success, nextframe = reader.read()
            if not success:
                break
            continue
        if frameindex > frameend:
            break
        ## determining desirable frames to modify and encode for fps changes
        if not upsampling: ## This is true with no FPS change as well
            if frameindex < targetframe: ## Skip this frame
                thisframe = nextframe
                success, nextframe = reader.read()
                frameindex += 1
                if not success:
                    break
                continue
            else: ## take this frame
                modifyAndWrite(thisframe, writer, values)
                written += 1
                thisframe = nextframe
                success, nextframe = reader.read()
                frameindex += 1
                if not success:
                    break

        else: ##upsampling
            floored = int(np.floor(targetframe))
            while floored == frameindex:
                selectframe = None;
                if values["BLN"]:
                    selectframe = frBlend(thisframe, nextframe, targetframe-floored)
                else:
                    selectframe = thisframe
                modifyAndWrite(selectframe, writer, values)
                written += 1
                targetframe += frameratio
                floored = int(np.floor(targetframe))
            thisframe = nextframe
            success, nextframe = reader.read()
            frameindex += 1
            if not success:
                break
    print(f"Frames written. Final video length: {written}")

## Frames selected by FramePick are sent to this function, which writes the video
## after modifying the frame by the given parameters.
def modifyAndWrite(frame, writer, values):
    top = int(values['CRT'])
    bottom = int(values['CRB'])
    left = int(values['CRL'])
    right = int(values['CRR'])
    resw = int(values['RSW'])
    resh = int(values['RSH'])
    if top != '': ## crop specified
        frame = frCrop(frame, top, bottom, left, right)
    if resw != '': ## resolution specified
        frame = frResChange(frame, resw, resh)
    writer.write(frame)

while True:
    event, values = window.read(timeout=33)

    if event in (sg.WINDOW_CLOSED, 'Exit'):
        break

    elif(event == 'Open'):
        retval = sg.popup_get_file("Please choose a movie to edit:")
        curmovie = cv2.VideoCapture(retval)
        frameout = []

        cm_fps = curmovie.get(cv2.CAP_PROP_FPS)
        cm_height = int(curmovie.get(cv2.CAP_PROP_FRAME_HEIGHT))
        cm_width = int(curmovie.get(cv2.CAP_PROP_FRAME_WIDTH))

        thumbnail = getThumb(curmovie, 0)
        window["THUMB"].update(data = thumbnail)
        window["SLIDER"].update(range=(0,curmovie.get(cv2.CAP_PROP_FRAME_COUNT)-1))
        window["MAXFRAMES"].update(str(int(curmovie.get(cv2.CAP_PROP_FRAME_COUNT))))
        window["RSW"].update(int(cm_width))
        window["RSH"].update(int(cm_height))
        window["FPS"].update(cm_fps)
        window["CRT"].update('0')
        window["CRB"].update(cm_height)
        window["CRL"].update('0')
        window["CRR"].update(cm_width)
        window["TR1"].update(0)
        window["TR2"].update(int(curmovie.get(cv2.CAP_PROP_FRAME_COUNT)-1))
        print("loaded movie and thumbnail.")
    elif(event == 'Process'):
        desiredframerate = values["FPS"]
        desiredresolutionH = int(values["RSH"])
        desiredresolutionW = int(values["RSW"])
        print(f"Processing...\n\tDesired Frame Rate: {desiredframerate}"+
            f"\n\tDesired Resolution: {desiredresolutionW} x {desiredresolutionH}" + 
            f"\n\tDesired Trim: [{values['TR1']}-{values['TR2']}]")
        curmovie.set(cv2.CAP_PROP_POS_FRAMES, 0)
        framePick(curmovie, values)
        
    elif(event == 'SLIDERRELEASE'):
        window["FRAMEINPUT"].update(value=int(values["SLIDER"]))
        if(curmovie == None):
            continue
        else:
            thumbnail = getThumb(curmovie, int(values["SLIDER"]))
            window["THUMB"].update(data = thumbnail)

    elif(event == 'FRAMEINPUTSUBMIT'):
        window["SLIDER"].update(value=int(values["FRAMEINPUT"]))
        if(curmovie == None):
            continue
        else:
            thumbnail = getThumb(curmovie, int(values["FRAMEINPUT"]))
            window["THUMB"].update(data = thumbnail)

    elif(event == 'PLAYPAUSE'):
        if curmovie == None:
            continue
        if playing:
            window["PLAYPAUSE"].update(image_filename="smallplay.png")
            print("pausing")
            playing = False
        else:
            window["PLAYPAUSE"].update(image_filename="smallpause.png")
            print("playing")
            playing = True

    if playing:
        status, frame = curmovie.read()
        if not status:
            playing = False
            print("End of movie")
        else:
            outframe = cv2.imencode('.png', cv2.resize(frame, (426,240)))[1].tobytes()
            window["THUMB"].update(data = outframe)
            window["SLIDER"].update(value=curmovie.get(cv2.CAP_PROP_POS_FRAMES))
            window["FRAMEINPUT"].update(value=int(curmovie.get(cv2.CAP_PROP_POS_FRAMES)))
