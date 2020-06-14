# Reference: https://pypi.org/project/SpeechRecognition/
# Reference: https://www.geeksforgeeks.org/speech-recognition-in-python-using-google-speech-api/
# Note this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr
import subprocess

def get_speech():
    # Set the device ID of the mic that we specifically want to use to avoid ambiguity

    MIC_NAME = "ATGM1-USB: USB Audio (hw:1,0)"
    
    for i, microphone_name in enumerate(sr.Microphone.list_microphone_names()):
        print(microphone_name)
        if(microphone_name == MIC_NAME):
            device_id = i
            break

    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone(device_index = device_id) as source:
        # clear console of errors
        subprocess.run("clear")

        # wait for a second to let the recognizer adjust the
        # energy threshold based on the surrounding noise level
        r.adjust_for_ambient_noise(source)

        print("What type of vehicle are you looking for?")
        try:
            audio = r.listen(source, timeout = 1.5)
        except sr.WaitTimeoutError:
            print("Listening timed out whilst waiting for phrase to start")
            quit()

        word = None

        # recognize speech using Google Speech Recognition
        try:

            word = r.recognize_google(audio, key = "https://www.googleapis.com/auth/assistant-sdk-prototype")
            print("I believe you said '{}'".format(word))
        except sr.UnknownValueError:
            word = "Google Speech Recognition could not understand audio"
        except sr.RequestError as e:
            word = "Could not request results from Google Speech Recognition service; {0}".format(e)

        return word
