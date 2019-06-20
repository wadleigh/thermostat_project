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
	

def main():
	withinAmount = 0.5
	numPoints = 20
	extraTimeBetweenPoints = 1
	timeBetweenReadings = 3 #in seconds
	readingsBetweenAdjustment = 1
	filename = Path("/home/pi/Data/temp_hum_log_summer.csv")#.expanduser()
	set_temp_file_name = 'set_temp.csv'


	pin1 = 7
	pinBR = 25
	while True:
		tempAve, humAve, tempAveBR, humAveBR = read_2_temps(numPoints,extraTimeBetweenPoints,timeBetweenReadings, pin1, pinBR)
		curTime = datetime.datetime.now()
		lineToWrite = '{0:%Y-%m-%d %H:%M:%S}, {1:0.2f}, {2:0.2f}, {3:0.2f}, {4:0.2f} \n'.format(curTime, tempAve, humAve, tempAveBR, humAveBR)

		with filename.open(mode = 'a') as log:
			log.write(lineToWrite)

		print(lineToWrite)

		time.sleep(timeBetweenReadings)


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