#!/usr/bin/python3

from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
import sounddevice as sd
import soundfile as sf
import os
import time

# HOW MANY SAMPLES TO GENERATE?
samples = 4

os.environ["SUNO_OFFLOAD_CPU"] = "True"

# download and load all models
print("LOADING MOEDLS")
preload_models()

summon_prompt = "As good a time as any."
leave_prompt = "Your presence is no longer required"

def generate_tts(index, prompt, name):
    audio_array = generate_audio(prompt)
    # save audio to disk
    write_wav(f'{name}{index}.wav', SAMPLE_RATE, audio_array)

print("GENERATING")
# generate audio from text

for index in range(1, samples):
    generate_tts(index=index, prompt=summon_prompt, name="summon")
    #generate_tts(index=index, prompt=leave_prompt, name="leave")

print("Done")
