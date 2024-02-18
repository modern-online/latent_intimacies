## About Cats

Cats is one of the three prototypes we built during a LAB#03: Synthetic Minds creative prototyping residency at Medialab Matadero in Madrid. Please refer to the main page of the repository for more information regarding the projet. 

Essentially, cats is a wearable virtual companion. It uses computer vision to take photos, then describes those photos through image captioning using text-to-speech. It runs on a battery, operates offline, and due to its tiny architecture, takes long time to load and compute. Cats takes around 60 minutes to boot, then captures a photo, which takes another 45 minutes to process. Subsequently, you have a new photo description every 45 minutes, spoken aloud. The user has no control over the device, except from turning it on and off, and taking it places.

Cats stores things it sees in a text file. Every time you turn it on, it will describe everything it has seen so far. Images are not stored. 

## Hardware

Our device runs on a [Raspberry Pi Zero 2W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/), coupled with a compatible [battery pack](https://www.pisugar.com/), compatible camera like [this one](https://www.adafruit.com/product/3508) (there are many camera options online just make sure you get one with the right ribbon cable as the one for Pi Zero is smaller that the regular Raspberry Pi). Finally, we used a 5eur. bluetooth speaker but we tested Bluetooth headphones as well and got them working with a bit of a grind. If you play your cards right, the device can be built for 50-60eur. 

## Software

In the future, if there's demand, we could package the operating system with the code as a virtual image file, which can be easily flashed into an SD card and then plugged into a Pi Zero. 

In general,the code was written in Python, and uses [Open CV (CV2)](https://opencv.org/) computer vision module, [Smallcap](https://github.com/RitaRamo/smallcap) Image Captioning model by Rita Ramos (please follow the instructions on their GitHub page as we used their pre-trained model, and to run that you need things like COCO index and captions, also listed in the link), you, and simple old-school text-to-speeh using [espeak](https://espeak.sourceforge.net/). To run the image-captioning model, you would also need [Pytorch](https://pytorch.org/) and [Transformers](https://huggingface.co/docs/transformers/en/index) machine leaarning modules. 

## Installation

Please note that the code itself is not very complicated, but to get it to run on this particular architecture is a bit of a hassle. 

### Getting your RPi Ready (somewhat easy) 

(1) To get your Rpi Zero up and running, follow this (or similar) [tutorial](https://howtohifi.com/beginners-guide-to-raspberry-pi-os-installation/). IMPORTANT: The project was built in February, 2024, and the latest OS by RPi was not yet compatible with Pytorch, therefore we used RASPBIAN BULLSEYE LITE, the headless earlier version of the OS. 

(2) Once you have your OS running, you can either plug your PI into a screen with a keyboard and mouse (a bit of a mess of USB and HDMI adapters for Pi Zero) or (SSH)[https://www.onlogic.com/company/io-hub/how-to-ssh-into-raspberry-pi/] login into it remotely from your computer, provided you're on the same WiFi network. 

(3) A couple of system configurations needed:  
Expanding filesystem memory. When you install a Pi OS, it only takes the part of the SD card that is needed to run the system itself. You then need to explicitly grant the computer access to the remaining SD card space. 

In the terminal, type:
```sudo raspi-config --expand-rootfs```
follow any on-screen instructions. Once done, reboot either through the interactive menu, or by typing
```sudo reboot```








