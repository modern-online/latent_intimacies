from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
from vosk import Model, KaldiRecognizer
import pyaudio
import sounddevice as sd
import soundfile as sf
import os
import time
from random import randint
import ast

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
preload_models()

model = Model(r"vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, 16000)

chatbot = ChatBot('Demolition')

# Mic Stream
mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)

print("FINISHED LOADING")

def process_and_train():

    trainer = ListTrainer(chatbot)

    with open("./clean_data/clean_data.txt", encoding="utf8") as text:
        dataset = text.read()
    
    # convert dataset from string to actual list 
    dataset = ast.literal_eval(dataset)
    
    # train model on conversation pairs
    for data in dataset:
        data = tuple(data)
        trainer.train(data)

def demolish_data(sentence):
    with open("./clean_data/clean_data.txt", encoding="utf8") as text:
        dataset = text.read()
        dataset = ast.literal_eval(dataset)
        for i, pair in enumerate(dataset):
            if sentence in pair:
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
    
    print("LISTENING")

    while True:
        try:
            if stream.is_stopped():
                stream.start_stream()
            
            data = stream.read(4096)

            if recognizer.AcceptWaveform(data):
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
                        print(response)
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
                        audio_array = generate_audio(str(response))

                        # save audio to disk
                        write_wav("./fixed_audio_data/generated/tts.wav", SAMPLE_RATE, audio_array)

                        # play response audio
                        play_audio("generated", generated_tts);

                        print("TIME IT TOOK: ")
                        print(str(time.time() - start_time) + "s.")
                        
                        # Ask if this response has been satisfactory
                        play_audio("satisfaction", satisfaction[randint(0, len(negative)-1)]);
        
        except Exception as e:
            print(e)
            pass

except KeyboardInterrupt():
    quit()