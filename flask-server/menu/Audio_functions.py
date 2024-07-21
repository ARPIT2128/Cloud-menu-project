"""
THIS MODULE INCLUEDS THE FUNCTION REALATED TO AUDIO TASKS
----------------------------------------------------------------
1. speech_to_text() : This function is used to convert the audio input to
a text representation of the audio.

2. text_to_audio() : This function is used to convert the text input to a 
audio representation of the text.

"""

import speech_recognition as sr
from gtts import gTTS
import os 

def speech_to_text():
    """
    This function is used to convert the audio input to
    a text representation of the audio. It usese the `speech_recognition` module for speech detection.
    -Parameters:
        - No parameters
    -Returns: text representation of the audio.

    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise, please wait...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        
        audio_data = recognizer.listen(source)
        print("Recognizing...")
        
        try:
            text = recognizer.recognize_google(audio_data)
            print(f"Recognized Text: {text}")
        except sr.UnknownValueError:
            print("Google Web Speech API could not understand the audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Web Speech API; {e}")
    return text


def text_to_speech(text, language='en',filename="text_to_speech"):
    """
    The provided functional document outlines a Python function `text_to_speech`, which utilizes the Google Text to Speech (gTTS) API to convert text into speech and save it as an MP3 file. Key points include:
    - API Used: Google Text to Speech (gTTS).
    - Functionality: Converts input text into speech and saves it as an MP3 file.
    - Parameters:
        - text: The text to be converted into speech.
        - language: The language of the speech (default is English, 'en').
        - filename: The name of the output MP3 file (default is "text_to_speech").
    - Language Support: gTTS supports multiple languages including English, Hindi, Tamil, French, and German.
    - Audio Speed: The speech can be generated at two speeds, fast or slow, but this function sets it to fast by default.
    - Voice Customization: The current gTTS API does not support changing the voice of the generated audio.
    """
    speech = gTTS(text=text, lang= language,slow=False)
    speech.save(f"{filename}.mp3")



