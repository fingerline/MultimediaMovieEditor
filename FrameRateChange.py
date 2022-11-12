import cv2
import numpy as np


def rateChange(moviein):
    cap = cv2.VideoCapture(moviein)
    print(f"CV_CAP_PROP_FRAME_WIDTH: '{cap.get(cv2.CAP_PROP_FRAME_WIDTH)}'")
    print(f"CV_CAP_PROP_FRAME_HEIGHT : '{cap.get(cv2.CAP_PROP_FRAME_HEIGHT)}'")
    print(f"CAP_PROP_FPS : '{cap.get(cv2.CAP_PROP_FPS)}'")
    print(f"CAP_PROP_POS_MSEC : '{cap.get(cv2.CAP_PROP_POS_MSEC)}'")
    print(f"CAP_PROP_FRAME_COUNT  : '{cap.get(cv2.CAP_PROP_BRIGHTNESS)}'")
    print(f"CAP_PROP_BRIGHTNESS : '{cap.get(cv2.CAP_PROP_BRIGHTNESS)}'")
    print(f"CAP_PROP_CONTRAST : '{cap.get(cv2.CAP_PROP_CONTRAST)}'")
    print(f"CAP_PROP_SATURATION : '{cap.get(cv2.CAP_PROP_SATURATION)}'")
    print(f"CAP_PROP_HUE : '{cap.get(cv2.CAP_PROP_HUE)}'")
    print(f"CAP_PROP_GAIN  : '{cap.get(cv2.CAP_PROP_GAIN)}'")
    print(f"CAP_PROP_CONVERT_RGB : '{cap.get(cv2.CAP_PROP_CONVERT_RGB)}'")


    while cap.isOpened():
        success, frame = cap.read()
        if success:
            resized = cv2.resize(frame, (640, 360), interpolation=cv2.INTER_AREA)
            cv2.imshow('Frame', resized)

            cv2.waitKey(1)
        else:
            break
    
    cap.release()

    cv2.destroyAllWindows()

rateChange('sample.avi')