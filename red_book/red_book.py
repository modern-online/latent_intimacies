#!/usr/bin/python3

from transformers import GPTNeoForCausalLM, GPT2Tokenizer
import nltk
from nltk.tokenize.treebank import TreebankWordDetokenizer
from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
import pyaudio
import sounddevice as sd
import soundfile as sf
from vosk import Model, KaldiRecognizer
import os
import time
from random import randint

#######################################
# CHANGE TO RESPOND TO SOMETHING ELSE
activation_phrase = "open book"
deactivation_phrase = "may i go"
book_is_active = False
answer_length = 45
#######################################

# FIXED REPONSE LISTS
leave = [f for f in os.listdir("./audio_data/leave/") if f != ".DS_Store"]
summon = [f for f in os.listdir("./audio_data/summon/") if f != ".DS_Store" ]
generated_tts = "tts.wav"


# Timeout counter
empty_loop_count = 0

# For text cleanup and grammar check
d = TreebankWordDetokenizer()

print("LOADING MODELS")

# Load GPT Neo ML models
model = GPTNeoForCausalLM.from_pretrained("./gpt-neo-poetry")
tokenizer = GPT2Tokenizer.from_pretrained("./gpt-neo-poetry")

# Load STT models
stt_model = Model(r"vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(stt_model, 16000)

# Load TTS models
preload_models()

print("FINISHED LOADING")

# Mic Stream
mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
print("LISTENING")

def generate_prophecy(prompt):
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids
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

                if human_said == activation_phrase:
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
                        print("GENERATING")
                        start_time = time.time()
                        prophecy = generate_prophecy(human_said)
                        prophecy = clean_text(prophecy)
                        print(prophecy)

                        # TTS response
                        audio_array = generate_audio(str(prophecy))

                        # save audio to disk
                        write_wav("./audio_data/generated/tts.wav", SAMPLE_RATE, audio_array)

                        # play response audio
                        play_audio("generated", generated_tts);

                        print("TIME IT TOOK: ")
                        print(str(time.time() - start_time) + "s.")

                else:
                    empty_loop_count+=1

            else: 
                empty_loop_count+=1



        except Exception as e:
            print(e)
            pass

except KeyboardInterrupt:
    quit()



