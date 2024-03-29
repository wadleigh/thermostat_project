#!/usr/bin/env python3

import Adafruit_DHT
import time
import datetime
from pathlib import Path
import RPi.GPIO as GPIO
import PID
import pandas

def read_temp(numPoints, extraTimeBetweenPoints, timeBetweenReadings, pin):
	""" Read in the temperature and humidity data from the sensor """
	sensor = Adafruit_DHT.DHT22
	tempList = []
	humList = []
	for i in range(numPoints):
		# Try to grab a sensor reading.  Use the read_retry method which will retry up
		# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
		humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
		#curTime = time.asctime( time.localtime(time.time()) )
		if humidity < 100.1:
			tempList.append(temperature)
			humList.append(humidity)
		time.sleep(extraTimeBetweenPoints)

	# Convert the temperature to Fahrenheit.
	tempAve = sum(tempList) / len(tempList)  * 9/5.0 + 32
	humAve = sum(humList) / len(humList)
	return tempAve, humAve

def read_2_temps(numPoints, extraTimeBetweenPoints, timeBetweenReadings, pin1, pin2):
	""" Read in the temperature and humidity data from the sensor """
	sensor = Adafruit_DHT.DHT22
	tempList = []
	humList = []
	temp2List = []
	hum2List = []
	for i in range(numPoints):
		# Try to grab a sensor reading.  Use the read_retry method which will retry up
		# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
		humidity, temperature = Adafruit_DHT.read_retry(sensor, pin1)
		humidity2, temperature2 = Adafruit_DHT.read_retry(sensor, pin2)
		#curTime = time.asctime( time.localtime(time.time()) )
		if humidity < 100.1:
			tempList.append(temperature)
			humList.append(humidity)
		if humidity2 < 100.1:
			temp2List.append(temperature2)
			hum2List.append(humidity2)
		time.sleep(extraTimeBetweenPoints)

	# Convert the temperature to Fahrenheit.
	tempAve = sum(tempList) / len(tempList)  * 9/5.0 + 32
	humAve = sum(humList) / len(humList)
	temp2Ave = sum(temp2List) / len(temp2List)  * 9/5.0 + 32
	hum2Ave = sum(hum2List) / len(hum2List)
	return tempAve, humAve, temp2Ave, hum2Ave



def control_motor(curPos, FracOfRotToTurn):
	""" Control the motor.  Assume the position starts at "curPos". """
	#variables to determine rotation
	#1 clockwise, 0 counterclockwise (when looking at motor, dial on heater is reversed)
	# zero turns up temp, 1 turns down temp
	if FracOfRotToTurn >= 0:
		#increase temp
		direction = 0
		
	elif FracOfRotToTurn < 0:
		#decrease temp
		direction = 1

	#pin number (not GPIO number)
	stepPin = 31
	directionPin = 33

	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(stepPin, GPIO.OUT)
	GPIO.setup(directionPin, GPIO.OUT)
	GPIO.output(stepPin, 0)
	GPIO.output(directionPin, direction)

	#Round the fraction to turn to the nearest step
	stepsInRot = 200
	stepsToTurn = round(stepsInRot * FracOfRotToTurn)

	maxPos = 0.75 #It can actually go a little past 0.75 turns, so this is conservative
	minPos = 0
	maxPos = round(stepsInRot * maxPos)
	minPos = round(stepsInRot * minPos)
	hitExtrema = 0

	targetPos = curPos + stepsToTurn
	if targetPos > maxPos:
	  hitExtrema = 1
	  targetPos = maxPos
	elif targetPos < minPos:
	  hitExtrema = 1
	  targetPos = minPos

	stepsToTurn = targetPos - curPos 
	numSteps = abs(stepsToTurn)

	timeStep = 0.02
	for i in range(numSteps):
	  GPIO.output(stepPin, 1)
	  time.sleep(timeStep)
	  GPIO.output(stepPin, 0)
	  time.sleep(timeStep)
	GPIO.cleanup()
	return targetPos, hitExtrema

def find_set_point_temp_for_now():
	file_name = "schedule_of_temps.csv"
	data_frame = pandas.read_csv(file_name)

	curTime = datetime.datetime.now()
	hour = curTime.hour
	weekdaystring = curTime.strftime('%A') 
	return data_frame.loc[hour, weekdaystring]

def read_set_temp(set_temp_file_name):
	""" read the set point tempurature in from a file """
	with open('set_temp.csv') as setTempFile:
		setTemp = float(setTempFile.read())
	setTempFile.closed
	return setTemp

def control_pid(pid_object, input_cur_temp, set_point_temp):
	""" Manipulates the pid object """
	#Errors will be of order 1.  The ranges is ~ -10 to 10.
	pid_object.SetPoint = set_point_temp
	

def main():
	withinAmount = 0.5
	numPoints = 20
	extraTimeBetweenPoints = 1
	timeBetweenReadings = 3 #in seconds
	readingsBetweenAdjustment = 1
	filename = Path("/home/pi/Data/temp_hum_log_summer_2020.csv")#.expanduser()
	set_temp_file_name = 'set_temp.csv'
	
	targetTemp = find_set_point_temp_for_now()
	curPos = 0 #starting position of knob
	setPos = 0 #Amount to turn knob initially, can be positive or negative #0 increases temp, 1 decreases temp
	curPos, hitExtrema = control_motor(curPos, setPos)

	#Initiallize a PID object
	#Errors will be of order 1.  The ranges is ~ -10 to 10.
	P = 0.01
	I = 0.0
	D = 0.06
	pid = PID.PID(P, I, D)
	pid.windup_guard = 20 #Don't accumulate more that this amount of error in degrees F in the integral
	pid.SetPoint = targetTemp
	pid.setSampleTime(60)

	pin1 = 7
	pinBR = 25
	while True:
		for i in range(readingsBetweenAdjustment):
			tempAve, humAve, tempAveBR, humAveBR = read_2_temps(numPoints,extraTimeBetweenPoints,timeBetweenReadings, pin1, pinBR)
			curTime = datetime.datetime.now()
			lineToWrite = '{0:%Y-%m-%d %H:%M:%S}, {1:0.3f}, {2:0.2f}, {3:0.2f}, {4:0.2f}, {5:0.2f}, {6:0.2f} \n'.format(curTime, curPos, targetTemp, tempAve, humAve, tempAveBR, humAveBR)

			with filename.open(mode = 'a') as log:
				log.write(lineToWrite)

			print(lineToWrite)

			time.sleep(timeBetweenReadings)

		targetTemp = find_set_point_temp_for_now()
		pid.SetPoint = targetTemp
		pid.update(tempAve)
		fracToChange = pid.output

		curPos, hitExtrema = control_motor(curPos, fracToChange)



	# Note that sometimes you won't get a reading and
	# the results will be null (because Linux can't
	# guarantee the timing of calls to read the sensor).
	# If this happens try again!
	#if humidity is not None and temperature is not None:
	#    print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
	#else:
	#    print('Failed to get reading. Try again!')
	#    sys.exit(1)

if __name__=="__main__":
	main()