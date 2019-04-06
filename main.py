# -*- coding: utf-8 -*-
from dataprocessfunctions import *
from importantclasses import *
import collections
# import grovenfcreader
import grovepi
import time
import _thread as thread
import itchat

# Global variables
STATE = "ON"   # alarem state
LOUDNESS_SENSOR = "ON"
ULTRASONIC_SENSOR = "OFF"
PIR_SENSOR = "ON" 
WECHAT_MESSAGE = "OFF"

ID = "None"
lock = thread.allocate()
exit_flag = 0
warning_message = "NORMAL"
count = 0
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
	loudnessFilter = LoudnessFilter(0.5,0,30,15,6,8,5)
	distanceFilter = LowPassFilter(0.1, 500, 80)
	movementFilter = MedianFilter(20)

	return

def checkState():
	global warning_message, STATE,loudnessFilter,distanceFilter,movementFilter,count
	while True:
		time.sleep(1)
		global loudnessFilter, distanceFilter, movementFilter
		last_warning = warning_message
		if loudnessFilter.state == "NORMAL" and distanceFilter.state == "NORMAL" and movementFilter.state == "NORMAL":
			warning_message = "NORMAL"
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
		elif loudnessFilter.state == "WARNING" :
			warning_message = "Loudness sensor warning!"
		
		if last_warning != warning_message and warning_message != "NORMAL":
			with open('warning_history.csv', 'a') as f:
				f.write(time.strftime("%d-%m-%Y %H:%M:%S",time.localtime()) +", "+str(time.time())+"," + warning_message + "," + " 1" + str(loudnessFilter.cur_highPass) +"\n")
				count += 1
		if warning_message != "NORMAL":
			STATE = "ALERT"
		

	return

def collectSensorData():
	while True:
		if LOUDNESS_SENSOR == "ON" and STATE != "OFF":
			loudnessFilter.addData(grovepi.analogRead(1))    
		if ULTRASONIC_SENSOR == "ON" and STATE != "OFF":
			distanceFilter.addData(grovepi.ultrasonicRead(2))
		if PIR_SENSOR == "ON" and STATE != "OFF":
			movementFilter.addData(grovepi.digitalRead(3))
			
		time.sleep(0.01)

def activeNFCReader():
	global ID, lock
	while True:
		tempID = input()
		# tempID = grovenfcreader.waitForTag(3)    # using NFC tag
		if tempID != "None":    # empty input, skip current loop     
			ID = tempID
	return
	
def validateID():
	global ID, lock, myshop, STATE
	while True:
		# if lock.acquire():
		if myshop.checkIdentity(ID):   		 # ID is valid
			if STATE == "ALERT" or STATE == "ON":
				myshop.addActiveEmployee(ID)
				print (ID + " log in")
				with open('timeline.csv', 'a') as f:
					f.write(time.strftime("%d-%m-%Y %H:%M:%S",time.localtime()) +", "+ myshop.findNameById(ID) + ", " + "1\n")
				
				loudnessFilter.reset()
				movementFilter.reset()
				distanceFilter.reset()
				STATE = "OFF"                        # turn off the alarm
				print("Alarm off")
			elif STATE == "OFF":
				if myshop.checkIsActive(ID):
					myshop.removeActiveEmployeeByID(ID)
					print (ID + " log out")
					
					with open('timeline.csv', 'a') as f:
						f.write(time.strftime("%d-%m-%Y %H:%M:%S",time.localtime()) +", "+ myshop.findNameById(ID) + ", " + "0\n")
				else:
					myshop.addActiveEmployee(ID)
					print (ID + " log in")
					with open('timeline.csv', 'a') as f:
						f.write(time.strftime("%d-%m-%Y %H:%M:%S",time.localtime()) +", "+ myshop.findNameById(ID) + ", " + "1\n")
		elif ID != "None":
			print("Invalid ID: " + ID)
			# lock.release()
		ID = "None"		
		time.sleep(1)
	return	

initialiseHumanResource()
initialiseDataProcessor()
if WECHAT_MESSAGE == "ON":
	itchat.login(enableCmdQR = 2)
try:
	thread.start_new_thread(activeNFCReader,())
	thread.start_new_thread(validateID,())
	thread.start_new_thread(checkState,())
	thread.start_new_thread(collectSensorData,())
except Exception as e: 
	print(e)


while True:
	# check alarm state
	if STATE == "ON":	
		print(warning_message)
	elif STATE == "OFF":
		if myshop.getNumberOfStaffInShop() == 0:
			loudnessFilter.reset()
			movementFilter.reset()
			distanceFilter.reset()
			for x in range(10,0,-1):
				print("Alarm activate in " + str(x) + " second")
				time.sleep(1)
			STATE = "ON"
			print("Alarm on")
	elif STATE == "ALERT":
		print(warning_message + " Scan valid ID card to turn off!")

		if True:
			#itchat.send(warning_message, toUserName='filehelper')
			loudnessFilter.reset()
			movementFilter.reset()
			distanceFilter.reset()
			STATE = "OFF"

	time.sleep(1.5)
