camera app for the zero boot system

An able the camera vi "sudo raspi-config"

To make the app auto start on boot up you need to add below
@python /home/pi/zero_boot_system_apps/camera/camera_app/camera.py
to the file below
/etc/xdg/lxsession/LXDE-pi/autostart
