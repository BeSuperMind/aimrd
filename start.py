from text_to_speech import text_to_speech_sync
import cv2
from field import BlueField
from speech import getQuery



faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# function to start the application
def starter(mixer):
    text_to_speech_sync('Starting the app. This app helps you to meditate. First would you like to have a demo?. Please include yes or no in your voice', mixer)
    res = getQuery(mixer)
    if 'no' in res:
        text_to_speech_sync('Ok great, now lets start the meditation session.', mixer)
        return 'started'
    elif res == '503':
        text_to_speech_sync('Please check your internet connection', mixer)
        return '503'
    elif res == 'error':
        text_to_speech_sync('There was some error starting the application, please try again later.', mixer)
        return 'error'
    elif 'yes' in res:
        while(True):
            text_to_speech_sync('Opening camera, make yourself ready.', mixer)
            video = cv2.VideoCapture(0)
            blue_field = BlueField()
            start_point, end_point = blue_field.create_field(video, faceDetect)
            text_to_speech_sync('Now for the entire meditation you have to be in the marked blue color field. Can we start the session? or do you want the demo one more time?', mixer)
            session_response = getQuery(mixer)
            session_response = session_response.split()
            if 'start' in session_response:
                return 'started'
            elif 'demo' in session_response:
                pass
            elif 'exit' or 'close' in session_response:
                return 'exit'
    else:
        text_to_speech_sync('There was some error starting the application, please try again later.', mixer)
        return 'error'