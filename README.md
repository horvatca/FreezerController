# FreezerController
Python to control the temperature of a freezer via power relay on raspberry pi


To set up the Raspberry Pi
Assumes you have root/sudo access, and ssh enabled, and a network connection.

Set the host name:
Either via Raspbian interface or by editing
````terminal
sudo nano /etc/hostname
-just add the name
sudo nano /etc/hosts
-change the entry on the 127.0.1.1 lint
````

Install git:
````terminal
sudo apt install git
````

install GPIo pins:
````terminal
sudo apt-get install rpi.gpio
````

verify GPIO pins:
````terminal
pinout
````

Enable the one wire interface for the temp sensor on GPIO physical pin 11 in the boot config by adding the following to the /boot/config.txt:
````terminal
sudo nano /boot/config.txt
#enable overlay for single wire temp sensor
dtoverlay=w1-gpio,gpiopin=17
````

clone the git repo into your home directory
````terminal
cd~
git clone https://github.com/horvatca/FreezerController.git
````

Make the script executable. Execute this command in the folder the script is in, hopefully /home/pi/FreezerController
````console
chmod +x /home/pi/FreezerController/freezermonitor.py
````

Make a cron job to execute the script every minute:
Access cron schedule with this command:
````console
crontab -e
````
Add this line to the cron schedule:
````console
* * * * * /home/pi/FreezerController/freezermonitor.py
````
Check to make sure it took with:
crontab - l




to push updates you make toyour repo
git add .
git commit -m 'your message'
git push



