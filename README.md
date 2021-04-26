# ECE480-Team14 Automatic Sorting Robot

This is a repository for the ECE480 design project and it contain the nessaccery information to run the robot.

# Files for running the robot

The files can be found in the Silverware file in the raspberry pi. The functionality of the files are as follows:

1- SystemMain.py: Handle the PiCamera and main loop and connects every file and module used together.

2- ObjectDetection.py: Takes messurements of the silverware and processes it, Deal with image thresholding and contour finding.

3- ObjectTracking.py: Takes contour information, keeping the largest, Finds type of utensil, and queues the silverware.

4- ServoController.py: Allows control of the servo using RaspberryPi's gpiozero module,Sets the desired tray location.

5- Arduino Code: Controls the motor attaxhed to the belt. Affects the speed of the belt.

# How to Run

Run the following commands in the command line:

1- $ source OpenCV-master-pi3/bin/activate
2- $ cd SilverwareDetection/
3- $ python3 SystemMain.py

# Link for previous Repository

https://github.com/Dionise9/ECE480-Team2-Robot#objecttrackingpy
