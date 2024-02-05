#!/usr/bin/python3

import torch
from transformers import AutoTokenizer, CLIPImageProcessor, AutoModel, AutoModelForCausalLM
from transformers.models.auto.configuration_auto import AutoConfig
from src.vision_encoder_decoder import SmallCap, SmallCapConfig
from src.gpt2 import ThisGPT2Config, ThisGPT2LMHeadModel
from src.utils import prep_strings, postprocess_preds
from src.retrieve_caps import *
import json
from PIL import Image
import time
import cv2
from random import randint
import pyttsx3

device = "cpu"

####################################################
# IMAGE PATH
image_path = 'data/image.jpg'
# TIME BETWEEN IMAGES
interval = 10
# TEXT FILE FOR SAVING CAPTIONS
captions_file = 'data/dump.txt'
# CHANGE VOICE BETWEEN MALE AND FEMALE
voice = 15; # 15 UK Brian ,
####################################################

print("LOADING MODELS...")

# load feature extractor
feature_extractor = CLIPImageProcessor.from_pretrained("openai/clip-vit-base-patch32")

# load and configure tokenizer
tokenizer = AutoTokenizer.from_pretrained("gpt2")
tokenizer.pad_token = '!'
tokenizer.eos_token = '.'

# load models

AutoConfig.register("this_gpt2", ThisGPT2Config)
AutoModel.register(ThisGPT2Config, ThisGPT2LMHeadModel)
AutoModelForCausalLM.register(ThisGPT2Config, ThisGPT2LMHeadModel)
AutoConfig.register("smallcap", SmallCapConfig)
AutoModel.register(SmallCapConfig, SmallCap)
model = AutoModel.from_pretrained("Yova/SmallCap7M")
model= model.to(device)

template = open('src/template.txt').read().strip() + ' '

captions = json.load(open('datastore/coco_index_captions.json'))
retrieval_model, feature_extractor_retrieval = clip.load("RN50x64", device=device)
retrieval_index = faiss.read_index('datastore/coco_index')

# initialize tts
engine = pyttsx3.init()
engine.setProperty('rate', 125)
voices = engine.getProperty('voices')  
engine.setProperty('voice', voices[voice].id)

print("OPENING CAMERA...")
# Open a camera (0 is usually the default camera)
cap = cv2.VideoCapture(0)
# Check if the camera is opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()


print("FINISHED LOADING STUFF")

def retrieve_nns(image_embedding, index, k=4):
    xq = image_embedding.astype(np.float32)
    _, I = index.search(xq, k) 
    return I

print("READING MESSAGES FROM THE PREVIOUS TIME")
# Read and speak out all the captions from the previous session
with open(captions_file, 'r+') as f:
    previous_captions = f.readlines()
    if previous_captions:
        for caption in previous_captions:
            engine.say(caption)
            engine.runAndWait()
    # clean the file
    f.truncate(0)

try:
    while True: 
        try:
            print("STARTING NEW CAPTURE")
            start = time.time()

            # Capture a single frame
            for iter in range(3):
                _, frame = cap.read()

            # Save the frame
            cv2.imwrite(image_path, frame)
            
            print("IMAGE SAVED")

            time.sleep(3)

            print("ANALYZING")

            image = Image.open(image_path).convert("RGB")

            start = time.time()

            pixel_values_retrieval = feature_extractor_retrieval(image).to(device)
            with torch.no_grad():
                image_embedding = retrieval_model.encode_image(pixel_values_retrieval.unsqueeze(0)).cpu().numpy()

            nns = retrieve_nns(image_embedding, retrieval_index)[0]
            caps = [captions[i] for i in nns][:4]

            # prepare prompt
            decoder_input_ids = prep_strings('', tokenizer, template=template, retrieved_caps=caps, k=4, is_test=True)

            # generate caption
            pixel_values = feature_extractor(image, return_tensors="pt").pixel_values
            with torch.no_grad():
                pred = model.generate(pixel_values.to(device),
                                    decoder_input_ids=torch.tensor([decoder_input_ids]).to(device),
                                    max_new_tokens=25, no_repeat_ngram_size=0, length_penalty=0,
                                    min_length=1, num_beams=3, eos_token_id=tokenizer.eos_token_id)

            print("\nNICE CAPTION:")
            alternative_caption = tokenizer.decode(decoder_input_ids).split('\n')
            alternative_caption = [item for item in alternative_caption if item.strip() != ""][1:-1]
            random_index = randint(1, len(alternative_caption)-1)
            alternative_caption = alternative_caption[random_index]
            
            # clean "is" or "are" from the caption
            alternative_caption = alternative_caption.replace(" is ", " ")
            alternative_caption = alternative_caption.replace(" are ", " ")

            # say and print the caption
            print(alternative_caption)
            engine.say(f'I saw {alternative_caption}')
            engine.runAndWait()

            # append caption to text file
            with open(captions_file, 'a') as f:
                f.write(f'\n I saw {alternative_caption}')

            print("\nREAL CAPTION:")
            print(postprocess_preds(tokenizer.decode(pred[0]), tokenizer))
            print()
            
            print("TIME IT TOOK: ")
            print(str(time.time()-start) + "s.")
            print()

            print("WAITING FOR THE NEXT IMAGE")
            time.sleep(interval)

        except Exception as e:
            print(e)
            pass

except KeyboardInterrupt():
    cap.release()
    print('Done')