# AWS IOT LAB
## About this Lab
After finishing the following steps, you will build a cluster using PYNQ-Z2 in which devices can communicate with each other and work together. You can press the buttons in publisher board and the leds in subscriber board can glitter accordingly.
## What is AWS Greengrass
AWS IoT Greengrass is software that extends cloud capabilities to local devices. This enables devices to collect and analyze data closer to the source of information, react autonomously to local events, and communicate securely with each other on local networks. AWS IoT Greengrass developers can use AWS Lambda functions and prebuilt connectors to create serverless applications that are deployed to devices for local execution.  
The following diagram shows the basic architecture of AWS IoT Greengrass.
![Geengrass](https://github.com/wutianze/PYNQ_GreenGrass/blob/master/image/greengrass.png)
AWS IoT Greengrass makes it possible for customers to build IoT devices and application logic. Specifically, AWS IoT Greengrass provides cloud-based management of application logic that runs on devices. Locally deployed Lambda functions and connectors are triggered by local events, messages from the cloud, or other sources.  
In AWS IoT Greengrass, devices securely communicate on a local network and exchange messages with each other without having to connect to the cloud. AWS IoT Greengrass provides a local pub/sub message manager that can intelligently buffer messages if connectivity is lost so that inbound and outbound messages to the cloud are preserved.  
AWS IoT Greengrass protects user data:  
Through the secure authentication and authorization of devices.  
Through secure connectivity in the local network.  
Between local devices and the cloud.  
Device security credentials function in a group until they are revoked, even if connectivity to the cloud is disrupted, so that the devices can continue to securely communicate locally.  
AWS IoT Greengrass provides secure, over-the-air software updates of Lambda functions.
## Preparation
- > 3 PYNQ-Z2  
  > AWS account  
  > 1 switch  
## Step by Step
- > The following steps you can refer to [this](https://pynq.readthedocs.io/en/v2.4/getting_started/pynq_z2_setup.html).
  > Conncet your boards and your pc to your switch through LAN(In your switch). Conncet WAN(In your switch) to the Internet.
  > Conncet your boards to your pc through usb using serial link. Run ipconfig in the terminals opened for boards and find your boards' ips.
  > Close the serial link windows and using ssh to connect to your boards.
- Run the following commands on all boards.
  ```shell
  sudo adduser --system ggc_user
  sudo addgroup --system ggc_group
  ```
- In our lab, we will have one board used as core, two boards as device (one board used as publisher and the other used as subscriber).
- > Create your group and set your core board.  
  > Sign in to the AWS Management Console on your computer and open the AWS IoT Core console. If this is your first time opening this console, choose Get started.
Choose Greengrass.  
![choose greengrass](https://docs.aws.amazon.com/greengrass/latest/developerguide/images/console-greengrass.png)
If you don't see the Greengrass node in the navigation pane, change to an AWS Region that supports AWS IoT Greengrass. For the list of supported regions, see AWS Regions and Endpoints in the AWS General Reference.
  > 
After this step, you will see the following picture in your AWS monitor. And the core process is running in your core board.
![Group Created](https://docs.aws.amazon.com/greengrass/latest/developerguide/images/gg-get-started-009.2.png)
- Configure two devices in AWS web.  
![Devices](https://docs.aws.amazon.com/greengrass/latest/developerguide/images/gg-get-started-065.5.png)  
First follow [Create AWS IoT Devices in an AWS IoT Greengrass Group](https://docs.aws.amazon.com/greengrass/latest/developerguide/device-group.html) to create your two devices. And then [Configure Subscriptions](https://docs.aws.amazon.com/greengrass/latest/developerguide/config-subs.html). Now you will see the group has been deployed successfully.  
- Then you have to [Install the AWS IoT Device SDK for Python](https://docs.aws.amazon.com/greengrass/latest/developerguide/IoT-SDK.html) in your two device boards.  
In this lab, we won't use basicDiscovery.py in AWS tutorial. We will use button.py and sensor.py instead, you can find them in this respository. Copy the button.py to your publisher board and sensor.py to your subscriber board. Remember to copy the .py file to the folder that contains the HelloWorld_Publisher and HelloWorld_Subscriber device certificates files.  
- Edit the button.py&sensor.py, find places "xxxx" and replace them with your own settings.  
![example](https://github.com/xupsh/PYNQ_GreenGrass/blob/master/image/Capture.PNG)  
The first 'xxxx' place is where you put your endpoint adress. The other two places are where you put your own device certificates files.  You can refer to [this](https://docs.aws.amazon.com/greengrass/latest/developerguide/test-comms.html) to find what 'xxxx' should be.
- In publisher board, run:
  ```shell
  sudo python3 button.py
  ```
  And in subscriber board, run:
  ```shell
  sudo python3 sensor.py
  ```
  Wait a minute until the two processes is up.
- Now when you press the button in publisher you can see leds in subscriber glitter. Also you can build a subscriber in AWS cloud. Search AWS IoT in *Services*. Choose *Test* and then *Subscribe to a topic*, fill the topic with yours(here hello/world/pubsub). In *MQTT payload display*, we choose the second *Display payloads as strings*. Now subscribe to the topic and you will find a new tip on the left, enter it and you can watch the information of the button actions.
## Further
Now you have learned how to use aws greengrass, you can replace the "hello world" function with something cool. Maybe you can refer to [this](https://github.com/wutianze/PYNQ_GreenGrass/blob/master/demo-learning.md).
## Reference
[AWS Tutorial](https://docs.aws.amazon.com/zh_cn/greengrass/latest/developerguide/gg-gs.html)
