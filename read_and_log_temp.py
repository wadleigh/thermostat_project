#!/usr/bin/env python3
# now with 100% more git

import Adafruit_DHT
import time
import datetime
from pathlib import Path

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
sensor = Adafruit_DHT.DHT22
pin = 7

numPoints = 5
extraTimeBetweenPoints = 1
timeBetweenReadings=60*10

filename = Path("/home/pi/Data/temp_hum_log.csv")#.expanduser()

while True:
	tempList = []
	humList = []
	#Doesn't save the first reading (it seems to be wrong most of the time)
	for i in range(numPoints+1):
		humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
		#curTime = time.asctime( time.localtime(time.time()) )
		curTime = datetime.datetime.now()
		if i > 0:
			tempList.append(temperature)
			humList.append(humidity)
		time.sleep(extraTimeBetweenPoints)

	# Convert the temperature to Fahrenheit.
	tempAve = sum(tempList) / len(tempList)  * 9/5.0 + 32
	humAve = sum(humList) / len(humList)

	lineToWrite = '{0:%Y-%m-%d %H:%M:%S}, {1:0.2f}, {2:0.2f} \n'.format(curTime, tempAve, humAve)

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