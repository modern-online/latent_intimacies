#!/usr/bin/python3

from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
import sounddevice as sd
import soundfile as sf
import os
import time

os.environ["SUNO_OFFLOAD_CPU"] = "True"
#os.environ["SUNO_USE_SMALL_MODELS"] = "True"

# download and load all models
print("LOADING MDOELS")
preload_models()

print("GENERATING")
# generate audio from text

start_time = time.time()

text_prompt = """
     Hello, my name is Suno. And, uh — and I like pizza. [laughs] 
"""
audio_array = generate_audio(text_prompt)

# save audio to disk
write_wav("tts.wav", SAMPLE_RATE, audio_array)

data, fs = sf.read("tts.wav", dtype='float32')  
sd.play(data, fs)
status = sd.wait()  # Wait until file is done playing

print("TIME IT TOOK: ")
print(str(time.time() - start_time) + "s.")