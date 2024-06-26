## _Demolition_

_Demolition_ is one of the three prototypes we built during the LAB#03: Synthetic Minds creative prototyping residency at Medialab Matadero in Madrid. _Demolition_ is site-specific, a block of concrete encapsulating half a dozen WhatsApp chats, our online interactions with those friends and family members who agreed to take part. You can ask anything you want, and the voice agent will try to supply the best possible answer, sampling text from this tiny, intimate dataset. It will then ask you to judge if its answer is relevant.


## Contents

- [Overview](#overview)
- [Hardware](#hardware)
- [Software](#software)
- [Small disclaimer](#small-disclaimer)
- [Installation](#installation)
- [Training ChatterBot with custom data](#training-chatterbot-with-custom-data)
- [Launching the script](#launching-the-script)
- [Automation](#automation)


## Overview

Using automation to erase memories of past experiences can liberate us from the fangs of yesterday. Revisiting prior interactions through _Demolition_'s constrained interface conjures flashes of past generosity, intimacy, and care – digital residues by turns gratifying and disconcerting. Textual snippets of the past, stripped from their original context, can supply catharsis. At the same time, the interaction allows users to calibrate their engagement, asserting their agency in the difficult process of mourning and moving on. 


## Hardware

Our device runs on a [Jetson Orin Nano Developer Kit with a 8GB VRAM module](https://developer.nvidia.com/embedded/learn/get-started-jetson-orin-nano-devkit), chosen for its superior performance and compatibility with machine learning tasks. It is paired with a Bluetooth headset to facilitate audio interactions with the device.


## Software

The code was written in Python, and uses [Pytorch](https://pytorch.org/) and [Transformers](https://huggingface.co/docs/transformers/en/index) machine learning modules for running Suno AI's fully generative [Bark](https://huggingface.co/docs/transformers/en/model_doc/bark) text-to-speech (TTS) engine, and [ChatterBot](https://chatterbot.readthedocs.io/en/stable/), a small, old module for training chatbots with tiny datasets.


## Small disclaimer:

This is a fairly detailed tutorial aimed at our principal audience, artists and designers fiddling with tech. It is an intermediate-level project that requires a fundamental understanding of computers, and some prior experience of creative coding. For those who know their way around, the essentials are:

1. Setting up a Jetson Orin Nano Development Kit  
2. Pairing a bluetooth headset (or equivalent)  
3. Installing python modules (with some proving more problematic than others, i.e. torch and ChatterBot)   
4. Obtraining training data, in our case, WhatsApp messages
5. Downloading/training/fine-tuning a custom language model  
6. Automating  

Please also note that the repository contains two main files demolition.py and demolition_jetson.py. The main difference between the two is that demolition.py implements Bark from [source](https://github.com/suno-ai/bark) and has been tested on MacOS whereas the demolition_jetson uses the implementation via [Huggingface](https://huggingface.co/docs/transformers/en/model_doc/bark). At the time of development we had troubles with Pytorch (torchaudio in particular) compatibility on Jetson Nano, and a different approach was implemented.


## Installation

1. Get the Jetson Orin running 

Follow this [guide](https://developer.nvidia.com/embedded/learn/get-started-jetson-orin-nano-devkit#prepare) depending on your developer kit module. If your kit is not from the official developer, follow their appropriate instructions. We used [Jetpack SDK 5.0.2](https://developer.nvidia.com/embedded/jetpack-sdk-502). 

2. Update the system and install Jetpack Components  

Open the terminal, then type:  
```sudo apt-get update```  
```sudo apt-get upgrade```  
```sudo apt-get install nvidia-jetpack```  

3.  Install git and clone the repository  
```sudo apt-get install git```  
```git clone https://github.com/modern-online/latent_intimacies.git```  
The repository should now be in your /home folder. Clean up all the things you don't need. Also note that /utils folder contains some simple scripts that we used for testing. 

4. Setting up a working directory and a [virtual environment](https://docs.python.org/3/library/venv.html). 

A virtual environment is like a contained folder that holds all the modules and items necessary for your code to run. The main advantage is that it keeps original Python folder intact, so if you mess something up, you can just delete the virtual environment and start again.

Inside the demolition folder, right-click then choose to open terminal. Type:  
```python -m venv demolenv```  
This creates a new virtual environment in a folder called demolenv. (If you get an error message saying no such command as venv exists, follow the suggested fix and install the venv module for Python).   
```source demolenv/bin/activate```  
activates the virtual environment.
You should now see _(demolenv)_ on the left of your command line. Please read the above documentation link to understand how virtual environments work. You are now ready to install the actual project. 

5. Installing Python modules

##### Another little disclaimer for those who know their way around: Typically, I would export a requirements file listing all the needed modules, but since we're building things on a Jetson, many standard versions would not work. Hence it's best to just install the latest Jetson-supported module version, depending on your OS.

Install a precompiled **torch** (or you can compile but it will take a few hours):  
Download a precompiled version [here](https://forums.developer.nvidia.com/t/pytorch-for-jetson/72048). At the time, we used PyTorch v2.1.0 for Jetpack 5.  
Put it in your the demolition folder.   
In terminal (assuming you're in the demolition folder, and that your virtual environment is active), type:  
```pip install [the name of the package you downloaded.whl]```  

Install audio drivers:  
```sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0```  
```sudo apt-get install ffmpeg libav-tools```  

Now install remaining modules:
``` pip install transformers scipy sounddevice soundfile vosk pyaudio sounddevice soundfile chatterbot```

6. Downloading speech-to-text machine learning model
Download a speech-to-text model of your choice (even small models work very well in English) from [here](https://alphacephei.com/vosk/models) and put it in the demolition folder. 

7. ChatterBot compatibility issues
There's one (or several depending on version) issues with the compatibility of ChatterBot (a relatively old Python module) and other ones that get constantly updated. If you encounter any issues we would suggest looking online as there is not one definitive solution. We encountered a yaml module incompatibility that is relatively easy to solve: 

Go to /demolenv/python/site-packages/chatterbot
Open corpus.py file with a text editor
replace _yaml.load()_ with _yaml.safe_load()_

[comment]: # For ChatterBot, the compatibility issue with yaml is clearly explained. However, you could potentially expand a bit more on why you chose that specific library over alternatives.


## Training ChatterBot with custom data

We trained ChatterBot on a selection of our personal WhatsApp messages, chosen for their intimate and personal nature. Have a look at this brief [tutorial](https://maazirfan.medium.com/building-a-chatbot-from-whatsapp-conversations-a-step-by-step-tutorial-48290cd458ef) on how to obtain data from WhatsApp and prepare it for training.

[comment]: # (After the steps on exporting WhatsApp data, note how a user could substitute data from a different messaging platform.)

Things to keep in mind:  
1. If you export data from different devices (i.e. exporting from iPhone and Android), the data cleaning might be slightly different.  
2. If you have messages in multiple languages, uniformising to a single language is necessary.  
3. For the demolition script to work, the clean version of the data in a LIST format, must be placed in a clean_data.txt file, in clean_data subfolder within your demolition directory, like this: /clean_data/clean_data.txt  
4. demolition_jetson.py uses a smaller random sample of the entire dataset (our WhatsApp data was quite large and therefore constant re-training becomes slow). If your data is relatively small, you can modify line 74 to increase sample_size.

You can use our little **scripts** for **translation** (/utils/translate.py ; you will need to additionally install [deep_translator](https://pypi.org/project/deep-translator/) module via pip) as well as **data cleaning** (/utils/clean_text_data.py) but some adjustments are likely to be required based on text formatting. 

Note: While we used WhatsApp data for the prototype, you can explore using other personal data sources, such as text messages, emails, or chat logs.


## Launching the script

Open terminal in the demolition folder, activate the virtual environment, then type:   
```python demolition_jetson.py```   
The first launch will take some time as transformers library will download the Bark model. 


## Automation 

#### Automating the launch of the script

Once all your scripts are running with success, you can automate the launch of _Demolition_, by adding the procedure to .bashrc (it's a system level script that executes when you open the terminal): 

Open terminal.  
```cd```  
to make sure we're in home directory  
```sudo nano .bashrc```   
to edit the file. Scroll to the bottom, and after the bluetooth config lines, add:  
```sleep 40```  (it will wait 40s before launching the script to make sure all other system processes kick in)  
```cd /home/[path to demolition folder] &&```  
```source demolenv/bin/activate &&```  
```python demolition_jetson.py```  
```ctrl+x``` to save then ```Y``` key to confirm.   

Now search for "startup applications" in your Ubuntu's search bar, and add terminal to it so it can launch on startup:  
Click _Add_  
In the _name_ field, type _Terminal_  
In the _command_ field, type _gnome-terminal_  
Click _Add_ 

This esentially allows the system to pretend to be you and execute the same sequence of actions that you would to run the script.  
```sudo reboot```
Then see if everything executes on its own!  

#### (Optional) Automating connection to Bluetooth headset

After a bit of wrangling, we managed to make Jetson Nano connect to Bluetooth headset with microphone automatically upon system start.  
The best way would be to start with this detailed [blog post](https://ansonvandoren.com/posts/pulseaudio-auto-bluetooth-hfp-profile/).  
The general concept is that you need to:  
1. Pair the headset (try looking at this [tutorial](https://forums.raspberrypi.com/viewtopic.php?t=235519)  
2. Make system audio drivers recognise it as an audio device  
3. Store the device profile in system configuration  
4. **IMPORTANT** Turn on the headset before turning on the Jetson (otherwise automatic pairing tends to fail)  
5. Add a line in the .bashrc file (it's a system file that executes things upon startup of the system), like this:  

cd  
(to make sure you're in your home folder)  
```sudo nano .bashrc```  
(to open the file with a command line text editor called Nano)  
Scroll to the very bottom, then add:  
```bluetoothctl connect YOURDEVICEID```  
(hopefully you've gotten the ID by following the tutorial).  
Then press CTRL+X to save the file, and the Y key to confirm.  
This will force-connect the speaker on startup, provided the speaker is on when RPi powers up.

DONE.