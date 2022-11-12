import PySimpleGUI as sg
import cv2
import base64

def getThumb(movie, frame):
    movie.set(cv2.CAP_PROP_POS_FRAMES, frame)
    success, outframe = movie.read()
    if not success:
        print(f"Error getting thumbnail at frame {frame}")
    else:
        movie.set(cv2.CAP_PROP_POS_FRAMES, 0)
        return cv2.imencode('.png', cv2.resize(outframe, (426,240)))[1].tobytes()

curmovie = None
defaultimage = cv2.resize(cv2.imread('default.png'), (426,240))
defaultimageb = cv2.imencode('.png', defaultimage)[1].tobytes()
playing = False

col_left = [
    [sg.Text('Framerate:', s=(12,1), justification='left', font ='Helvetica 12'), sg.Input()],
    [sg.Text('Resolution:', s=(12,1), justification='left', font ='Helvetica 12'), sg.Input()],
    [sg.Text('Crop Fields:', s=(12,1), justification='left', font ='Helvetica 12'), sg.Input()],
    [sg.Text('Trim Fields:', s=(12,1), justification='left', font ='Helvetica 12'), sg.Input()],
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
            [sg.Push(), sg.Text('Movie Viewer', size=(20,1), justification='center', font='Helvetica 20'), sg.Push()],
            [sg.HorizontalSeparator()],
            [sg.Column(col_left), sg.Column(col_right)]
        ],)
    ]
]

window = sg.Window(title="Movie Editor", layout=layout, finalize=True)
window['SLIDER'].bind('<ButtonRelease-1>', 'RELEASE')
window['FRAMEINPUT'].bind("<Return>", "SUBMIT")


while True:
    print("hi we're in event")
    event, values = window.read(timeout=20)
    if event in (sg.WINDOW_CLOSED, 'Exit'):
        print('uh oh exit')
        break
    elif(event == 'Open'):
        retval = sg.popup_get_file("Please choose a movie to edit:")
        curmovie = cv2.VideoCapture(retval)
        thumbnail = getThumb(curmovie, 0)
        window["THUMB"].update(data = thumbnail)
        window["SLIDER"].update(range=(0,curmovie.get(cv2.CAP_PROP_FRAME_COUNT)-1))
        window["MAXFRAMES"].update(str(int(curmovie.get(cv2.CAP_PROP_FRAME_COUNT))))

        print("loaded movie and thumbnail.")
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
            window["FRAMEINPUT"].update(value=curmovie.get(cv2.CAP_PROP_POS_FRAMES))



                
    else:
        print(event, values)