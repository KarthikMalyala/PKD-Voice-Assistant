## PKD Voice Assistant
## Karthik Malyala

import speech_recognition as sr
import pyaudio
import pvporcupine
import pyttsx3
import time
import struct
import winsound

def speak(text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice',voices[0].id)
    print('\n' + 'LARRI: ' + text + ' \n')
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.... \n", end="")
        audio = r.listen(source)
        query = ''

        try:
            print("Recognizing...\n", end="")
            query = r.recognize_google(audio, language= 'en-US')
            #print(f"User said: {query}")

        except Exception as e:
            print("Exception: " + str(e))

    return query.lower()


def flow():
    global enable
    userSaid = takeCommand()
    if "stop" in userSaid:
        speak("Stopping Sir")
        enable = False
    else:
        speak(userSaid)
    time.sleep(1)

def main():
    porcupine = None
    audio = None
    stream = None

    try:
        porcupine = pvporcupine.create(access_key="GIPgOzykL7Rk71C8Z+0ZTe1ne4i6yNwe1rRGEvKpiCQbYITdiEX6/A==", keyword_paths=["C:\LARRI\PKD\philip_en_windows_v2_1_0.ppn"])
        audio = pyaudio.PyAudio()
        stream = audio.open(rate=porcupine.sample_rate,
                            channels=1,
                            format=pyaudio.paInt16,
                            input=True,
                            frames_per_buffer=porcupine.frame_length)

        while True:
            pc_output = stream.read(porcupine.frame_length)
            pc_output = struct.unpack_from("h" * porcupine.frame_length, pc_output)
            keyword_index = porcupine.process(pc_output)
            if keyword_index >= 0:
                print("Wake Word Detected.. \n", end="")
                winsound.Beep(200, 800)
                flow()
                time.sleep(1)
                if enable == False:
                    print("\nThank you!")
                    break
                print("LARRI: Awaiting next command")
    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio is not None:
            audio.close(stream)

enable = True
main()

