
#!/usr/bin/env python
import paho.mqtt.client as mqtt
import time
from subprocess import call

# Use MQTT for remote reboot and shutdown
# copy this file to /usr/local/bin (if other path is used, then also change the service script file)

# "on connect" event
def connectFunction (client, userdata, flags, rc):
  if rc==0:
    print("connected OK Returned code=",rc)
    MyClient.publish("stat/RPI_test", "online") # Publish message to MQTT broker
  else:
    print("Bad connection Returned code=",rc)

# "on message" event
def messageFunction (client, userdata, message):
  topic = str(message.topic)
  payload = str(message.payload.decode("utf-8"))
  print("New message received:", topic+" "+payload)
  if topic=="cmnd/RPI_test":
    handleCmnd(payload)

# handle new MQTT command function
def handleCmnd (cmnd):
  if cmnd=="reboot":
    call(['shutdown', '-r', 'now'], shell=False) #reboot host
  elif cmnd=="shutdown":
    call(['shutdown', '-h', 'now'], shell=False) #shut down host
  elif cmnd=="test":
    print("'test' received")

MyClient = mqtt.Client() # Create a MQTT client object
#MyClient.username_pw_set("my_mqtt_user", "my_mqtt_password")
MyClient.on_connect = connectFunction # run function on connect with broker
MyClient.will_set("stat/RPI_test", "Offline", 0, True)
MyClient.connect("192.168.1.4", 1883) # Connect to the test MQTT broker
MyClient.subscribe("cmnd/RPI_test") # Subscribe to a topic
MyClient.on_message = messageFunction # Attach the messageFunction to subscription
MyClient.loop_start() # Start the MQTT client


while(1):
  MyClient.publish("stat/RPI_test", "online") # Publish message to MQTT broker
  time.sleep(60) # Sleep for a while
