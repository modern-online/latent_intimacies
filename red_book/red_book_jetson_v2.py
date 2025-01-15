#!/usr/bin/python3

from transformers import GPTNeoForCausalLM, GPT2Tokenizer, AutoProcessor, BarkModel
import nltk
from nltk.tokenize.treebank import TreebankWordDetokenizer
from scipy.io.wavfile import write as write_wav
import pyaudio
import sounddevice as sd
import soundfile as sf
from vosk import Model, KaldiRecognizer
import os
import time
import random
import torch
import accel

#######################################
# CHANGE TO RESPOND TO SOMETHING ELSE
answer_length = 40
starting_prompts = ["The last watch recorded strange lights in glassware", "Time collects at the bottom of the hour, waiting to be stirred", "Between the third and fourth spoonful, the future changes its mind", "Browser cache, coffee grounds, the goose-neck kettle's angular certainties", "Drawers calculate in dropped hairpins and forgotten keys", "The freezer door opens onto routes that cargo ships forgot, forever buffering", "Between inventory and prophecy, porcelain holds patterns of probable storms"]
#######################################

was_swinging = False
nullify_sensor = False

# FIXED REPONSE LISTS
thinking = [f for f in os.listdir("./audio_data/thinking/") if f != ".DS_Store" ]

# For text cleanup and grammar check
d = TreebankWordDetokenizer()


def generate_prophecy(prompt):
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)
    gen_tokens = model.generate(input_ids, do_sample=True, temperature=0.9, early_stopping=False, top_k=50, max_new_tokens=answer_length, repetition_penalty = 1.3)
    prophecy = tokenizer.batch_decode(gen_tokens)[0]
    prophecy = prophecy.replace(prompt, "")
    prophecy = clean_text(prophecy)
    return prophecy

def clean_text(input):
    sentences = nltk.sent_tokenize(input)
    sentences[0].strip()
    # If there's at least one complete sentence in generated prophecy
    if len(sentences) > 1:
        sentences.pop()
    sentences = d.detokenize(sentences)
    return sentences

def play_audio(container, file):
    filename = f'./audio_data/{container}/{file}'
    data, fs = sf.read(filename, dtype='float32')  
    sd.play(data, fs)
    status = sd.wait()  # Wait until file is done playing 

# ===========================================================================

print("LOADING MODELS")

device = "cuda" if torch.cuda.is_available() else "cpu"

# Load GPT Neo ML models
model = GPTNeoForCausalLM.from_pretrained("./gpt-neo-poetry", torch_dtype=torch.float32).to(device)
tokenizer = GPT2Tokenizer.from_pretrained("./gpt-neo-poetry")

# Load Bark
processor = AutoProcessor.from_pretrained("suno/bark-small")
model_bark = BarkModel.from_pretrained("suno/bark-small", torch_dtype=torch.float32)
sample_rate = model_bark.generation_config.sample_rate

print("MOVING GPT TO GPU")
torch.cuda.empty_cache()
for param in model.parameters():
    #print(param.data) 
    param.data = param.data.to(device)
print("FINISHED MOVING GPT")

print("MOVING BARK TO GPU")
for param in model_bark.parameters():
    #print(param.data) 
    param.data = param.data.to(device)
print("FINISHED MOVING BARK")

#################################################
# ENABLE ON JETSON AND TEST FOR PERFORMANCE
model_bark.enable_cpu_offload()
model_bark.to_bettertransformer()
#################################################

print("FINISHED LOADING")

play_audio("thinking", thinking[random.randint(0, len(thinking)-1)])
time.sleep(3)

try:
    while True:
        try:
            
            # Check accellerometer data
            # Returns True if device is shaking
            is_swinging = accel.is_moving(nullify_sensor)
            nullify_sensor = False
            
            # returns a random .wav
            if is_swinging:
                audio_files = os.listdir("./audio_data/generated/")
                if audio_files:
                    file_pick = random.choice(audio_files)
                    play_audio("generated", file_pick)
                was_swinging = True

            else:
                if was_swinging:
                    time.sleep(5)
                    play_audio("thinking", thinking[random.randint(0, len(thinking)-1)])
                    was_swinging = False
                    
                    if file_pick and len(audio_files) > 20:
                        text_file = file_pick.replace(".wav", ".txt")
                        text_file_path = f"./text_data/generated/{text_file}"

                        if os.path.isfile(text_file_path):
                            with open(text_file_path, "r") as f:
                                prompt = f.read()
                        else:
                            prompt = random.choice(starting_prompts)
                    
                    else:
                        prompt = random.choice(starting_prompts)

                    print("GENERATING NEW PROPHECY")
                    start_time = time.time()
                    prophecy = generate_prophecy(prompt)
                    prophecy = str(clean_text(prophecy))
                    
                    print()
                    print(prophecy)
                    print()

                    # TTS response
                    inputs = processor([prophecy], return_tensors="pt").to(device)
                    audio_array = model_bark.generate(**inputs, do_sample=True)
                    audio_array = audio_array.cpu().numpy().squeeze()

                    # save audio to disk
                    timestr = time.strftime("%Y%m%d-%H%M%S")
                    filename = f'tts_{timestr}'
                    write_wav(f"./audio_data/generated/{filename}.wav", rate=sample_rate, data=audio_array)

                    # save prompt in a file
                    with open(f"./text_data/generated/{filename}.txt", "w+") as f:
                        f.write(prophecy)


                    # play response audio
                    play_audio("generated", f'{filename}.wav');

                    print("TIME IT TOOK: ")
                    print(str(time.time() - start_time) + "s.")
                    
                    nullify_sensor = True

                time.sleep(.5)

        except Exception as e:
            print(e)
            pass

except KeyboardInterrupt:
    quit()
