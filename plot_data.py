#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt


def get_data_csv(file_name):
	""" read data in from a file """
	headers = ['date time','knob position','set point temp','lv temp','lr hum','br temp','br hum']
	data_frame = pd.read_csv(file_name, names = headers)
	return data_frame

def main():
	data_frame = get_data_csv('/Users/laurawadleigh/Dev/thermostat_data/temp_hum_log.csv')
	data_frame['date time'] = pd.to_datetime(data_frame['date time'])
	plt.plot(data_frame.loc[:,'date time'],data_frame.loc[:,'lv temp'])
	plt.show()

if __name__=="__main__":
	main()