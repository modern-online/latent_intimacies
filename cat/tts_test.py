#!/usr/bin/python3

import pyttsx3
engine = pyttsx3.init()
engine.setProperty('rate', 115)
voices = engine.getProperty('voices')  
for i, voice in enumerate(voices):
    print(i, voice.id, voice.name)
engine.setProperty('voice', voices[113].id)
## 15 Brian (UK)

engine.say("I will speak this text")
engine.runAndWait()