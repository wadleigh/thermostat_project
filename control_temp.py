#!/usr/bin/env python3

import Adafruit_DHT
import time
import datetime
from pathlib import Path
import RPi.GPIO as GPIO

def read_temp(numPoints,extraTimeBetweenPoints,timeBetweenReadings):
	sensor = Adafruit_DHT.DHT22
	pin = 7
	tempList = []
	humList = []
	#Doesn't save the first reading (it seems to be wrong most of the time)
	for i in range(numPoints+1):
		# Try to grab a sensor reading.  Use the read_retry method which will retry up
		# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
		humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
		#curTime = time.asctime( time.localtime(time.time()) )
		if i > 0:
			tempList.append(temperature)
			humList.append(humidity)
		time.sleep(extraTimeBetweenPoints)

	# Convert the temperature to Fahrenheit.
	tempAve = sum(tempList) / len(tempList)  * 9/5.0 + 32
	humAve = sum(humList) / len(humList)
	return tempAve, humAve


def control_motor(curPos, direction, FracOfRotToTurn):
	#variables to determine rotation
	#1 clockwise, 0 counterclockwise (when looking at motor, dial on heater is reversed)
	# zero turns up temp, 1 turns down temp
	signOfDirection = 1 - direction * 2

	#pin number (not GPIO number)
	stepPin = 31
	directionPin = 33

	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(stepPin, GPIO.OUT)
	GPIO.setup(directionPin, GPIO.OUT)
	GPIO.output(stepPin, 0)
	GPIO.output(directionPin, direction)

	maxPos = 0.75 #It can actually go a little past 0.75 turns, so this is conservative
	minPos = 0
	hitExtrema = 0

	targetPos = curPos + signOfDirection * FracOfRotToTurn
	if targetPos > maxPos:
	  hitExtrema = 1
	  targetPos = maxPos
	elif targetPos < minPos:
	  hitExtrema = 1
	  targetPos = minPos

	FracOfRotToTurn = (targetPos - curPos) / signOfDirection 

	stepsInRot = 200
	numSteps = int(round(stepsInRot * FracOfRotToTurn))

	timeStep = 0.001
	for i in range(numSteps):
	  GPIO.output(stepPin, 1)
	  time.sleep(timeStep)
	  GPIO.output(stepPin, 0)
	  time.sleep(timeStep)
	GPIO.cleanup()
	return targetPos, hitExtrema


def main():
	targetTemp = 66
	withinAmount = 0.5
	numPoints = 10
	extraTimeBetweenPoints = 1
	timeBetweenReadings = 60*1
	readingsBetweenAdjustment = 10
	filename = Path("/home/pi/Data/temp_hum_log.csv")#.expanduser()

	curPos = 0 #starting position of knob
	setPos = 0.5 #Position to turn to knob too initially
	#increase temp
	direction = 0
	curPos, hitExtrema = control_motor(curPos, direction, setPos)
	FracOfRotToTurn = 0.02 

	while True:
		for i in range(readingsBetweenAdjustment):
			tempAve, humAve = read_temp(numPoints,extraTimeBetweenPoints,timeBetweenReadings)
			curTime = datetime.datetime.now()
			lineToWrite = '{0:%Y-%m-%d %H:%M:%S}, {1:0.2f}, {2:0.2f}, {3:0.2f} \n'.format(curTime, tempAve, humAve, curPos)

			with filename.open(mode = 'a') as log:
				log.write(lineToWrite)

			print(lineToWrite)

			time.sleep(timeBetweenReadings)

		if tempAve < (targetTemp - withinAmount): 
			#increase temp
			direction = 0
			curPos, hitExtrema = control_motor(curPos, direction, FracOfRotToTurn)
			
		elif tempAve > (targetTemp + withinAmount):
			#decrease temp
			direction = 1
			curPos, hitExtrema = control_motor(curPos, direction, FracOfRotToTurn)

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