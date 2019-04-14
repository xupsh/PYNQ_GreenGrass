from pynq.overlays.base import BaseOverlay
from pynq.lib.pmod import *
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from time import sleep
from datetime import date, datetime
import math
import socket

# initialize GPIO
base = BaseOverlay("base.bit")
btn = 'NULL'
def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip

local_ip = get_host_ip()
# AWS IoT certificate based connection
myMQTTClient = AWSIoTMQTTClient("pynq_controller")

#Here to put your own endpoint
myMQTTClient.configureEndpoint("xxxxx.iot.us-east-1.amazonaws.com", 443)

#Here to put your own files
myMQTTClient.configureCredentials("VeriSign-Class3-Public-Primary-Certification-Authority-G5.pem", "xxxxxxxxxx.private.key", "xxxxxxxxx.cert.pem")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
 
#connect and publish
myMQTTClient.connect()
myMQTTClient.publish("pynq_test/button", "connected", 0)
 
#loop and publish sensor reading
while 1:
    now = datetime.utcnow()
    now_str = now.strftime('%Y-%m-%dT%H:%M:%SZ') #e.g. 2016-04-18T06:12:25.877Z
    
    btn = '0'
    if (base.buttons[0].read()==1):
        btn = '1'
        sleep(0.5)
        
    elif (base.buttons[1].read()==1):
        btn = '2'
        sleep(0.5)
            
    elif (base.buttons[2].read()==1):
        btn = '3'
        sleep(0.5)

    elif (base.buttons[3].read()==1):
        btn = '4'
        sleep(0.5)

    #payload = '{ "ip_source: "'+ local_ip +'","timestamp": "' + now_str + '","instruction": ' + btn + ' }'
    payload = btn
    print (payload)
    myMQTTClient.publish("pynq_test/button", payload, 0)
    sleep(0.5)

