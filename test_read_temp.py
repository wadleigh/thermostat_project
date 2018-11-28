#!/usr/bin/env python3
import datetime

curTime = datetime.datetime.now()

with open('set_temp.csv') as setTempFile:
	setTemp = float(setTempFile.read())
setTempFile.closed

print(setTemp)