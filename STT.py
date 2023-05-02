## PKD Voice Assistant
## Karthik Malyala

import speech_recognition as sr
import re
import asyncio
import pyaudio
import pvporcupine
import pyttsx3
import time
import struct
import winsound
from EdgeGPT import Chatbot, ConversationStyle
from responsive_voice import ResponsiveVoice

async def process(prompt):
    bot = Chatbot(cookiePath='cookies.json')
    response = await bot.ask(prompt=prompt, conversation_style=ConversationStyle.balanced)

    for message in response["item"]["messages"]:
        if message["author"] == "bot":
            bot_response = message["text"]

    # Select only the bot response from the response dictionary
    for message in response["item"]["messages"]:
        if message["author"] == "bot":
            bot_response = message["text"]
    # Remove [^#^] citations in response
    bot_response = re.sub(r'\b[A-Z][^?]*\?\b', '', bot_response)
    bot_response = re.sub('\[\^\d+\^\]', '', bot_response)
    bot_response = re.sub('Hello, this is Bing. ', '', bot_response)
    bot_response = re.sub('😊', '', bot_response)
    await bot.close()
    return bot_response

def speak(text):
    engine = ResponsiveVoice(gender=ResponsiveVoice.MALE, lang=ResponsiveVoice.ENGLISH_GB, pitch=0.4, rate=0.5, vol=1)
    #engine = pyttsx3.init('sapi5')
    #voices = engine.getProperty('voices')
    #engine.setProperty('voice',voices[0].id)
    if text == "Stopping Sir" or text == "":
        engine.say(text, blocking=True)
    else:
        print('\n' + 'You asked: ' + text + ' \n')
        output = asyncio.run(process(text))
        print('LARRI: ' + output + ' \n')
        engine.say(output, blocking=True)

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone(device_index=2) as source:
        print("Listening.... \n", end="")
        audio = r.listen(source)
        query = ''

        try:
            print("Recognizing...\n", end="")
            query = r.recognize_google(audio, language= 'en-US')

        except Exception as e:
            print("Exception: " + str(e))

    return query.lower()

def flow():
    global enable
    userSaid = takeCommand()
    if "stop" in userSaid or "no" in userSaid:
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