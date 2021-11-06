# waveshare-scripts
Modified scripts for Raspberry PI Waveshare hw extensions

## Fan_HAT Script usage

### Install python and dependencies
    sudo apt-get update
    sudo apt-get install python3-pip
    sudo pip3 install RPi.GPIO
    sudo pip3 install smbus

### Run script manual
    git clone https://github.com/ChuckNorrison/waveshare-scripts
    cd Fan_HAT/python/
    sudo python3 main.py

### Run script as service
copy the service file example to /etc/systemd/system/ and tweak the script path

    sudo systemctl start FAN-HAT
    sudo systemctl enable FAN-HAT

### check logs
    sudo journalctl -fu FAN-HAT
