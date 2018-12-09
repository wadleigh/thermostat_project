#!/usr/bin/env python3
import datetime
import pandas

file_name = "schedule_of_temps.csv"
data_frame = pandas.read_csv(file_name)

curTime = datetime.datetime.now()
hour = curTime.hour
weekdaystring = curTime.strftime('%A') 

print(data_frame.loc[hour, weekdaystring])