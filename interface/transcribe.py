import speech_recognition as sr
import sys

from util import logger

log = logger.setup_logger()

def transcribe_audio(filename):
    log.info(f'Transcribing audio for file {filename}')
    recognizer = sr.Recognizer()
    
    with sr.AudioFile(filename) as source:
        audio_data = recognizer.record(source)
        
        try:
            text = recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            print("Could not understand the audio")
        except sr.RequestError as e:
            print("Error occurred during transcription: {0}".format(e))

    return text

