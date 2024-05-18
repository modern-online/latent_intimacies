## About Demolition

Demolition is one of the three prototypes we built during a LAB#03: Synthetic Minds creative prototyping residency at Medialab Matadero in Madrid. Demolition, is site-specific, a block of concrete encapsulating half a dozen WhatsApp chats, our online interactions with those friends and family members who agreed to take part. We can ask anything we want, and the voice agent will try to give the best possible answer, by sampling text from this tiny, intimate dataset. It will then ask us to judge if its answer is relevant.

Using automation to erase unfavourable memories of past experiences liberates us from the fangs of yesterday. Confronting textual snippets of the past, stripped from their original context, can supply catharsis. At the same time, the interaction allows users to gauge and adjust their level of engagement, during the difficult process of mourning and moving on.

## Hardware

Our device runs on a [Jetson Orin Nano Developer Kit with a 8GB VRAM module](https://developer.nvidia.com/embedded/learn/get-started-jetson-orin-nano-devkit), coupled with a bluetooth headset.

## Software

In general,the code was written in Python, and uses [Pytorch](https://pytorch.org/) and [Transformers](https://huggingface.co/docs/transformers/en/index) machine leaarning modules for running [Bark](https://huggingface.co/docs/transformers/en/model_doc/bark) text-to-speech (TTS) engine by Suno AI, and a small old module for training chatbots with tiny datasets, [Chatterbot](https://chatterbot.readthedocs.io/en/stable/).


## A little disclaimer: 
This is a somewhat detailed tutorial as it is aimed at our principal audience, artists and designers fiddling with tech. It is an intermediate level project that requires some fundemantal understanding of computers as well as having dealt with creative coding in the past. For those who know their way around, the essentials are:

(1) Setting up a Jetson Orin Nano Development Kit  
(2) Pairing a bluetooth headset (or equivalent)  
(3) Installing python modules (with some somewhat more problematic than others, i.e. torch and Chatterbot)   
(4) Downloading/training/fine-tuning a custom language model  
(6) Automating  

Please also note that the repository contains two main files demolition.py and demolition_jetson.py. The main difference between the two is that demolition.py implements Bark from [source](https://github.com/suno-ai/bark) and has been tested on MacOS whereas the demolition_jetson uses the implementation via [Huggingface](https://huggingface.co/docs/transformers/en/model_doc/bark). At the time of development we had troubles with Pytorch (torchaudio in particular) compatibility on Jetson Nano, and a different approach was implemented.

## Installation

**(1)** Get the Jetson Orin running 

Follow this [guide](https://developer.nvidia.com/embedded/learn/get-started-jetson-orin-nano-devkit#prepare) depending on your developer kit module. If your kit is not from the official developer, follow their appropriate instructions. We used [Jetpack SDK 5.0.2](https://developer.nvidia.com/embedded/jetpack-sdk-502). 

**(2)**  Update the system and install Jetpack Components  

Open the terminal, then type:  
```sudo apt-get update```  
```sudo apt-get upgrade```  
```sudo apt-get install nvidia-jetpack```  

**(3)**  Install git and clone the repository  
```sudo apt-get install git```  
```git clone https://github.com/modern-online/latent_intimacies.git```  
The repository should now be in your /home folder. Clean up all the things you don't need. Also note that /utils folder contains some simple scripts that we used for testing along the way. 

**(4)** Setting up a working directory and a [virtual environment](https://docs.python.org/3/library/venv.html). 

A virtual environment is like a contained folder that holds all the modules and items necessary for your code to run. The advantage of it is that it keeps original Python folder intact, so in case you mess something up, you can just delete the virtual environment and start again. 

Inside the demolition folder, right-click then choose to open terminal. Type:  
```python -m venv demolenv```  
This creates a new virtual environment in a folder called demolenv. (In case you get an error message saying no such command as venv exists, follow what the error says to install the venv module for Python).   
```source demolenv/bin/activate```  
activates the virtual environment.   
You should now see <em>(redenvironment)</em> on the left of your command line. Please read the above documentation link to understand how virtual environments work. You are now ready to install the actual project. 

**(5)** Installing Python modules

#### Another little disclaimer for those who know their way around: Typically, I would export a requirements file listing all the needed modules, but since we're building things on a Jetson, many standard versions would not work. Hence it's best to just install the latest Jetson-supported module version depending on your OS.

Install a precompiled **torch** (or you can compile but it will take a few hours):  
Download a precompiled version [here](https://forums.developer.nvidia.com/t/pytorch-for-jetson/72048). At the time, we used PyTorch v2.1.0 for Jetpack 5.  
Put it in your the demolition folder.   
In terminal (assuming you're in the redbook folder, and that your virtual environment is active), type:  
```pip install [the name of the package you downloaded.whl]```  

Install audio drivers:  
```sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0```  
```sudo apt-get install ffmpeg libav-tools```  

Now install remaining modules:
``` pip install transformers nltk scipy sounddevice soundfile vosk```  

