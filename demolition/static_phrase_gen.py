from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
import sounddevice as sd
import soundfile as sf
import os
import time

os.environ["SUNO_OFFLOAD_CPU"] = "True"

# download and load all models
print("LOADING MDOELS")
preload_models()

thinking_prompt = "thinking"
positive_prompt = "thank you, my answer will be remembered"
negative_prompt = "my answer has been forgotten"
satisfaction_query = "were you sattisfied with my answer, yes or no?"

def generate_tts(index, prompt, name):
    audio_array = generate_audio(prompt)
    # save audio to disk
    write_wav(f'{name}{index}.wav', SAMPLE_RATE, audio_array)

print("GENERATING")
# generate audio from text

for index in range(1,5):
    generate_tts(index=index, prompt=thinking_prompt, name="thinking")
    generate_tts(index=index, prompt=positive_prompt, name="positive")
    generate_tts(index=index, prompt=negative_prompt, name="negative")
    generate_tts(index=index, prompt=satisfaction_query, name="satisfaction")

print("Done")
