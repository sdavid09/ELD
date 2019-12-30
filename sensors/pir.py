#!/usr/bin/python
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(22, GPIO.IN) #PIR

try:
    time.sleep(2) # to stabilize sensor
    while True:
        if GPIO.input(22):
            time.sleep(0.5) #Buzzer turns on for 0.5 sec
            print("Motion Detected...")
            time.sleep(3) #to avoid multiple detection
	else:
	    print("False")
        time.sleep(0.1) #loop delay, should be less than detection delay

except:
    GPIO.cleanup()
