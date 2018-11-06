First you will need to install the library for the ADS1115 from here
https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code

To make the app auto start on boot up you need to add below
@python /home/pi/pialyzer/pialyzer.py
to the file below
~/.config/lxsession/LXDE-pi/autostart
