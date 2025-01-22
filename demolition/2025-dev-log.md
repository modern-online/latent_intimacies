<b>1 — CORE:</b>  
1.1 Flashed Jetpack 6.0 (Jetson Orin NX 16GB)  
Needed Ubuntu 22.04 computer, USB-C cable  
1.2 Updated the system (use apt — NOT apt-get — because Jetson only partially supported by OS)  
1.3 Installed Firefox (snap install firefox)  
1.4 Installed full package of Pipewire and wireplumber (audio servers to heal deal with I2S amp and mic)   
Used this guide : https://ubuntuhandbook.org/index.php/2022/04/pipewire-replace-pulseaudio-ubuntu-2204/   
Had to restart the system for Pipewire to take effect  
1.5 Installed VS code using this Github repo : https://github.com/JetsonHacksNano/installVSCode  

<b>2 — I2S MIC and I2S AMP setup</b> 

2.1 Wiring  
Adafruit SPH0645 Mic :  
PIN1 — 3V  
PIN9 — GND  
PIN38 — DOUT  
PIN35 — LRCL (shared with amp)  
PIN12 — BLCK (shared with amp)  

MAX98357A amp  
PIN2 — 5V  
PIN6 — GND  
PIN40 — DIN  
PIN35 — LRCL (shared with amp)
PIN12 — BLCK (shared with amp)

2.2 Configuring pins to enable I2S: 
sudo /opt/nvidia/jetson-io/jetson-io.py  
Configure manually to enable I2S  

<b>3 — Project files</b>

3.1. Copied  
demolition_jetson_v2.py  
clean_data.txt (dataset)  
vosk-model-small-en-us-0.15  
Pre-recorded "thinking" audio files  

3.2. Cleaned "thinking" directory's hidden files  
(otherwise unnecessary files break the code when monitoring folder)  

<b>4 — Python modules</b>  

4.1. Created virtual environment .venv  
4.2. Start with chatterbot as it's the oldest one (and tf contains older dependencies)  
Failed to build, pip install chatterbot==1.0.4 worked  
4.3 Installed wheel for building  
4.4 Torch :   
	4.4.1 Figure out Cuda version :  nvcc --version  
	Err: command not found  
	4.4.2 Add symlinks to .bashrc  
	export PATH=/usr/local/cuda/bin${PATH:+:${PATH}}$   
	export LD_LIBRARY_PATH=/usr/local/cuda/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}  
	4.4.3 Download a wheel for torch : Jetpack 6.0 + Ubuntu 22.04 + Cuda 12.2  
	https://forums.developer.nvidia.com/t/pytorch-for-jetson/72048   
	pip install [file].whl   
4.5 Pyaudio:  
  4.5.1 sudo apt install portaudio19-dev  
  4.5.2 pip install pyaudio  
4.6. Installed transformers (got dependency version mismatch but doesn't seem to affect the script)  
4.7. pip install accelerate (same dependency error)   
4.8. Installed the rest of the modules (launching the script and getting errors until everything needed was installed)  
4.9. installed punkt :  
  python   
  import nltk  
  nltk.download('punkt_tab')  
  exit()  
4.10. Numpy compilation conflict 1.x vs 2.x (from transformers) :  
   pip uninstall numpy  
   pip install numpy==1.26.4  
4.11. Bug with playing any audio from python. Ended removing sounddevice module.   
	User subprocess instead to play audio directly via alsa   

<b>5 — File order</b>  

5.1 Created appropriate folder structure based on error messages   

<b>6 – Autostart</b>  

6.1 Created autostart_demolition.sh  
6.2 Added silent audio to autostart to run in background (to prevent I2S from switching off and popping):  
aplay -D default -t raw -r 44100 -c 1 -f S16_LE /dev/zero & disown  


