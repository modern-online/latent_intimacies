## About Red Book

Red Book is one of the three prototypes we built during a LAB#03: Synthetic Minds creative prototyping residency at Medialab Matadero in Madrid. Please refer to the main page of the repository for more information regarding the projet. Red Book is inspired by a mystical social game played by Mexican children. Blending chance, prophecy, and divination, playing the game requires a set of protocols for activation and engagement, while stressing the importance of disengagement. Leaving without permission may have undesirable consequences.

The Red Book is a curated language model, trained on texts (often books) contributed by its users. A group looking for answers designates a spokesperson to address the Book, much as one would a voice-activated digital assistant. Once activated, the speaker delivers prompts and questions, interpreting the needs and interests of others in the group. Some questions linger, unanswered. As the interaction draws to a close, the speaker seeks permission to leave.

## Hardware

Our device runs on a [Jetson Orin Nano Developer Kit with a 8GB VRAM module](https://developer.nvidia.com/embedded/learn/get-started-jetson-orin-nano-devkit), coupled with a plug-n-play [microphone and speaker bundle](https://www.waveshare.com/usb-to-audio.htm).

## Software

In general,the code was written in Python, and uses [Pytorch](https://pytorch.org/) and [Transformers](https://huggingface.co/docs/transformers/en/index) machine leaarning modules. Specifically, we use a custom-tuned smallest version of Eleuther's [GPT-NEO](https://huggingface.co/docs/transformers/en/model_doc/gpt_neo) for language generation as well as a smaller version of [Bark](https://huggingface.co/docs/transformers/en/model_doc/bark) by Suno AI.   

## A little disclaimer: 
This is a somewhat detailed tutorial as it is aimed at our principal audience, artists and designers fiddling with tech. It is an intermediate level project that requires some fundemantal understanding of computers as well as having dealt with creative coding in the past. For those who know their way around, the essentials are:

(1) Setting up a Jetson Orin Nano Development Kit  
(2) Adding speakers and microphone  
(3) Installing python modules (with some somewhat more problematic than others, i.e. torch)   
(4) Downloading/training/fine-tuning a custom language model  
(5) Automating  

Please also note that the repository contains two main files red_book and red_book_jetson. The main difference between the two is that red_book implements Bark from [source](https://github.com/suno-ai/bark) and has been tested on MacOS whereas the red_book_jetson uses the implementation via [Huggingface](https://huggingface.co/docs/transformers/en/model_doc/bark). At the time of development we had troubles with Pytorch (torchaudio in particular) compatibility on Jetson Nano, and a different approach was implemented.  

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

Inside the redbook folder, right-click then choose to open terminal. Type:  
```python -m venv redenvironment```  
This creates a new virtual environment in a folder called redenvironment. (In case you get an error message saying no such command as venv exists, follow what the error says to install the venv module for Python).   
```source redenvironment/bin/activate```  
activates the virtual environment.   
You should now see <em>(redenvironment)</em> on the left of your command line. Please read the above documentation link to understand how virtual environments work. You are now ready to install the actual project. 

**(5)** Installing Python modules

#### Another little disclaimer for those who know their way around: Typically, I would export a requirements file listing all the needed modules, but since we're building things on a Jetson, many standard versions would not work. Hence it's best to just install the latest Jetson-supported module version depending on your OS.

Install a precompiled **torch** (or you can compile but it will take a few hours):  
Download a precompiled version [here](https://forums.developer.nvidia.com/t/pytorch-for-jetson/72048). At the time, we used PyTorch v2.1.0 for Jetpack 5.  
Put it in your the red-book folder.   
In terminal (assuming you're in the redbook folder, and that your virtual environment is active), type:  
```pip install [the name of the package you downloaded.whl]```  

Install audio drivers:  
```sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0```  
```sudo apt-get install ffmpeg libav-tools```  

Now install remaining modules:
``` pip install transformers nltk scipy sounddevice soundfile vosk ```  

**(6)** Downloading machine learning models  

Download a speech-to-text model of your choice (even small models work very well in English) from [here](https://alphacephei.com/vosk/models) and put it in the red book folder. 
Download our custom fine-tuned GPT-Neo poetry model from [here](https://drive.google.com/file/d/1xbaOWP6rkfdtG4b-nqnbasEudCUlT1KE/view?usp=sharing) and put it in the red book folder.
Download nltk punkt. In terminal, type:  
```python```  
```import nltk```  
```nltk.download(punkt)```   
```exit()```  

## Launching the script

Open terminal in the red book folder, activate the virtual environment, then type:   
```python red_book_jetson.py```   
The first launch will take some time as transformers library will download the Bark model. 

## Automation 

Once all your scripts are running with success, you can automate the launch of Red Book, by adding the procedure to .bashrc (it's a system level script that executes when you open the terminal): 

Open terminal.  
```cd```  
to make sure we're in home directory  
```sudo nano .bashrc```   
to edit the file. Scroll to the bottom, and after the bluetooth config lines, add:  
```sleep 40```  (it will wait 40s before launching the script to make sure all other system processes kick in)  
```cd /home/[path to red_book folder] &&```  
```source redenvironment/bin/activate &&```  
```python red_book_jetson.py```  
```ctrl+x``` to save then ```Y``` key to confirm.   

Now search for "startup applications" in your Ubuntu's search bar, and add terminal to it so it can launch on startup:  
Click <em>Add</em>  
In the <em>name</em> field, type <em>Terminal</em>  
In the <em>command</em> field, type <em>gnome-terminal</em>  
Click <em>Add</em> 

This esentially allows the system to pretend to be you and execute the same sequence of actions that you would to run the script.  
```sudo reboot```
Then see if everything executes on its own!  

DONE.



