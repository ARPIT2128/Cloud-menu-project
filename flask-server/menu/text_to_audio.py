# There are several APIs available to convert text to speech in Python. 
# One of such APIs is the Google Text to Speech API commonly known as the gTTS API. 
# gTTS is a very easy to use tool which converts the text entered, into audio which can be saved as a mp3 file.
# The gTTS API supports several languages including English, Hindi, Tamil, French, German and many more.
# The speech can be delivered in any one of the two available audio speeds, fast or slow. 
# However, as of the latest update, it is not possible to change the voice of the generated audio.

from gtts import gTTS
import os 

Text_to_convert = input("Text to convert:")

language = 'en'

speech = gTTS(text=Text_to_convert, lang= language,slow=False)

speech.save("sagemaker.mp3")

os.system("start sagemaker.mp3")