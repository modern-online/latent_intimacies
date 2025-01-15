#!/home/latent-intimacies/Desktop/demolition/.venv/bin/python

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from transformers import AutoProcessor, BarkModel
from scipy.io.wavfile import write as write_wav
from vosk import Model, KaldiRecognizer
from optimum.bettertransformer import BetterTransformer
import gc
import pyaudio
import sounddevice as sd
import soundfile as sf
from num2words import num2words
from time import sleep
import os
import time
from random import randint, choices
import ast
import torch

response = ""

dataset = "data.txt"

# FIXED REPONSE LISTS
negative = [f for f in os.listdir("./fixed_audio_data/negative/") if f != ".DS_Store"]
positive = [f for f in os.listdir("./fixed_audio_data/positive/") if f != ".DS_Store" ]
satisfaction = [f for f in os.listdir("./fixed_audio_data/satisfaction/") if f != ".DS_Store" ]
thinking = [f for f in os.listdir("./fixed_audio_data/thinking/") if f != ".DS_Store" ]
generated_tts = "tts.wav"

os.environ["SUNO_OFFLOAD_CPU"] = "True"
#os.environ["SUNO_USE_SMALL_MODELS"] = "True"

# download and load all models
print("LOADING MODELS")

device = "cuda" if torch.cuda.is_available() else "cpu"

print("LOADING BARK")
processor = AutoProcessor.from_pretrained("suno/bark-small")
model_bark = BarkModel.from_pretrained("suno/bark-small", torch_dtype=torch.float32)
time.sleep(5)
#print("TRANSFERING TO GPU")
#gc.collect()
#print(f'Available GPU Memory: {torch.cuda.get_device_properties(0).total_memory}')
#print(f'Reserved GPU Memory: {torch.cuda.memory_reserved(0)}')
#print(f'Allocated GPU Memory: {torch.cuda.memory_allocated(0)}')
#model_bark = model_bark.cuda()
#print(f'Allocated GPU Memory post GPU loading: {torch.cuda.memory_allocated(0)}')
#print("TRANSFERED")
time.sleep(5)
sample_rate = model_bark.generation_config.sample_rate
#model_bark = model_bark.to_bettertransformer()
model_bark = BetterTransformer.transform(model_bark, keep_original_model=False)
model_bark.enable_cpu_offload()
print("LOADED BARK")
time.sleep(5)
model = Model(r"vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, 16000)
print("LOADED VOSK")

time.sleep(5)

print("MOVING BARK TO GPU")
torch.cuda.empty_cache()
for param in model_bark.parameters():
    print(param.data) 
    param.data = param.data.to(device)
print("FINISHED LOADING")

time.sleep(5)

# Mic Stream
print("INITIALIZING MIC")
mic = pyaudio.PyAudio()
time.sleep(1)
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
time.sleep(3)
print("MIC INTITIALIZED")

def process_and_train():
    start_time = time.time()
    if os.path.isfile("./db.sqlite3-wal"):
        os.remove("./db.sqlite3-wal")
    if os.path.isfile("./db.sqlite3-shm"):
        os.remove("./db.sqlite3-shm")
    if os.path.isfile("./db.sqlite3"):
        os.remove("./db.sqlite3")

    global chatbot
    chatbot = ChatBot('Demolition')
    trainer = ListTrainer(chatbot)

    with open("./clean_data/clean_data.txt", encoding="utf8") as text:
        dataset = text.read()

    # convert dataset from string to actual list 
    dataset = ast.literal_eval(dataset)
    
    remaining_entries = len(dataset)
    print("DATA ENTRIES REMAINING:")
    print(remaining_entries)

    # Increase division value for randomly sampling dataset if training is too slow   
    sample_size = int(len(dataset) / 40)
    dataset = choices(dataset, k=sample_size)
    
    trainer.train(dataset)
    
    print("TIME TRAINER TOOK")
    print(str(time.time()-start_time) + "s.")

    return remaining_entries

def demolish_data(sentence):
    with open("./clean_data/clean_data.txt") as text:
        dataset = text.read()
        dataset = ast.literal_eval(dataset)
        deleted = True

        if (len(dataset) > 1):
            for i, data in enumerate(dataset):
                if str(sentence) in str(data):
                    #print("DELETING")
                    #print(str(data))
                    dataset.pop(i)
        
        else: 
            deleted = False

    with open("./dirty_data/temp_data.txt", "w") as f:
        f.write(str(dataset))

    os.remove("./clean_data/clean_data.txt")
    os.rename("./dirty_data/temp_data.txt", "./clean_data/clean_data.txt")
    return deleted

def play_audio(container, file):
    filename = f'./fixed_audio_data/{container}/{file}'
    data, fs = sf.read(filename, dtype='float32')  
    sd.play(data, fs)
    status = sd.wait()  # Wait until file is done playing 

try:
    
    # Train the algorithm for the first time
    remaining_entries = process_and_train()
    
    print("LISTENING")
    play_audio("thinking", thinking[randint(0, len(negative)-1)]);
    time.sleep(3)
    
    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    human = ""

    while True:
        try:
            if stream.is_stopped():
                stream.start_stream()
            
            data = stream.read(4096)

            if recognizer.AcceptWaveform(data):
                human = ""
                text = eval(recognizer.Result())
                human = text["text"]

                if human and not human == 'huh': # somehow the new mic tends to hear "huh"
                    print("Human said:")
                    print(human)
                    stream.stop_stream()
                    
                    play_audio("thinking", thinking[randint(0, len(negative)-1)]);

#                    if human.strip() == "yes":
#                        play_audio("positive", positive[randint(0, len(negative)-1)]);
                    
#                    elif human.strip() == "no":
#                        play_audio("negative", negative[randint(0, len(negative)-1)]);
#                        demolish_data(response)
#                        process_and_train()

#                    else: 

                        #play_audio("thinking", thinking[randint(0, len(negative)-1)]);
			
                    print("GENERATING")
                    start_time = time.time()

                    # Get a response to an input statement
                    response = chatbot.get_response(human)
                    print(response)

                    demolished = demolish_data(response)

                    if demolished: 
                        response = str(response) + " has been forgotten."
                    else:
                        response = str(response)

                    response += num2words(remaining_entries) + " entries remaining."

                    # TTS response
                    inputs = processor([response], return_tensors="pt").to(device)
                    audio_array = model_bark.generate(**inputs, do_sample=True)
                    audio_array = audio_array.cpu().numpy().squeeze()

                    # save audio to disk
                    write_wav("./fixed_audio_data/generated/tts.wav", rate=sample_rate, data=audio_array)
                    
                    process_and_train()
		     	
                    # play response audio
                    play_audio("generated", generated_tts);

                    print("TIME IT TOOK: ")
                    print(str(time.time() - start_time) + "s.")
                    
                    # Ask if this response has been satisfactory
#                    play_audio("satisfaction", satisfaction[randint(0, len(negative)-1)])
                    
                    
                    human = ""

                    sleep(1)


        except Exception as e:
            print(e)
            pass

except KeyboardInterrupt():
    quit()
