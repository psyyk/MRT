# -*- coding: utf-8 -*-
from dataprocessfunctions import *
from importantclasses import *
import collections
# import grovenfcreader
import grovepi
import time
import thread

# Global variables
STATE = "ON"   # alarem state
LOUDNESS_SENSOR = "OFF"
ULTRASONIC_SENSOR = "OFF"
PIR_SENSOR = "ON" 

ID = "None"
lock = thread.allocate()
exit_flag = 0
warning_message = ""

def initialiseHumanResource():

	global staff, myshop

	yanke = Employee("Yan Ke", "4302467")
	jack = Employee("Jack Ma", "666666")
	tom = Employee("Tom Zhang", "333211")
	staff = []

	staff.append(yanke)
	staff.append(jack)
	staff.append(tom)

	myshop = Shop(staff)

	return

def initialiseDataProcessor():
	global loudnessFilter, distanceFilter, movementFilter
	loudnessFilter = LoudnessFilter(0.5,0,34,10,4,6)
	distanceFilter = LowPassFilter(0.1, 500, 300)
	movementFilter = MedianFilter(5)

	return

def checkState():
	global warning_message
	while True:
		time.sleep(1)
		global loudnessFilter, distanceFilter, movementFilter
		if loudnessFilter.state == "NORMAL" and distanceFilter.state == "NORMAL" and movementFilter.state == "NORMAL":
			warning_message = "NORMAL"
			print("111")
			continue
		elif loudnessFilter.state == "WARNING" and distanceFilter.state == "WARNING" and movementFilter.state == "NORMAL":
			warning_message = "Loudness sensor and Ultrasonic sensor warning!"	
		elif loudnessFilter.state == "WARNING" and distanceFilter.state == "NORMAL" and movementFilter.state == "WARNING":
			warning_message = "Loudness sensor and PIR sensor warning!"	
		elif loudnessFilter.state == "NORMAL" and distanceFilter.state == "WARNING" and movementFilter.state == "WARNING":
			warning_message = "Ultrasonic sensor and PIR sensor warning!"	
		elif loudnessFilter.state == "WARNING" and distanceFilter.state == "WARNING" and movementFilter.state == "WARNING":
			warning_message = "Loudness sensor and Ultrasonic sensor and PIR sensor warning!"	
		elif distanceFilter.state == "WARNING":
			warning_message = "Ultrasonic sensor warning!"
		elif movementFilter.state == "WARNING" :
			warning_message = "PIR sensor warning!"
			print("222")

		elif loudnessFilter.state == "WARNING" :
			warning_message = "Loudness sensor warning!"
		state = "ALERT"
	return

def collectSensorData():
	while True:
		if LOUDNESS_SENSOR == "ON" and STATE == "ON":
			loudnessFilter.addData(grovepi.analogRead(1))    
		if ULTRASONIC_SENSOR == "ON" and STATE == "ON":
			distanceFilter.addData(grovepi.ultrasonicRead(2))
		if PIR_SENSOR == "ON" and STATE == "ON":
			movementFilter.addData(grovepi.digitalRead(3))
			print("333")
		time.sleep(0.01)

def activeNFCReader():
	global ID, lock
	while True:
		tempID = raw_input()
		# tempID = grovenfcreader.waitForTag(3)    # may need change
		if tempID != "None":    # empty input, skip current loop     无输入时这个值是多少？？
			# if lock.acquire():
			ID = tempID
				# lock.release()
	return
	
def validateID():
	global ID, lock, myshop, STATE
	while True:
		# if lock.acquire():
		if myshop.checkIdentity(ID):   		 # ID is valid
			if STATE == "ALERT" or STATE == "ON":
				myshop.addActiveEmployee(ID)
				print (ID + " log in")
				STATE = "OFF"                        # turn off the alarm
				print("Alarm off")
			elif STATE == "OFF":
				if myshop.checkIsActive(ID):
					myshop.removeActiveEmployeeByID(ID)
					print (ID + " log out")
				else:
					myshop.addActiveEmployee(ID)
					print (ID + " log in")
		elif ID != "None":
			print("Invalid ID: " + ID)
			# lock.release()
		ID = "None"		
		time.sleep(1)
	return	

initialiseHumanResource()
initialiseDataProcessor()

try:
	thread.start_new_thread(activeNFCReader,())
	thread.start_new_thread(validateID,())
	thread.start_new_thread(checkState,())
	thread.start_new_thread(collectSensorData,())
except:
	print("something wrong")


while True:
	# check current state
	if STATE == "ON":	
		print(warning_message)
	elif STATE == "OFF":
		if myshop.getNumberOfStaffInShop() == 0:
			for x in range(5,0,-1):
				print("Alarm activate in " + str(x) + "second")
				time.sleep(1)
			STATE = "ON"

			print("Alarm on")
	elif STATE == "ALERT":
		print("Alerting!!! Scan valid ID card to turn off!")

	
	time.sleep(1)

# 不同state打印不同输出
# checkState()






