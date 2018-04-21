#!/usr/bin/python
import RPi.GPIO as GPIO
import time 
import os
import picamera
import MySQLdb
from datetime import datetime

db=MySQLdb.connect(host="jjsample.cnfdilkrunc8.us-west-2.rds.amazonaws.com",port=3306,user="justin",passwd="justin12",db="sample1")

dbase=db.cursor()
piccnt=0

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
count = 0
RANGE=60 # distance in cm
PICSPATH = "/home/pi/Development/pics/"
 
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2
    #return (distance, pir)
    return distance

def distance2():
    GPIO.output(GPIO_TRIGGER2, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER2, False)
 
    StartTime2 = time.time()
    StopTime2 = time.time()
 
    while GPIO.input(GPIO_ECHO2) == 0:
        StartTime2 = time.time()
    while GPIO.input(GPIO_ECHO2) == 1:
        StopTime2 = time.time()
 
    TimeElapsed2 = StopTime2 - StartTime2
    distance2 = (TimeElapsed2 * 34300) / 2
    #return (distance2, pir)
    return distance2

if __name__ == '__main__':
    try:
        while True:
            temp = count
            dist = distance()
            dist2 = distance2()
            pir = GPIO.input(GPIO_PIR)
            
           # print "Distance1: %0.1f Distance2: %0.1f" %(dist, dist2)
            #print "PIR: %s PIR2 %s "  %(pir, pir2)
            if dist2 < dist:
                if pir and (dist2 < RANGE and dist > RANGE):
                    redo=4;
                    while redo > 0:
                        dist = distance()
                        if dist <= RANGE:
                            print "Entered!!!"
                            count+=1
                            now= datetime.now()
                            try:
                                dbase.execute("""INSERT INTO  main_door VALUES ( %s, %s)""",( now , count))
                                db.commit()
                            except:
                                print "CANNOT EXECUTE"
                                db.rollback()
                            with picamera.PiCamera() as cam:
                                cam.resolution=(1280, 720)
                                cam.capture(PICSPATH + str(piccnt) + ".jpg")
                                #cam.capture(PICSPATH + "test" + ".jpg")
                               # os.system("scp -i /home/pi/newace.pem /home/pi/Development/pics/%s.jpg ec2-user@ec2-54-191-39-89.us-west-2.compute.amazonaws.com:/var/www/html/img/" %(str(now)))
                            piccnt+=1
                            print "Picture Taken!"
                            break
                        redo -=1
                        #time.sleep(0.20)
                        time.sleep(0.25)
            if dist < dist2:
                if pir and (dist < RANGE and dist2 > RANGE):
                    redo=4
                    while redo > 0:
                        dist2 = distance2()
                        if dist2 <= RANGE:
                            print "Exited!!!"
                            count-=1
                            now= datetime.now()
                            try:
                                dbase.execute("""INSERT INTO  main_door VALUES ( %s, %s)""",( now , count))
                                #dbase.execute("""INSERT INTO  RM_1 VALUES ( %s,%s, %s)""",( now ,mic, count))
                                db.commit()
                            except:
                                print "CANNOT EXECUTE2"
                                db.rollback()
                            break
                        redo -=1
                        #time.sleep(0.20)
                        time.sleep(0.25)
            if temp != count:
                now= datetime.now()
                print "%s Count:%s " %( str(now), count)
            time.sleep(0.1)
        # Reset by pressing CTRL + C except KeyboardInterrupt:
    except Exception as e:
        print e
        print("Exiting counter!")
    finally:
        GPIO.cleanup()
