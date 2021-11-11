# waveshare-scripts
Modified scripts for Raspberry PI Waveshare hw extensions

## Fan_HAT Script usage
![image](https://user-images.githubusercontent.com/2964146/140618419-931f8ccb-7e41-4b3f-b751-ccc35d79a9b0.png)

### Install python and dependencies
    sudo apt-get update
    sudo apt-get install python3-pip
    sudo pip3 install RPi.GPIO
    sudo pip3 install smbus

## Enable i2C Interface
    sudo raspi-config
     
Choose Interfacing Options -> I2C ->yes 

### Run script manual
    git clone https://github.com/ChuckNorrison/waveshare-scripts
    sudo chmod -R +x Fan_HAT/python/
    cd Fan_HAT/python/
    sudo python3 main.py

### Run script as service
copy the service file example to /etc/systemd/system/ and tweak the script path

    sudo systemctl start FAN-HAT
    sudo systemctl enable FAN-HAT

### check logs
    sudo journalctl -fu FAN-HAT
![image](https://user-images.githubusercontent.com/2964146/140618788-48d63065-90c5-4c77-a19d-d5100e4ae93d.png)

### links
https://www.waveshare.com/fan-hat.htm
