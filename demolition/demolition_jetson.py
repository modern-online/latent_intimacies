#!/usr/bin/python3

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from transformers import AutoProcessor, BarkModel
from scipy.io.wavfile import write as write_wav
from vosk import Model, KaldiRecognizer
import pyaudio
import sounddevice as sd
import soundfile as sf
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

processor = AutoProcessor.from_pretrained("suno/bark-small")
model_bark = BarkModel.from_pretrained("suno/bark-small", torch_dtype=torch.float32).to(device)
sample_rate = model_bark.generation_config.sample_rate
#model_bark.enable_cpu_offload()
model_bark = model_bark.to_bettertransformer()

model = Model(r"vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, 16000)


# Mic Stream
mic = pyaudio.PyAudio()

print("FINISHED LOADING")

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

    print("DATA ENTRIES REMAINING:")
    print(len(dataset))

    # Increase division value for randomly sampling dataset if training is too slow   
    sample_size = int(len(dataset) / 40)
    dataset = choices(dataset, k=sample_size)
    
    trainer.train(dataset)
    
    print("TIME TRAINER TOOK")
    print(str(time.time()-start_time) + "s.")

def demolish_data(sentence):
    with open("./clean_data/clean_data.txt") as text:
        dataset = text.read()
        dataset = ast.literal_eval(dataset)
        
        for i, data in enumerate(dataset):
        	if str(sentence) in str(data):
        		print("DELETING")
        		print(str(data))
        		dataset.pop(i)

    with open("./dirty_data/temp_data.txt", "w") as f:
        f.write(str(dataset))

    os.remove("./clean_data/clean_data.txt")
    os.rename("./dirty_data/temp_data.txt", "./clean_data/clean_data.txt")

def play_audio(container, file):
    filename = f'./fixed_audio_data/{container}/{file}'
    data, fs = sf.read(filename, dtype='float32')  
    sd.play(data, fs)
    status = sd.wait()  # Wait until file is done playing 

try:

    # Train the algorithm for the first time
    process_and_train()
    
    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    human = ""
    
    
    print("LISTENING")

    while True:
        try:
            if stream.is_stopped():
                stream.start_stream()
            
            data = stream.read(4096)

            if recognizer.AcceptWaveform(data):
                human = ""
                text = eval(recognizer.Result())
                human = text["text"]
                print("Human said:")
                print(human)

                if human:
                    stream.stop_stream()

                    if human.strip() == "yes":
                        play_audio("positive", positive[randint(0, len(negative)-1)]);
                    
                    elif human.strip() == "no":
                        play_audio("negative", negative[randint(0, len(negative)-1)]);
                        demolish_data(response)
                        process_and_train()

                    else: 

                        play_audio("thinking", thinking[randint(0, len(negative)-1)]);

                        print("GENERATING")
                        start_time = time.time()

                        # Get a response to an input statement
                        response = chatbot.get_response(human)
                        print(response)

                        # TTS response
                        inputs = processor([str(response)], return_tensors="pt").to(device)
                        audio_array = model_bark.generate(**inputs, do_sample=True)
                        audio_array = audio_array.cpu().numpy().squeeze()

                        # save audio to disk
                        write_wav("./fixed_audio_data/generated/tts.wav", rate=sample_rate, data=audio_array)

                        # play response audio
                        play_audio("generated", generated_tts);

                        print("TIME IT TOOK: ")
                        print(str(time.time() - start_time) + "s.")
                        
                        # Ask if this response has been satisfactory
                        play_audio("satisfaction", satisfaction[randint(0, len(negative)-1)])
                        
                        human = ""
        except Exception as e:
            print(e)
            pass

except KeyboardInterrupt():
    quit()
