# RPI-MQTT-shutdown
This script will reboot or shutdown the host on demand via MQTT message. 
It will also send the host connection status ("Online" or "Offline") to the broker.

Installation:

`sudo apt-get install python-pip`

Install Paho

Get the files:

`cd /usr/local/bin`
`sudo git clone https://github.com/olkal/RPI-MQTT-shutdown.git`

Edit MQTT url, port, user, passwrd and topics:

`sudo nano /usr/local/bin/RPI-MQTT-shutdown/mqtt_shutdown.py`

Run/test the script: 

`cd /usr/local/bin/RPI-MQTT-shutdown
sudo python /usr/local/bin/RPI-MQTT-shutdown/mqtt_shutdown.py`

******************************
Autostart the script:

`cd /usr/local/bin/RPI-MQTT-shutdown
sudo mv mqtt_shutdown.service /etc/systemd/system/
sudo systemctl enable mqtt_shutdown.service`

Run service (will be automatically started on next reboot):

`sudo systemctl start mqtt_shutdown.service`
