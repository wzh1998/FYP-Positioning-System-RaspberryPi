#!/usr/bin/env python
import serial
import RPi.GPIO as GPIO
import os
import sys
import time
import string
from subprocess import Popen
ser = serial.Serial(
       # port='/dev/ttyS0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0

        port='/dev/ttyUSB0',
#	port='/dev/ttyS0',
        baudrate = 38400,
        
        
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)

#movie1 = ("/home/pi/Videos/1.mp4")
#movie2 = ("/home/pi/Videos/2.mp4")
while 1:

#	print(ser.name)
#        y=ser.readline()
	y=ser.read(ser.inWaiting())
	time.sleep(0.01)
#        print x
	x = y.replace("U", "")
	print x
	time.sleep(1)
        
	if x == '3000E2000019060C01360510E09F488D':
         print "A"
	 time.sleep(3)
       
        elif x== '3000E2000019060C00770650D633EB30':
         print "B"
	 time.sleep(3)
        else:
         print "none"

