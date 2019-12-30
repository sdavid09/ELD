#!/usr/bin/python
import RPi.GPIO as GPIO
import time 
import os
import picamera
import MySQLdb
from datetime import datetime

cnt=0
count = 0
RANGE=100 # distance in cm
PICSPATH = "/home/pi/Development/pics/"
GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 17
GPIO_ECHO = 27

GPIO_TRIGGER2 = 23 
GPIO_ECHO2 = 24
GPIO_PIR = 22

GPIO.setup(GPIO_PIR, GPIO.IN) #PIR
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

GPIO.setup(GPIO_TRIGGER2, GPIO.OUT)
GPIO.setup(GPIO_ECHO2, GPIO.IN)

class Counter(object):
    def __init__(self, dbg=False): 
        self.dbg=dbg
        pass

    def setDebug(self, val):
        self.dbg = val
        
    def distance(self, GPIO_TRIGGER, GPIO_ECHO):
        # set Trigger to HIGH
        GPIO.output(GPIO_TRIGGER, True)
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)
     
        StartTime = time.time()
        StopTime = time.time()
     
        while GPIO.input(GPIO_ECHO) == 0:
            StartTime = time.time()
        while GPIO.input(GPIO_ECHO) == 1:
            StopTime = time.time()
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        distance = (TimeElapsed * 34300) / 2
        return distance

#   def distance2(self):
#       # set Trigger to HIGH
#       GPIO.output(GPIO_TRIGGER2, True)
#       # set Trigger after 0.01ms to LOW
#       time.sleep(0.00001)
#       GPIO.output(GPIO_TRIGGER2, False)
#    
#       StartTime2 = time.time()
#       StopTime2 = time.time()
#    
#       # save StartTime
#       while GPIO.input(GPIO_ECHO2) == 0:
#           StartTime2 = time.time()
#       # save time of arrival
#       while GPIO.input(GPIO_ECHO2) == 1:
#           StopTime2 = time.time()
#    
#       TimeElapsed2 = StopTime2 - StartTime2
#       distance2 = (TimeElapsed2 * 34300) / 2
#       return distance2

    def sendToDatabase(self, data): 
        db=MySQLdb.connect(host="jjsample.cnfdilkrunc8.us-west-2.rds.amazonaws.com",port=3306,user="justin",passwd="justin12",db="sample1")
        dbase=db.cursor()

    def takePicture(self, file):
        pass

    def determineDirection(self, dist, dist2):
        if dist < dist2 and dist < RANGE:
            print "Exiting"
        elif dist2 <  dist and dist2 < RANGE:
            print "Entering"

    def start(self):
        while True:
            pir = GPIO.input(GPIO_PIR) # PIR sensor
           #dist = self.distance(GPIO_TRIGGER=17,GPIO_ECHO=27)
           #dist2 = self.distance(GPIO_TRIGGER=23, GPIO_ECHO=24)
            dist = self.distance(GPIO_TRIGGER,GPIO_ECHO)
            dist2 = self.distance(GPIO_TRIGGER2, GPIO_ECHO2)
            if self.dbg:
                print "Distance: %s Distance2: %s " %(dist, dist2)
            if pir:
                self.determineDirection(dist, dist2)
            time.sleep(1)

if __name__ == '__main__':
    cnt = Counter(dbg=True)
    try:
        cnt.start()
    except Exception as e:
        print e
        print("Exiting counter!")
    finally:
        GPIO.cleanup()
    
