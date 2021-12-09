# Personal_Greenhouse
## About
An automated system to create an environment for plant growth based on desired specifications (humidity and temperature). This will not only provide a user-friendly and easy way for anyone to grow plants (such as in their own homes), but will also help to decrease carbon dioxide levels as more plants are grown in the environment. This personal greenhouse will be able to sense, save and show data in CSV files regarding the humidity of soil, humidity of air, temperature,  and percentage of plant growth. In addition, it will periodically monitor and notify the user of the greenhouse conditions in order to provide the plant with an optimal environment to survive in.

## Hardware

- Rapberry Pi
- Adafruit STEMMA Soil Sensor
- DHT11 Temperature/Humidity Sensor
- Raspberry Pi Camera Module V2
- ELEGOO 4 Channel DC 5V Relay Module
- 12 V Water Pump
- Heat Lamp
- TP-Link Kasa Smartplug
- LCD Display
- Humidifier

## Other Materials

- Plant environment (plastic tank)
- Tubing for water pump

## Required Libraries and API keys

Since this project utilizes python make sure to run the following commands:
Make sure to install npm and node.js

` sudo apt-get update ` </br>
` apt-get upgrade ` </br>
` pip3 install pandas numpy PIL adafruit-circuitpython-seesaw Adafruit-DHT RPi.GPIO twilio tplink-cloud-api `</br>
` npm install twilio-cli -g `</br>
` sudo apt-get install libsecret-1-dev`</br>

Sign up for a Twilio account (get a phone number and API keys)
Setup smart plugs with internet network and name them "Smart Heater" and "Smart Humidifier" and plug in those actuators accordingly.
Make sure RPi has I2C communication enabled.

## Software Setup
In toggle_smartplug.py add your Kasa username and password for the smart plugs.
In parse_send_data.py add your TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN and the source and destination phone with the area code (e.g. +143248412)

## Hardware setup
Make sure both soil sensors have different addresses (0x36 and 0x37).
Setup LCD display as shown in: https://www.mbtechworks.com/projects/drive-an-lcd-16x2-display-with-raspberry-pi.html
Setup DHT sensors one in GPIO16 and the other in GPIO20
Setup Soil humidity sensors on GPIO3 (SDA) and GPIO4 (SCL)
Setup in for relay module at GPIO21
Connect camera and point at plant

<p align="center" width="100%">
    <img max_width="100%" src="imgfolder/image1.png">
</p>

## Video
<p align="center" width="100%">
<video src='imgfolder/video1.mp4' width=480/>
</p>
