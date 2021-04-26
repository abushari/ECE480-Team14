# Team Effort
# ECE 480 Team 2
# 12/4/2020
# Originally created to attempt to track silverware
# Instead sets tray after being detected in the center of the image

import ServoController
import threading

# Finds if test is withing beta of center (Used to work of a alpha percentage)
def min_max_comp(test, center, beta):
    return (test > (center - beta) and test < (center + beta))

#tup[0] = major, tup[1] = minor, tup[2] = x, tup[3] = y, tup[4] = area, tup[5] = type, tup[6] = ctr

# Fork major, spoon major, soup spoon major, knife major
fM, sM1, sM2, kM = 395, 260, 220, 530 
# Fork minor, spoon minor, soup spoon minor, knife minor
fm, sm1, sm2, km = 50, 62, 85, 40

# Beta minor axis
bm = 5
# Beta major axis
bM = 40

# Finds if a position is within beta of another position (Same as min_max_comp except different variable orders)
def test_in_beta(pos1,pos2,beta):
	posMax = pos1 + beta
	posMin = pos1 - beta
	
	return (pos2 > posMin and pos2 < posMax)

# Does test in beta for x and y positions in given contour objects
def test_x_y(obj1,obj2,beta): 
	return (test_in_beta(obj1[2],obj2[2],beta) and test_in_beta(obj1[3],obj2[3],beta))
	
	
# Removes duplicated given objects, uses largest
def remove_dups(objs):
	toRemove = set()
	# Terrible time complexity, but number of objects is small
	for i1,obj1 in enumerate(objs):
		for i2,obj2 in enumerate(objs):
			if i2 == i1:
				continue
			if test_x_y(obj1,obj2,40):
				if obj2[4] > obj1[4]:
					toRemove.add(i1)
					print("add 1")
				else:
					print("add 2")
					toRemove.add(i2)
					
	for i in sorted(toRemove,reverse=True):
		del objs[i]
		
	return objs

	# Creates a thread to delay the arrival of the utensil, acts as a queue
	# Otherwise pyhton will pause on the wait, in this case only this thread
	# isn't scheduled, not the entire process
def create_set_tray_thread(utensil):
	threading.Thread(target=ServoController.setTray,args=(utensil,1.7)).start()
	
	# Tracks contours on screen, the middle was discovered to be the most acurate way 
	# to clasify the silverware. Once it's detected a piece it takes the contour stats
	# and pushes them through the conditional. It then queues a tray position.
def track_objects(objs):
	# Remove duplicates (Such as nested contours)
	objs = remove_dups(objs)

	for tup in objs:
		# Conditionals for finding utensil type
		if test_in_beta(260,tup[2],10):
			if min_max_comp(tup[0], fM, bM):
				create_set_tray_thread("fork")
				#print("Fork detected")
			elif min_max_comp(tup[0], sM1, bM) or min_max_comp(tup[0], sM2, bM):
				#print("Spoon detected")
				create_set_tray_thread("spoon")
			elif min_max_comp(tup[1], km, bm):
				#print("Knife detected")
				create_set_tray_thread("knife")
			else:
				#print("None detected")
				create_set_tray_thread("none")
		
	
