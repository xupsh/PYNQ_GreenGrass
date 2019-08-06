# AWS IOT LAB
## What you will learn
After finishing the following steps, you will build a cluster using PYNQ-Z2 in which devices can communicate with each other and work together. You can press the buttons in publisher board and the leds in subscriber board can glitter accordingly.
## What is AWS Greengrass
AWS IoT Greengrass is software that extends cloud capabilities to local devices. This enables devices to collect and analyze data closer to the source of information, react autonomously to local events, and communicate securely with each other on local networks. AWS IoT Greengrass developers can use AWS Lambda functions and prebuilt connectors to create serverless applications that are deployed to devices for local execution.  
The following diagram shows the basic architecture of AWS IoT Greengrass.
![Geengrass](https://docs.aws.amazon.com/greengrass/latest/developerguide/images/greengrass.png)
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
- Connect to your boards successfully.
- Make sure your boards can access internet.
## Step by Step
- [Connect to your board](https://pynq.readthedocs.io/en/v2.4/getting_started/pynq_z2_setup.html).
- Run the following commands on all boards.
  ```shell
  sudo adduser --system ggc_user
  sudo addgroup --system ggc_group
  ```
- In our lab, we will have one board used as core, two boards as device (one board used as publisher and the other used as subscriber).
- In the core board, you have to follow [module2](https://docs.aws.amazon.com/zh_cn/greengrass/latest/developerguide/module2.html) to set your board.  
![Group Created](https://docs.aws.amazon.com/greengrass/latest/developerguide/images/gg-get-started-009.2.png)
- In the device board, you have to follow [module4](https://docs.aws.amazon.com/zh_cn/greengrass/latest/developerguide/module4.html) to create your two devices. Please pay attention that the tutorial uses just one pc, we have to split the pc into two PYNQ boards. What you need to do is to replace the two consoles opened in pc with two boards' processes.  
![Devices](https://docs.aws.amazon.com/greengrass/latest/developerguide/images/gg-get-started-065.5.png)
- Now, in your core board, you will have /greengrass and you should run the daemon process in it.
  ```shell
  cd /greengrass/ggc/core/
  sudo ./greengrassd start
  ```
- In other two boards (one is for subscriber, one is for publisher), you will have a root-ca-certs.pem and xxx-setup.tar.gz respectively. Then unzip the package and put button.py|sensor.py in the same directory.
- Edit the button.py|sensor.py, find places "xxxx" and replace them with your own settings.
- Deploy your group and wait until the deployment is finished and then you can run publisher and subscriber processes finally.
- The test step is [here](https://docs.aws.amazon.com/zh_cn/greengrass/latest/developerguide/test-comms.html). In publisher board, you can run:
  ```shell
  sudo python3 button.py
  ```
  And in subscriber board, you run:
  ```shell
  sudo python3 sensor.py
  ```
- Now when you press the button in publisher you can see leds in subscriber glitter. Also you can build a subscriber in AWS cloud. Search AWS IoT in *Services*. Choose *Test* and then *Subscribe to a topic*, fill the topic with yours(here hello/world/pubsub). In *MQTT payload display*, we choose the second *Display payloads as strings*. Now subscribe to the topic and you will find a new tip on the left, enter it and you can watch the information of the button actions.
## Further
Now you have learned how to use aws greengrass, you can replace the "hello world" function with something cool. Maybe you can refer to [this](https://github.com/xupsh/PYNQ_GreenGrass/tree/master/demo-learning).
## Reference
[AWS Tutorial](https://docs.aws.amazon.com/zh_cn/greengrass/latest/developerguide/gg-gs.html)
