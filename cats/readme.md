## _Cats_

_Cats_ is one of three prototypes we built during the LAB#03: Synthetic Minds creative prototyping residency at Medialab Matadero in Madrid. This wearable device intertwines the daily lives of cats, their caretakers, and the community. A tiny AI narrator, _Cats_ offers a unique perspective on the world. Translating snapshots from a cat-worn camera into basic spoken texts, the AI emulates a cat. It sticks around, but sets its own pace, providing pleasure, ungoverned, on its own terms.


## Contents

- [Overview](#overview)
- [Hardware](#hardware)
- [Software](#software)
- [Small disclaimer](#small-disclaimer)
- [Installation](#installation)
- [Testing](#testing)
- [Automation](#automation)


## Overview

![cats](https://github.com/modern-online/latent_intimacies/blob/main/images/cats_live.jpg)

Essentially, _Cats_ is a wearable virtual companion. It uses computer vision to take photos, then describes those photos through image captioning using text-to-speech. It runs off a battery, operates offline, and due to its tiny architecture, runs extremely slowly. _Cats_ takes roughly an hour to boot, then captures a photo, which takes another 45 minutes to process. Subsequently, you have a new photo description every 45 minutes, spoken aloud. The user has no control over the device, except from turning it on and off, and taking it places.

_Cats_ stores what it sees in a text file. Every time you turn it on, it will describe everything it has seen so far. Images are not stored.


## Hardware

Our device runs on a [Raspberry Pi Zero 2W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/), chosen for its compact size and low power consumption, coupled with a compatible [battery pack](https://www.pisugar.com/), and compatible camera like [this one](https://www.adafruit.com/product/3508). There are many camera options online, but make sure you get one with the right ribbon cable, as the one for Pi Zero is smaller than for the regular Raspberry Pi. Finally, we used a €5 bluetooth speaker but we tested Bluetooth headphones as well and got them working with a bit of a grind. If you play your cards right, the device can be built for €50-60. For assembly, each of these items have their respective tutorials and documentation. You might need a soldering iron to solder the header pins onto the Raspberry Pi for the battery to work.


## Software

In the future, we could package the OS image and code for easier setup. We could package the operating system with the code as a virtual image file, which can be easily flashed into an SD card and then plugged into a Pi Zero. 

The code was written in Python, and uses the [Open CV (CV2)](https://opencv.org/) computer vision module for tasks like image capture and processing. We use Rita Ramos' [Smallcap](https://github.com/RitaRamo/smallcap) image captioning model, which generates descriptive text from images. Please follow the instructions on their GitHub page as we used their pre-trained model, and to run that you need things like COCO index and captions, also listed in the link. For text-to-speech, we used and simple, old-school [espeak](https://espeak.sourceforge.net/). To run the image-captioning model, you would also need [Pytorch](https://pytorch.org/) and [Transformers](https://huggingface.co/docs/transformers/en/index) machine learning modules. 

[comment]: # For OpenCV, you could explain what its core functionality is (e.g. computer vision tasks like object detection).

## Small disclaimer:

This is a fairly detailed tutorial aimed at our principal audience, artists and designers fiddling with tech. It is an intermediate-level project that requires a fundamental understanding of computers, and some prior experience of creative coding. For those who know their way around, the essentials are:

1. Setting up a RPI with the required components  
2. Installing the right OS  
3. Pairing a bluetooth speaker/headphones  
4. Installing python modules (with some somewhat more problematic than others, i.e. torch)  
5. Downloading required models and captions (notably [Smallcap](https://github.com/RitaRamo/smallcap) related stuff)  
6. Automating 


## Installation

Please note that the code itself is not very complicated, but to get it to run on this particular architecture is a bit of a hassle. 

#### Preparing the RPi (relatively easy) 

1. To get your Rpi Zero up and running, follow this (or similar) [tutorial](https://howtohifi.com/beginners-guide-to-raspberry-pi-os-installation/). IMPORTANT: The project was built in February 2024, and the latest OS by RPi was not yet compatible with Pytorch, therefore we used RASPBIAN BULLSEYE LITE, the headless earlier version of the OS. Make sure to configure the network connection as you'll need it for the installation. 

2. Once you have your OS running, you can either plug your PI into a screen with a keyboard and mouse (a bit of a mess of USB and HDMI adapters for Pi Zero) or [SSH](https://www.onlogic.com/company/io-hub/how-to-ssh-into-raspberry-pi/) login into it remotely from your computer, provided you're on the same WiFi network. 

3. A couple of system configurations needed:  

**Expanding filesystem memory.** When you install a Pi OS, it only takes the part of the SD card that is needed to run the system itself. You then need to explicitly grant the computer access to the remaining SD card space. 

In the terminal, type:  
```sudo raspi-config --expand-rootfs```  
and follow any on-screen instructions. Once done, reboot either through the interactive menu, or by typing   
```sudo reboot```  

**Updating the system.** After the reboot, do a general system update, typing, one after another:  
```sudo apt-get update```  
```sudo apt-get upgrade``` 

**Expanding swap memory** The tiny Raspberry Pi Zero only has 512mb of RAM. Compared to your computer that probably has 8-16gb at least, it's really nothing. A typical machine learning model loads itself into the RAM (or VRAM if you have a discrete graphics processor) from where it operates. 512mb is way too low for a machine learning model (depending on the model, you'd need at least 4-8gb). Fortunately, the concept of swap memory allows your computer to use your hard memory (in this case, SD card) if it runs out of RAM. The tradeoff is that SD card is much slower that the on-board RAM. Hence the **principal latency in _Cats_**.

Follow this [tutorial](https://pimylifeup.com/raspberry-pi-swap-file/) to increase swap. We had a big SD so went all out by increasing to 16GB (16000 mb), but probably 4-8gb would work, too. Protip: A good SD card can make a huge difference as increasing reading/writing speed has direct impact on the process. The most expensive is not always the best; here's a good [guide](https://www.tomshardware.com/best-picks/raspberry-pi-microsd-cards) on SD cards that work well on RPis.

4. Connecting a Blueetooth device (speaker or headphones). This one is a bit of a pain. This expansive albeit somewhat messy [tutorial](https://forums.raspberrypi.com/viewtopic.php?t=235519) will probably do the trick. Just read carefully and don't blindly copy-paste stuff because not all of the tutorial is relevant (i.e. the part with the USB dongle). A couple of tips:

- Always turn the bluetooth device on before turning on the PI, to make sure they connect. 
- Even after following tutorials, the PI would fail to automatically connect to our €5 speaker. What did the trick was to trust, pair the device (as explained in the tutorial), then add a line in the .bashrc file (it's a system file that executes things upon startup of the system), like this:

```cd```  
(to make sure you're in your home folder)    
```sudo nano .bashrc```  
(to open the file with a command line text editor called Nano)  
Scroll to the very bottom, then add:  
```bluetoothctl connect YOURDEVICEID```  
(hopefully you've gotten the ID by following the tutorial).  
Then press CTRL+X to save the file, and the Y key to confirm.  
This will force-connect the speaker on startup, provided the speaker is on when RPi powers up. 


#### Setting up Python 

Good news is that Python is already installed on RPi OS, so we can skip to the installation of the actual project files. 

5. Cloning this Github repository with project files and cleaning things up a bit. 

```cd```  
to make sure you're in home directory  
```sudo apt-get install git```  
to install git  
```git clone https://github.com/modern-online/latent_intimacies.git```  
to download the directory of this project   
```cd latent intimacies```  
to enter the folder  
```sudo rm -r demolition```  
```sudo rm -r red_book```  
to delete files related to other projects. 


6. Setting up a working directory and a [virtual environment](https://docs.python.org/3/library/venv.html). 
A virtual environment is like a contained folder that holds all the modules and items necessary for your code to run. The main advantage is that it keeps original Python folder intact, so if you mess something up, you can just delete the virtual environment and start again.

```cd cats ```  
enter cats folder    
```python -m venv catsenvironment```  
creates a new virtual environment in a folder called catsenvironment. (In case you get an error message saying no such command as venv exists, follow what the error says to install the venv module for Python).   
```source catsenvironment/bin/activate```  
activates the virtual environment.   
You should now see _(catsenvironment)_ on the left of your command line. Please read the above documentation link to understand how virtual environments work. You are now ready to install the actual project. 

7. Installing Python modules needed for the code to run.  

##### Another little disclaimer for those who know their way around: Typically, I would export a requirements file listing all the needed modules, but since we're building things on a PI, most of the latest/standard versions would not work. Hence it's best to just figure out the latest Pi-supported module version, depending on your OS.

Install **OpenCV** (to be able to capture images with the camera):  
```sudo apt install python3-opencv```  
Install **torch**, a grand module for machine learning. It's a bit hefty and it requires some special configurations for RPi, hence the best strategy is to install using wheel. Follow this [tutorial](https://qengineering.eu/install-pytorch-on-raspberry-pi-4.html). It's for a RPi4 but works for Zero as well provided you use BULLSEYE OS. Just scroll down to the yellow table and copy the code.  

**If you've made it this far, the worst is behind you.**

Install remaining modules using [pip](https://pypi.org/project/pip/). Pip is a python package manager that comes pre-installed with your Python, basically software that installs other software.  
``` pip install wheel```  
don't worry much about what this one does, it just makes some further installations a bit faster  
```pip install transformers```  
this one is a module on top of torch to do all kinds of machine learning  
```pip install pyttsx3```  
this one is a small text-to-speak module  
```sudo apt-get install -y libespeak-dev```   
this installs the necessary engine for text-to-speech to work 

**Make sure to download all the files needed for [Smallcap](https://github.com/RitaRamo/smallcap) to run, following the instuctions on their github.**

The "datastore" directory should be created in the cats directory:  
```mkdir datastore```  
```cd datastore```  
to download them via the command line, you can use wget:  
```sudo apt-get install wget```  
then:  
```wget LINK_FROM_SMALLCAP_INSTRUCTIONS```   
to download the files. 

**Create a data folder**
Go back to cats directory  
``cd ..``  
to go one folder back  
``makedir data``  
to create a data directory where the text file and the latest image will be store


## Testing

Make sure the virtual environment is activated.  
``` python camera_test.py ```  
tests your opencv library and if you didn't get any errors, a photo should stored in the /data folder.  
``` python tts_test.py ```  
tests your text to speech and lists all available voice ids. You can then modify the cats.py code with the voice ID you like.  
``` python cats.py ```  
launches the main script. It takes ages.


## Automation

Once all your scripts are running with success, you can automate the launch of _Cats_, by adding the procedure to .bashrc, just like we did with the bluetooth speaker setup:

```cd```  
to make sure we're in home directory  
```sudo nano .bashrc```  
to edit the file. Scroll to the bottom, and after the bluetooth config lines, add:  
```sleep 40``` 
it will wait 40s before launching the script to make sure all other system processes kick in.  
```cd /home/YOURUSERNAME/latent_intimacies/cats &&``` (replace this with your actual user name) 
```source catsenvironment/bin/activate &&```  
```python cats.py```  
This esentially allows the system to pretend to be you and execute the same sequence of actions that you would to run the script.  
```sudo reboot```  
Then see if everything executes on its own!  

DONE. 






