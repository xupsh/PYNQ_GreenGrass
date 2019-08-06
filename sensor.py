from pynq.overlays.base import BaseOverlay
from pynq.lib.pmod import *
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from time import sleep
from datetime import date, datetime
import math
import socket
from pynq.lib.arduino import Grove_LEDbar
from pynq.lib import MicroblazeLibrary
import numpy as np
#import lps25h
#import hts221
#import adafruit_lsm9ds1
# initialize GPIO
base = BaseOverlay("base.bit")

#ledbar = Grove_LEDbar(base.ARDUINO,ARDUINO_GROVE_G4)
#ledbar.reset()
i = 1

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip

def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

    #button message:1/2/3/4
    global btn, i
    try:
        btn = int(message.payload)
    except Exception as e:
    	print(e)
    #btn1 increase, btn2 decrease
    if (btn == 1):
        #sleep(0.2)
        #ledbar.write_level(i,2,1)
        print("btn == 1\n")
        i = min(i+1,9)
    elif (btn == 2):
        #sleep(0.2)
        i = max(i-1,0)
        print("btn == 2\n")
        #ledbar.write_level(i,2,1)
    elif (btn == 3):
        print("btn == 3\n")
        #ledbar.reset()
    base.leds[btn-1].on()
    sleep(0.2)
    base.leds[btn-1].off()

# Loading Base Overlay
#base.select_rpi()
#lib = MicroblazeLibrary(base.RPI, ['i2c','xio_switch','circular_buffer'])

pynq_self = "pynq_sensor"
local_ip = get_host_ip()
# AWS IoT certificate based connection
myMQTTClient = AWSIoTMQTTClient("pynq_greengrass_sensor")

#Here to put your own endpoint
myMQTTClient.configureEndpoint("xxxx.com", 443)

#Here to put your own files
myMQTTClient.configureCredentials("root-ca-cert.pem", "xxxx.private.key", "xxxx.cert.pem")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
 
#connect and publish
myMQTTClient.connect()
 
#loop and publish sensor reading
while 1:
        #get button instruction
    try:
        myMQTTClient.subscribe("hello/world/pubsub", 1,customCallback)
    except Exception as e:
        print(e)
            #pass
    print("loop\n")
    sleep(0.2)


