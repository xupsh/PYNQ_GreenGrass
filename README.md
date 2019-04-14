# PYNQ_GreenGrass

# [AWS GreenGrass](<https://aws.amazon.com/greengrass/>)

<https://docs.aws.amazon.com/greengrass/latest/developerguide/gg-gs.html>

# Structure

![Structure of the demo](https://github.com/xupsh/PYNQ_GreenGrass/blob/master/image/AWS%20Greengrass%20DEMO%20structure.png)

# Quick Start

## Install [AWS IoT Device SDK for Python](<https://github.com/aws/aws-iot-device-sdk-python>)

> > git clone https://github.com/aws/aws-iot-device-sdk-python.git
> >
> > cd aws-iot-device-sdk-python
> >
> > python3 setup.py install

## The installation of [sensor hat](<https://github.com/xupsh/pynq-sense-hat>) on **senser** board 

> > sudo pip3 install git+https://github.com/xupsh/pynq-sense-hat.git

![**sensor** board](https://github.com/xupsh/PYNQ_GreenGrass/blob/master/image/sensor_borad.jpeg)

## Greengrass Core

Follow the steps to create your own AWS Greengrass Group and Greengrass Core.

## Run the demo

Prepare **three** PYNQ board, and run **button.py**, **sensor.py** and **Greengrass Core** on them seperately.

Before running, mention to update your own AWS endpoint and AWS authority keys in the codes.

NOTE: Run as root.