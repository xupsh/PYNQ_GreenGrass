from pynq.overlays.base import BaseOverlay
from pynq.lib.pmod import *
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from time import sleep
from datetime import date, datetime
import math
import socket

# Sense Hat Library

from pynq.lib import MicroblazeLibrary
import numpy as np
import lps25h
import hts221
import adafruit_lsm9ds1
from pynq.lib.arduino import Grove_LEDbar

# Sense Hat Library

# initialize GPIO
base = BaseOverlay("base.bit")

ledbar = Grove_LEDbar(base.ARDUINO,ARDUINO_GROVE_G4)
ledbar.reset()
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
        sleep(0.2)
        ledbar.write_level(i,2,1)
        i = min(i+1,9)
    elif (btn == 2):
        sleep(0.2)
        i = max(i-1,0)
        ledbar.write_level(i,2,1)
    elif (btn == 3):
        ledbar.reset()

# Sense Hat Custom Function
def level_meter(accel_x, accel_y, buf, center_data):
    buf[0] = 0
    red_color = 0
    green_color = 0
    blue_color = 50
    x_value = int(accel_x * 1.5)
    y_value = int(accel_y * 1.5)
    x_value = 3 if x_value < -3 else 5 if x_value > 3 else abs(x_value) if x_value < 0 else 8 - x_value
    y_value = 3 if y_value < -3 else 5 if y_value > 3 else abs(y_value) if y_value < 0 else 8 - y_value
    frame_buffer = np.hstack((center_data[:,x_value:8],center_data[:,0:x_value]))
    frame_buffer = np.vstack((frame_buffer[y_value:8],frame_buffer[0:y_value]))
    frame_buffer = np.rot90(frame_buffer, 2)
    for y in range(0,8) :
        for x in range(0,8) :
            buf[1+x+8*0+3*8*y] = red_color
            buf[1+x+8*1+3*8*y] = green_color
            buf[1+x+8*2+3*8*y] = frame_buffer[y][x]*blue_color

# Loading Base Overlay
base.select_rpi()
lib = MicroblazeLibrary(base.RPI, ['i2c','xio_switch','circular_buffer'])

# Openning I2C Library
i2c = lib.i2c_open_device(1)
lib.set_pin(2, lib.SDA1)
lib.set_pin(3, lib.SCL1)

# Initializing Sensor
sensor_hts221 = hts221.HTS221_I2C(i2c)
sensor_lps25h = lps25h.LPS25H_I2C(i2c)
sensor_lsm9ds1 = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)

cnt = 0
buf = bytearray(193)
center_data = np.array(
    [
   #[1, 2, 3, 4, 5, 6, 7, 8],
    [0, 0, 0, 0, 0, 0, 0, 0],# 1
    [0, 0, 0, 0, 0, 0, 0, 0],# 2
    [0, 0, 0, 0, 0, 0, 0, 0],# 3
    [0, 0, 0, 1, 1, 0, 0, 0],# 4
    [0, 0, 0, 1, 1, 0, 0, 0],# 5
    [0, 0, 0, 0, 0, 0, 0, 0],# 6
    [0, 0, 0, 0, 0, 0, 0, 0],# 7
    [0, 0, 0, 0, 0, 0, 0, 0] # 8
    ]
)
# Initializing Sensor

pynq_self = "pynq_sensor"
local_ip = get_host_ip()
# AWS IoT certificate based connection
myMQTTClient = AWSIoTMQTTClient("pynq_greengrass_sensor")

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
myMQTTClient.publish("pynq_test/sensor", "connected", 0)
 
#loop and publish sensor reading
while 1:
    if(cnt == 50):
        now = datetime.utcnow()
        now_str = now.strftime('%Y-%m-%dT%H:%M:%SZ') #e.g. 2016-04-18T06:12:25.877Z

        temp = sensor_lps25h.temperature
        press = sensor_lps25h.pressure
        humi = sensor_hts221.humidity
        cnt = 0

        sense_hat_payload = '{ "self": ' + pynq_self +'","ip_source": ' + local_ip +'","timestamp": "' + now_str + '","sense hat temperature": ' + "float{:.2f}".format(temp)+ '","sense hat pressure": ' + "float{:.2f}".format(press)+ ' }'


        #send sensor data
        print(sense_hat_temp_payload)
        myMQTTClient.publish("pynq_test/sensor",sense_hat_temp_payload, 0)

        #get button instruction
        try:
            myMQTTClient.subscribe("pynq_test/button", 1,customCallback)
        except Exception as e:
            print(e)
            #pass


    accel_x, accel_y, accel_z = sensor_lsm9ds1.acceleration
    level_meter(accel_x, accel_y, buf, center_data)
    i2c.write(0x46, buf, 193)
    cnt = cnt + 1
    sleep(0.2)

