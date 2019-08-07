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
![xg](https://github.com/xupsh/PYNQ_GreenGrass/blob/master/image/IMG_20190807_104705.jpg)
## Step by Step
- The following steps you can refer to [this](https://pynq.readthedocs.io/en/v2.4/getting_started/pynq_z2_setup.html).
- Conncet your boards and your pc to your switch through LAN(In your switch). Conncet WAN(In your switch) to the Internet.
- Conncet your boards to your pc through usb using serial link. Run 
  ```shell
  hostname -I 
  ```  
  in the terminals opened for boards and find your boards' ips.
- Close the serial link windows and using ssh to connect to your boards.
- Run the following commands on all boards.
  ```shell
  sudo adduser --system ggc_user
  sudo addgroup --system ggc_group
  ```
- In our lab, we will have one board used as core, two boards as device (one board used as publisher and the other used as subscriber).
- Create your group and set your core board. This part you can refer to [this](https://docs.aws.amazon.com/greengrass/latest/developerguide/gg-config.html).  
- Sign in to the AWS Management Console on your computer and open the AWS IoT Core console. If this is your first time opening this console, choose Get started.
- Choose Greengrass.  
![choose greengrass](https://docs.aws.amazon.com/greengrass/latest/developerguide/images/console-greengrass.png)  
- If you don't see the Greengrass node in the navigation pane, change to an AWS Region that supports AWS IoT Greengrass. For the list of supported regions, see AWS Regions and Endpoints in the AWS General Reference.
- On the Welcome to AWS IoT Greengrass page, choose Create a Group.  
  An AWS IoT Greengrass group contains settings and other information about its components, such as devices, Lambda functions, and connectors. A group defines how its components can interact with each other.  
- On the Set up your Greengrass group page, choose Use easy creation to create a group and an AWS IoT Greengrass core.  
  Each group requires a core, which is a device that manages local IoT processes. A core needs a certificate and keys that allow it to access AWS IoT and an AWS IoT policy that allows it to perform AWS IoT and AWS IoT Greengrass actions. When you choose the Use easy creation option, these security resources are created for you and the core is provisioned in the AWS IoT registry.  
![set up](https://docs.aws.amazon.com/greengrass/latest/developerguide/images/gg-get-started-005.png)
- Enter a name for your group (for example, MyFirstGroup), and then choose Next.  
  ![name](https://docs.aws.amazon.com/greengrass/latest/developerguide/images/gg-get-started-006.png)
- Use the default name for the AWS IoT Greengrass core, and then choose Next.
  ![default name](https://docs.aws.amazon.com/greengrass/latest/developerguide/images/gg-get-started-007.png)
- On the Run a scripted easy Group creation page, choose Create Group and Core.  
  ![create group and core](https://docs.aws.amazon.com/greengrass/latest/developerguide/images/gg-get-started-008.png)
- Download your core's security resources and configuration file. On the confirmation page, under Download and store your Core's security resources, choose Download these resources as a tar.gz.
  ![download](https://docs.aws.amazon.com/greengrass/latest/developerguide/images/gg-get-started-009.png)
- After you download the security resources, choose Finish.  
  The group configuration page is displayed in the console:  
  ![finish](https://docs.aws.amazon.com/greengrass/latest/developerguide/images/gg-get-started-009.2.png)
- Download the AWS IoT Greengrass Core software installation package. Choose the CPU architecture and distribution (and operating system, if necessary) that best describe your core device. This time we choose ARMv7l for Raspbian package.
- In the previous step, you downloaded two files to your computer:  
  > greengrass-OS-architecture-1.9.2.tar.gz. This compressed file contains the AWS IoT Greengrass Core software that runs on the core device.  
  > hash-setup.tar.gz. This compressed file contains security certificates that enable secure communications between AWS IoT and the config.json file that contains configuration information specific to your AWS IoT Greengrass core and the AWS IoT endpoint.
  Transfer the two compressed files from your computer to the AWS IoT Greengrass core device.  
  The commands for example:  
  ```shell
  cd path-to-downloaded-files
  scp greengrass-OS-architecture-1.9.2.tar.gz xilinx@IP-address:/home/xilinx
  scp hash-setup.tar.gz xilinx@IP-address:/home/xilinx
  ```
- Open a terminal on the AWS IoT Greengrass core device and navigate to the folder that contains the compressed files.  
  Decompress the AWS IoT Greengrass Core software and the security resources.  
  > The first command creates the /greengrass directory in the root folder of the AWS IoT Greengrass core device (through the -C / argument).  
  > The second command copies the certificates into the /greengrass/certs folder and the config.json file into the /greengrass/config folder (through the -C /greengrass argument).
  ```shell
  cd path-to-compressed-files
  sudo tar -xzvf greengrass-OS-architecture-1.9.2.tar.gz -C /
  sudo tar -xzvf hash-setup.tar.gz -C /greengrass
  ```  
- Download the appropriate ATS root CA certificate. The following example downloads AmazonRootCA1.pem. The wget -O parameter is the capital letter O.  
  ```shell
  cd /greengrass/certs/
  sudo wget -O root.ca.pem https://www.amazontrust.com/repository/AmazonRootCA1.pem
  ```  
  You can run the following command to confirm that the root.ca.pem file is not empty:  
  ```shell
  cat root.ca.pem
  ```
- Start AWS IoT Greengrass on your core device.  
  ```shell
  cd /greengrass/ggc/core/
  sudo ./greengrassd start
  ```  
  You should see a Greengrass successfully started message.  
- Configure two devices in AWS web. This part you can refer to [this](https://docs.aws.amazon.com/greengrass/latest/developerguide/module4.html)   
- First Create AWS IoT Devices in an AWS IoT Greengrass Group
  In the AWS IoT Core console, choose Greengrass, choose Groups, and then choose your group.  
- On the group configuration page, choose Devices, and then choose Add your first Device.  
    ![CD](https://docs.aws.amazon.com/greengrass/latest/developerguide/images/gg-get-started-066.png)  
- Choose Create New Device.  
    ![ND](https://docs.aws.amazon.com/greengrass/latest/developerguide/images/gg-get-started-067.png)  
- Register this device as HelloWorld_Publisher, and then choose Next.  
    ![RD](https://docs.aws.amazon.com/greengrass/latest/developerguide/images/gg-get-started-068.png)  
- For 1-Click, choose Use Defaults. This option generates a device certificate with attached AWS IoT policy and public and private key.  
    ![1C](https://docs.aws.amazon.com/greengrass/latest/developerguide/images/gg-get-started-069.png)  
- Create a folder on your publisher board. Download the certificate and keys for your device into the folder.  
    ![CF](https://docs.aws.amazon.com/greengrass/latest/developerguide/images/gg-get-started-070.png)  
  Make a note of the common hash component in the file names for the HelloWorld_Publisher device certificate and keys (in this example, bcc5afd26d). You need it later. Choose Finish.  
- Decompress the hash-setup.tar.gz file. For example, run the following command:  
    ```shell
    tar -xzf hash-setup.tar.gz
    ```  
- Choose Add Device and repeat steps to add a new device to the group.  
  Name this device HelloWorld_Subscriber. Download the certificates and keys for the device to your subscriber board. Save and decompress them in the same folder that you created for HelloWorld_Publisher.  
  Again, make a note of the common hash component in the file names for the HelloWorld_Subscriber device.  
- You should now have two devices in your AWS IoT Greengrass group:  
    ![tg](https://docs.aws.amazon.com/greengrass/latest/developerguide/images/gg-get-started-071.png)  
- Save the root CA certificate as root-ca-cert.pem in the same folder as the certificates and keys for both devices.  
    ```shell
    cd path-to-folder-containing-device-certificates
    curl -o ./root-ca-cert.pem https://www.amazontrust.com/repository/AmazonRootCA1.pem
    ```  
  If you meet some net issues here, don't be afraid, you can use the root-ca-cert.pem you downloaded before or just ask someone to give you a copy of it.  
- Configure Subscriptions  
  In this step, you enable the HelloWorld_Publisher device to send MQTT messages to the HelloWorld_Subscriber device.  
  > On the group configuration page, choose Subscriptions, and then choose Add Subscription.
  > Configure the subscription.
  >> Under Select a source, choose Devices, and then choose HelloWorld_Publisher.
  >> Under Select a target, choose Devices, and then choose HelloWorld_Subscriber.
  >> Choose Next.  
  ![sb](https://docs.aws.amazon.com/greengrass/latest/developerguide/images/gg-get-started-072.png)  
- For Topic filter, enter hello/world/pubsub, choose Next, and then choose Finish.  
  Make sure that the AWS IoT Greengrass daemon is running, as described in Deploy Cloud Configurations to a Core Device.  
- On the group configuration page, from Actions, choose Deploy.  
  ![dp](https://docs.aws.amazon.com/greengrass/latest/developerguide/images/gg-get-started-040.png)  
- Then you have to Install the AWS IoT Device SDK for Python.
  Run the following commands to install the AWS IoT Device SDK for Python:  
    ```shell
    cd ~
    git clone https://github.com/aws/aws-iot-device-sdk-python.git
    cd aws-iot-device-sdk-python
    sudo python setup.py install
    ```  
- We will use button.py and sensor.py in this lab, you can find them in this respository. Copy the button.py to your publisher board and sensor.py to your subscriber board. Remember to copy the .py file to the folder that contains the HelloWorld_Publisher and HelloWorld_Subscriber device certificates files.  
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
