# Team Effort
# ECE 480 Team 2
# 12/4/2020
# Servo control module

from gpiozero import Servo
import time

# Create servo object using GPIO pin 17
servo = Servo(17)
# Set servo to it's minimum address
# Uses gpiozero Servo. Doc: https://gpiozero.readthedocs.io/en/stable/api_output.html
servo.value = 0.01
time.sleep(.5)
servo.value = None

# TODO Set tray postion based on given utensil string
def setTray(utensil,delay = 0):
	if delay:
		time.sleep(delay)
		
	print(utensil)
	if utensil == "knife":
		servo.value = .77
	elif utensil == "fork":
		servo.value = .4
	elif utensil == "spoon":
		servo.value = -.4
	else:
		servo.value = -.77

	time.sleep(.5)
	servo.value = None

	
# [utensil, tray time] ("Test case")
silverWare = [["fork",2],["spoon",6],["knife",10],["none",14]]
# Main controller, handles time
def main():
	start_time = time.time()
	while True:
		# Sleeps for .5, due to other on CPU may be more
		time.sleep(.5)
		elapsed_time = time.time() - start_time
		
		# Messy but works since our queue will always be small
		for i,table in enumerate(silverWare):
			if (table[1] < elapsed_time):
				setTray(table[0])
				silverWare.pop(i);
		
		if (len(silverWare) == 0):
			# For ending the test, this would actually go infinetly
			# in the final product
			break
			
#main()
		
