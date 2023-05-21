import sys
import time
import speech_recognition as sr

#import logging
#logging.basicConfig(level=logging.DEBUG)

sys.path.append('../')
from obswebsocket import obsws, requests  # noqa: E402

r = sr.Recognizer()
r.energy_threshold = 50
r.dynamic_energy_threshold = False

host = "localhost"
port = 4455
password = "secret"
ws = obsws(host, port, password)
ws.connect()

def switchScene(name : str):
    try:
        print("Switching to {}".format(name))
        ws.call(requests.SetCurrentProgramScene(sceneName=name))
    except KeyboardInterrupt:
        pass

# Define the keywords to trigger camera switching
keywords = ['cat', 'dog']

# Continuously listen for audio and process speech
with sr.Microphone() as source:
    print("Listening for speech...")
    while True:
        audio = r.listen(source)

        try:
            # Convert audio to text using speech recognition
            text = r.recognize_google(audio)

            # Print the recognized text
            print("Recognized:", text)

            # Check for keywords to switch cameras
            for keyword in keywords:
                if keyword in text:
                    # Switch cameras in OBS using WebSocket requests
                    switchScene(keyword)
                    break

        except sr.UnknownValueError:
            print("Speech recognition could not understand audio.")
        except sr.RequestError as e:
            print("Could not request results from speech recognition service; {0}".format(e))

ws.disconnect()
