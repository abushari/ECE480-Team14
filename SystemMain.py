# Nicholas Dionise
# ECE 480 Team 2
# 12/4/2020
# Main system controller

import time
import picamera
import picamera.array
import cv2
import numpy as np
import io
import ObjectDetection
import ObjectTracking
import ServoController
# Lots of imports

# Init cameras
camera = picamera.PiCamera()
camera.resolution = (640,480)
camera.framerate = 32
rawCapture = picamera.array.PiRGBArray(camera, size=(640,480))

# Init image to save each frame
image = np.empty((640, 480, 3), dtype=np.uint8)

# Warm up camera...
time.sleep(1)

delay = 0
previous = time.perf_counter()

ctr = 0

tracked_objs = []
	
debug = 0

# For loop to grab frames from camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	ctr = ctr + 1
	# Crop image
	image = frame.array[80:460 , 60:580]

	# Run the image through the object detection
	ret = ObjectDetection.image_processing(image, debug)
	if debug == 1:
		cv2.imwrite("Image"+str(ctr)+".jpg",image)
	if ret:
		print(len(ret[1]))
		for tup in ret[1]:
			# For every found contour, print it's information
			print("Major:", tup[0], "Minor:", tup[1], "Centroid, X:", tup[2], "Y:", tup[3], "Area:", tup[4])
		ObjectTracking.track_objects(ret[1])
		cv2.imshow("Im out", np.hstack((image, ret[0])))
		#cv2.imwrite("Output"+str(ctr)+".jpg", np.hstack((image, tup[0])))
	else:
		cv2.imshow("Im out", image)
		cv2.waitKey(1)
		rawCapture.truncate(0)
		continue
	
	newTime = time.perf_counter()
	
	elapsedTime = newTime - previous
	
	previous = newTime
	
	delay = max(0, delay - elapsedTime)
	
	cv2.waitKey(1) # 0 for manual step
	rawCapture.truncate(0)
