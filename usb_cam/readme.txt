First you will need to install the library for the ADS1115 from here
https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code

To make the app auto start on boot up you need to add below
@python /home/pi/zero_boot_system_apps/usb_cam/usb_cam.py
to the file below
/etc/xdg/lxsession/LXDE-pi/autostart
