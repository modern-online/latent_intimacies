## About Demolition

Demolition is one of the three prototypes we built during a LAB#03: Synthetic Minds creative prototyping residency at Medialab Matadero in Madrid. Demolition, is site-specific, a block of concrete encapsulating half a dozen WhatsApp chats, our online interactions with those friends and family members who agreed to take part. We can ask anything we want, and the voice agent will try to give the best possible answer, by sampling text from this tiny, intimate dataset. It will then ask us to judge if its answer is relevant.

Using automation to erase unfavourable memories of past experiences liberates us from the fangs of yesterday. Confronting textual snippets of the past, stripped from their original context, can supply catharsis. At the same time, the interaction allows users to gauge and adjust their level of engagement, during the difficult process of mourning and moving on.

## Hardware

Our device runs on a [Jetson Orin Nano Developer Kit with a 8GB VRAM module](https://developer.nvidia.com/embedded/learn/get-started-jetson-orin-nano-devkit), coupled with a bluetooth headset.

## Software

In general,the code was written in Python, and uses [Pytorch](https://pytorch.org/) and [Transformers](https://huggingface.co/docs/transformers/en/index) machine leaarning modules for running [Bark](https://huggingface.co/docs/transformers/en/model_doc/bark)text-to-speech (TTS) engine by Suno AI, and a small old module for training chatbots with tiny datasets, [Chatterbot](https://chatterbot.readthedocs.io/en/stable/).


## A little disclaimer: 
This is a somewhat detailed tutorial as it is aimed at our principal audience, artists and designers fiddling with tech. It is an intermediate level project that requires some fundemantal understanding of computers as well as having dealt with creative coding in the past. For those who know their way around, the essentials are:

(1) Setting up a Jetson Orin Nano Development Kit  
(2) Pairing a bluetooth headset (or equivalent)  
(3) Installing python modules (with some somewhat more problematic than others, i.e. torch and Chatterbot)   
(4) Downloading/training/fine-tuning a custom language model  
(6) Automating  

Please also note that the repository contains two main files demolition.py and demolition_jetson.py. The main difference between the two is that demolition.py implements Bark from [source](https://github.com/suno-ai/bark) and has been tested on MacOS whereas the demolition_jetson uses the implementation via [Huggingface](https://huggingface.co/docs/transformers/en/model_doc/bark). At the time of development we had troubles with Pytorch (torchaudio in particular) compatibility on Jetson Nano, and a different approach was implemented.


