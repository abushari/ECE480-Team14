# Nicholas Dionise
# ECE 480 Team 2
# 12/4/2020
# Object detection module
# Can't handle the seam in the belt.

import numpy as np
import cv2
import time

# Takes in image, applies adaptive threshold
# Returns list of contours found in image, and information related to them
def image_processing(im_in, debug=0):
	try:
		# Filter out high frequency noise on conveyor belt
		im_in = cv2.bilateralFilter(im_in, 4, 50, 75, borderType=cv2.BORDER_DEFAULT)
		
		# Find edges using canny edge detection
		edges = cv2.Canny(im_in, 60, 70)
		
		# Convert input images to grayscale for adaptive thresholding
		im_in = cv2.cvtColor(im_in, cv2.COLOR_BGR2GRAY)

		# Run adaptive thresholding
		im_th = cv2.adaptiveThreshold(im_in, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 5)

		# Combine canny and adaptive to try and fill gaps in the edge detection
		im_th = im_th | edges

		# Copy the thresholded image.
		im_floodfill = im_th.copy()

		# Mask used to flood filling.
		# Notice the size needs to be 2 pixels than the image.
		h, w = im_th.shape[:2]
		mask = np.zeros((h + 2, w + 2), np.uint8)

		# Floodfill from point (0, 0) and (width, height)
		cv2.floodFill(im_floodfill, mask, (0, 0), 255)
		width, height = im_in.shape[1], im_in.shape[0]
		cv2.floodFill(im_floodfill, mask, (width-1, height-1), 255)

		# Invert floodfilled image
		im_floodfill_inv = cv2.bitwise_not(im_floodfill)

		# Combine the two images to get the foreground.
		im_out = im_th | im_floodfill_inv


		# Display images.
		if debug == 1:
			cv2.imshow("Thresholded Image", im_th)
			cv2.imshow("Floodfilled Image", im_floodfill)
			cv2.imshow("Inverted Floodfilled Image", im_floodfill_inv)
			cv2.imshow("Edges", edges)
			cv2.imshow("Output", im_out)
			cv2.waitKey(0)

		# Clones image draw for the contour display
		im_draw = im_out.copy()

		# Prepares to find contours
		edges = im_out
		
		# Prints for when debug mode is enabled
		if debug == 1:
			cv2.imshow("Detection", np.hstack((im_in, edges)))
			cv2.waitKey(0)

		contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE,
											   cv2.CHAIN_APPROX_SIMPLE)	 # Edge detection, image segmentation, adaptive
		
		# Convert it to color so we can see the outline
		im_draw = cv2.cvtColor(im_draw, cv2.COLOR_GRAY2BGR)
		
		# Found countours and information about them
		usedContours = []
		returnList = []
		
		# Iterate over contours to find areas which fit the minimum size criteria.
		for c in contours:
			area = cv2.contourArea(c)
			if area > 900:
				# Pulls info from contour for later
				usedContours.append(c)
				# (location) (major-minor axis)
				(x, y), (MA, ama), angle = cv2.fitEllipse(c)
				majorAxis = max(MA, ama)
				minorAxis = min(MA, ama)
				# Area used to make sure size is correct
				returnTab = [majorAxis, minorAxis, x, y, area, "none", 0]
				returnList.append(returnTab)
		
		# Display the found contours on the images 
		cv2.drawContours(im_draw, usedContours, -1, (255, 0, 0), 3)
		
		return im_draw, returnList
	except:
		return None
