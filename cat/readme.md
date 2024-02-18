## About Cats

Cats is one of the three prototypes we built during a LAB#03: Synthetic Minds creative prototyping residency at Medialab Matadero in Madrid. Please refer to the main page of the repository for more information regarding the projet. 

Essentially, cats is a wearable virtual companion. It uses computer vision to take photos, then describes those photos through image captioning using text-to-speech. It runs on a battery, operates offline, and due to its tiny architecture, takes long time to load and compute. Cats takes around 60 minutes to boot, then captures a photo, which takes another 45 minutes to process. Subsequently, you have a new photo description every 45 minutes, spoken aloud. The user has no control over the device, except from turning it on and off, and taking it places.

Cats stores things it sees in a text file. Every time you turn it on, it will describe everything it has seen so far. Images are not stored. 

## Hardware

Our device runs on a [Raspberry Pi Zero 2W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/), coupled with a compatible [battery pack](https://www.pisugar.com/), compatible camera like [this one](https://www.adafruit.com/product/3508) (there are many camera options online just make sure you get one with the right ribbon cable as the one for Pi Zero is smaller that the regular Raspberry Pi). Finally, we used a 5eur. bluetooth speaker but we tested Bluetooth headphones as well and got them working with a bit of a grind. If you play your cards right, the device can be built for 50-60eur. 

## Software

In the future, if there's demand, we could package the operating system with the code as a virtual image file, which can be easily flashed into an SD card and then plugged into a Pi Zero. 

In general,the code was written in Python, and uses Open CV (CV2) computer vision library, [Smallcap](https://github.com/RitaRamo/smallcap) Image Captioning model by Rita Ramos (please follow the instructions on their GitHub page as we used their pre-trained model, and to run that you need things like COCO index and captions, also listed in the link), you, and simple old-school text-to-speeh using espeak library. 





