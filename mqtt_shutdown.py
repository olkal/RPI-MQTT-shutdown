#!/usr/bin/env python
import paho.mqtt.client as mqtt
import time
from subprocess import call

#configuration:
brokerAdr = "192.168.1.199"
brokerPort = 1883 
brokerUserName = "myMqttUser"
brokerPassword = "myMqttpassword"
teleTopic = "tele/myRPI/ncs"
cmndTopic = "cmnd/myRpi"

# "on connect" event
def connectFunction (client, userdata, flags, rc):
  if rc==0:
    print("connected OK Returned code=",rc)
    MyClient.publish(teleTopic, "Online", 1, True) # Publish message to MQTT broker
    MyClient.subscribe(cmndTopic) # Subscribe after re-connect
  else:
    print("Bad connection Returned code=",rc)

# "on message" event
def messageFunction (client, userdata, message):
  topic = str(message.topic)
  payload = str(message.payload.decode("utf-8"))
  print("New message received:", topic+" "+payload)
  if topic==cmndTopic:
    handleCmnd(payload)

# handle new MQTT command function
def handleCmnd (cmnd):
  if cmnd=="reboot":
    call(['shutdown', '-r', 'now'], shell=False) #reboot host
  elif cmnd=="shutdown":
    call(['shutdown', '-h', 'now'], shell=False) #shut down host
  elif cmnd=="test":
    MyClient.publish(teleTopic, "Reply to test msg") # Publish reply to an incomming msg with payload "test"

while (1):
  MyClient = mqtt.Client() # Create a MQTT client object
  MyClient.username_pw_set(brokerUserName, brokerPassword)
  MyClient.on_connect = connectFunction # run function on connect with broker
  MyClient.will_set(teleTopic, "Offline", 1, True)
  MyClient.connect(brokerAdr, brokerPort) # Connect to the test MQTT broker
  MyClient.on_message = messageFunction # Attach the messageFunction to subscription
  MyClient.loop_forever()    

