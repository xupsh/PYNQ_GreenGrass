from pynq.overlays.base import BaseOverlay
#from pynq.lib.pmod import *
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from time import sleep
from datetime import date, datetime
import math
import socket

# initialize GPIO
base = BaseOverlay("base.bit")
import math
from pynq.lib.pmod import Grove_TMP
from pynq.lib.pmod import PMOD_GROVE_G4 # import constants

# Grove2pmod is connected to PMODB (2)
# Grove ADC is connected to G4 (pins [6,2])
tmp = Grove_TMP(base.PMODB, PMOD_GROVE_G4)
#btn = 'NULL'
def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip

local_ip = get_host_ip()
print (local_ip)
# AWS IoT certificate based connection
myMQTTClient = AWSIoTMQTTClient("pynq_controller")

#Here to put your own endpoint
myMQTTClient.configureEndpoint("xxxx.amazonaws.com", 443)

#Here to put your own files
myMQTTClient.configureCredentials("root-ca-cert.pem", "xxxx.private.key", "xxxx.cert.pem")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
 
#connect and publish
myMQTTClient.connect()
myMQTTClient.publish("hello/world/pubsub", "connected", 0)
 
#loop and publish sensor reading
while 1:
    now = datetime.utcnow()
    now_str = now.strftime('%Y-%m-%dT%H:%M:%SZ') #e.g. 2016-04-18T06:12:25.877Z
    '''
    btn = '0'
    if (base.buttons[0].read()==1):
        btn = '1'
        #sleep(0.3)
        
    elif (base.buttons[1].read()==1):
        btn = '2'
        #sleep(0.3)
            
    elif (base.buttons[2].read()==1):
        btn = '3'
        #sleep(0.3)

    elif (base.buttons[3].read()==1):
        btn = '4'
        #sleep(0.3)
    '''
    temperature = tmp.read()
    payload = float("{0:.2f}".format(temperature))
    print(payload,'degree Celsius')
    #payload = '{ "ip_source: "'+ local_ip +'","timestamp": "' + now_str + '","instruction": ' + btn + ' }'
    #payload = btn
    if btn != '0':
        myMQTTClient.publish("hello/world/pubsub", payload, 0)
    sleep(0.2)


