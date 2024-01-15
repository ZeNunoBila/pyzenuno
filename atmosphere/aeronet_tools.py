'''
module that contains functions to treat and read AERONET data
'''


import pandas as pd
import datetime
def read_AERONET(aeronet_file,date_col_format='Date(dd-mm-yyyy)',site='MLO'):

	df = pd.read_csv(aeronet_file, na_values=["N/A","-999"])
	df['timestamp_UTC'] = df.apply(lambda s: pd.to_datetime(s[date_col_format] + " " + s['Time(hh:mm:ss)'],dayfirst=True), axis=1)
	if site=='MLO':
		df['timestamp_HST'] = df['timestamp_UTC'] - datetime.timedelta(hours=10)
		df.index = pd.DatetimeIndex(df.timestamp_HST)
	if site=='IZO':
		df['timestamp_WEST'] = df['timestamp_UTC'] - datetime.timedelta(hours=1)
		df.index = pd.DatetimeIndex(df.timestamp_WEST)
		
	return df
