from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import sys
import imutils
import os
import tinys3
import yaml
import datetime

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

image_width = cfg['image_settings']['horizontal_res']
image_height = cfg['image_settings']['vertical_res']
file_extension = cfg['image_settings']['file_extension']
file_name = cfg['image_settings']['file_name']
photo_interval = cfg['image_settings']['photo_interval'] # Interval between photo (in seconds)
image_folder = cfg['image_settings']['folder_name']

if not os.path.exists(image_folder):
    os.makedirs(image_folder)
# Get user supplied values
#cascPath = sys.argv[1]

# Create the haar cascade
#face_cascade = cv2.CascadeClassifier('/home/pi/opencv-3.0.0/data/haarcascades/haarcascade_frontalface_default.xml')
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#eye_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_eye.xml')
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(640, 480))

# allow the camera to warmup
time.sleep(0.1)
lastTime = time.time()*1000.0
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
    image = frame.array
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 3)
    
    # Detect faces in the image
    faces = face_cascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(30, 30),
    flags = cv2.cv.CV_HAAR_SCALE_IMAGE
    )
    print time.time()*1000.0-lastTime," Found {0} faces!".format(len(faces))
    lastTime = time.time()*1000.0
    # Draw a rectangle around the faces
    if (len(faces) > 0):
        st = datetime.datetime.utcnow()
        filepath = image_folder + '/' + "face" + str(st) + file_extension 
        cv2.imwrite(filepath, image)
        if cfg['debug'] == True:
            print '[debug] Uploading ' + filepath + ' to s3'

        # Upload to S3
        conn = tinys3.Connection(cfg['s3']['access_key_id'], cfg['s3']['secret_access_key'])
        f = open(filepath, 'rb')
        conn.upload(filepath, f, cfg['s3']['bucket_name'],
                   headers={
                   'x-amz-meta-cache-control': 'max-age=60'
                   })
        
    for (x, y, w, h) in faces:
        #cv2.circle(image, (x+w/2, y+h/2), int((w+h)/3), (255, 255, 255), 1)
        cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = image[y:y+h, x:x+w]
        cv2.imwrite("Test.jpg", image)
      # eyes = eye_cascade.detectMultiScale(roi_gray)
      # for (ex,ey,ew,eh) in eyes:
      #     cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
    # show the frame
    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF
 
	# clear the stream in preparation for the next frame
    rawCapture.truncate(0)
    
	# if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
        
  
        

