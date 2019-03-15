#!/usr/bin/env python3
import datetime
import pandas

filename ="/home/pi/Data/temp_hum_log.csv"
data_frame = pandas.read_csv(filename)


print(data_frame.tail(1))
# curTime = datetime.datetime.now()
# hour = curTime.hour
# weekdaystring = curTime.strftime('%A') 

# print(data_frame.loc[hour, weekdaystring])