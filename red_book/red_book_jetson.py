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
from random import randint
import torch

#######################################
# CHANGE TO RESPOND TO SOMETHING ELSE
activation_phrase = "right time"
deactivation_phrase = "thank you"
book_is_active = False
answer_length = 50
#######################################

# FIXED REPONSE LISTS
leave = [f for f in os.listdir("./audio_data/leave/") if f != ".DS_Store"]
summon = [f for f in os.listdir("./audio_data/summon/") if f != ".DS_Store" ]
thinking = [f for f in os.listdir("./audio_data/thinking/") if f != ".DS_Store" ]
generated_tts = "tts.wav"


# Timeout counter
empty_loop_count = 0

# For text cleanup and grammar check
d = TreebankWordDetokenizer()

print("LOADING MODELS")

device = "cuda" if torch.cuda.is_available() else "cpu"

# Load GPT Neo ML models
model = GPTNeoForCausalLM.from_pretrained("./gpt-neo-poetry", torch_dtype=torch.float32).to(device)
tokenizer = GPT2Tokenizer.from_pretrained("./gpt-neo-poetry")

# Load Bark
processor = AutoProcessor.from_pretrained("suno/bark-small")
model_bark = BarkModel.from_pretrained("suno/bark-small", torch_dtype=torch.float32).to(device)
sample_rate = model_bark.generation_config.sample_rate

#################################################
# ENABLE ON JETSON AND TEST
model_bark.enable_cpu_offload()
model_bark.to_bettertransformer()
#################################################

# Load STT models
stt_model = Model(r"vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(stt_model, 16000)


print("FINISHED LOADING")

# Mic Stream
mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
print("LISTENING")

def generate_prophecy(prompt):
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)
    gen_tokens = model.generate(input_ids, do_sample=True, temperature=0.9, early_stopping=False, top_k=30, max_length=answer_length, repetition_penalty = 1.2)
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
    

try:
    while True:
        try:
            
            #print("LOOP COUNT: " + str(empty_loop_count))
            # If book has been active without interactions for too long
            if book_is_active and empty_loop_count > 300:
                empty_loop_count = 0
                book_is_active = False

            if stream.is_stopped():
                stream.start_stream()
            
            data = stream.read(4096)

            if recognizer.AcceptWaveform(data):
                text = eval(recognizer.Result())
                human_said = text["text"]
                print("Human said:")
                print(human_said)

                if activation_phrase in human_said and not book_is_active:
                    stream.stop_stream()
                    empty_loop_count = 0
                    book_is_active = True

                    play_audio("summon", summon[randint(0, len(summon)-1)]);


                elif human_said.strip() and book_is_active: 
                    stream.stop_stream()
                    empty_loop_count = 0

                    if deactivation_phrase in human_said:
                        book_is_active = False

                        play_audio("leave", leave[randint(0, len(leave)-1)]);

                    else:
                        play_audio("thinking", thinking[randint(0, len(thinking)-1)]);
                        print("GENERATING")
                        start_time = time.time()
                        prophecy = generate_prophecy(human_said)
                        prophecy = str(clean_text(prophecy))
                        print()
                        print(prophecy)
                        print()

                        # TTS response
                        inputs = processor([prophecy], return_tensors="pt").to(device)
                        audio_array = model_bark.generate(**inputs, do_sample=True)
                        audio_array = audio_array.cpu().numpy().squeeze()

                        # save audio to disk
                        write_wav("./audio_data/generated/tts.wav", rate=sample_rate, data=audio_array)

                        # play response audio
                        play_audio("generated", generated_tts);

                        print("TIME IT TOOK: ")
                        print(str(time.time() - start_time) + "s.")
                        
                        human_said = " "

                else:
                    empty_loop_count+=1

            else: 
                empty_loop_count+=1



        except Exception as e:
            print(e)
            pass

except KeyboardInterrupt:
    quit()



