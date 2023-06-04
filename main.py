import sys
import time

import speech_recognition as sr
import pyaudio

import retrieve_data

from pywinauto import Application

sys.path.append('../')
from obswebsocket import obsws, requests  # noqa: E402

def open_programs():
    obs_path = r"D:\obs-studio\bin\64bit\obs64.exe"
    obs_working_dir = r"D:\obs-studio\bin\64bit"
    app = Application()
    app.start(obs_path, work_dir=obs_working_dir)

    dlg_spec = app.window()
    dlg_spec.move_window(x=None, y=None, width=960, height=1080, repaint=True)
    
    #chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    #bookmark_url = "https://www.facebook.com/live/producer" 
    #subprocess.Popen([chrome_path, bookmark_url])
    
    

open_programs()



r = sr.Recognizer()
r.energy_threshold = 50
r.dynamic_energy_threshold = False

host = "localhost"
port = 4455
password = "secret"
ws = obsws(host, port, password)
ws.connect()

# Set the audio capture settings
chunk_size = 1024
sample_rate = 44100

# Open an audio stream to capture system audio
audio_stream = pyaudio.PyAudio().open(
    format=pyaudio.paInt16,
    channels=1,
    rate=sample_rate,
    input=True,
    frames_per_buffer=chunk_size,
)

def switchScene(name : str):
    try:
        print("Switching to {}".format(name))
        ws.call(requests.SetCurrentProgramScene(sceneName=name))
    except KeyboardInterrupt:
        pass

# Define the keywords to trigger camera switching
keywords = ['camera one', 'camera two']

# Continuously listen for audio and process speech
print("Listening for speech...")
while True:
    # Convert audio to text using speech recognition
    # Read audio data from the stream
    audio_data = audio_stream.read(chunk_size)

    try:
        # Convert audio to text using speech recognition
        audio_data = sr.AudioData(audio_data, sample_rate=sample_rate, sample_width=2)
        text = r.recognize_google(audio_data)

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
            
            
            
"""wav_file_path = 'audio.wav'

# Perform speech recognition on the WAV file
recognizer = sr.Recognizer()
with sr.AudioFile(wav_file_path) as source:
    audio = recognizer.record(source)
    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))"""

ws.disconnect()