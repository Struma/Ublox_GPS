#!/usr/bin/python

#A simple serial GPS test script for the Ublox A6 gps

import serial
import pynmea2

ser = serial.Serial('/dev/ttyUSB0',9600)

while 1:
    data = ser.readline()
    if (data.startswith("$GPRMC")):
        msg = pynmea2.parse(data)
        print(str(msg.latitude) + " " + str(msg.longitude))
