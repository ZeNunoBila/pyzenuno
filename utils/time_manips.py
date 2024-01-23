#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 14:30:20 2024

@author: nunop
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 15:29:52 2024

@author: nunop
"""
'''
module that contains functions for time manipulation
'''
#import time


def tObj2Nicedate(t=0):
	'''
	
	'''
	import datetime
	if t==0:
		dtobj = datetime.datetime.now()
	else:
		dtobj = t
	ts = dtobj2str(dtobj,T=False,ms=False)
	return ts
		


def average_TimeStamp(dtobj1,dtobj2):
	'''
	function that gives the average TimeStamp between datetime objects 1 and 2	
	input and output arguments are all datetime objects
	'''
	#print (type(dtobj1))
	t1 = dtobj2tstamp(dtobj1)
	t2 = dtobj2tstamp(dtobj2)
	tm = (t1+t2)/2
	return tstamp2tdobj(tm)
	
	

def YYYYmmdd2dtobj(date):
	'''
	function converting YYYYmmdd strings to datetime objects
	'''
	pass
	

def get_closest_time(dtlist,dtobj):
	'''
	get the element of the list dtlist closest to dtobj
	'''
	import time
	import numpy as np
	import pyzenuno.misc_tools as pyzntools

	dtobj = time.mktime(dtobj.timetuple())
	dtlist = np.array([time.mktime(d.timetuple()) for d in dtlist])

	aa = pyzntools.find_nearest(dtlist,dtobj)
	#print dtobj
	#print dtlist
	return aa
	#nearest=min(dtlist, key=lambda x: abs(x - dtobj))
	#timedelta = abs(nearest - dtobj)
	#return nearest, timedelta
	
	
def str2dtobj(date):
	'''
	function converting YYYY-mm-dd(T)HH:MM:SS(.fff) strings to datetime objects
	automatically detects if T and/or microseconds are present
	'''
	import datetime

	fmt_sep = ' '
	fmt_ms = ''
	if date[10] == 'T':
		fmt_sep = 'T'
	elif date[10] == '-':
		fmt_sep = '-'		
	if len(date)>22:
		fmt_ms = '.%f'	  
	fmt = '%Y-%m-%d' + fmt_sep + '%H:%M:%S' + fmt_ms
	dtobj = datetime.datetime.strptime(date,fmt)
	return dtobj



def dtobj2str(dtobj,T=True,ms=True):
	'''
	function converting datetime objects to SOLSPEC telemetry format strings
	inputs:
	dtobj: datetime object
	T: bool: include T as separator between date and time (default True)
	ms: bool: include miliseconds (default True)
	'''
	import datetime

	fmt_sep = ' '
	fmt_ms = ''
	if T:
		fmt_sep = 'T'
	if ms:
		fmt_ms = '.%f'	  
	fmt = '%Y%m%d_%H%M%S' + fmt_ms
	dout = datetime.datetime.strftime(dtobj,fmt)
	return dout
	
def interpolate_time_series(new_t_grid,old_t_grid,data,left=None,right=None):
	import numpy as np
	new_t_grid_ts = dtobj2tstamp(new_t_grid)
	old_t_grid_ts = dtobj2tstamp(old_t_grid)
	
	new_data = np.interp(new_t_grid_ts,old_t_grid_ts,data,left=left,right=right)
	
	return new_data
	
def dtobj2tstamp(dtobj):
	'''
	function that converts a datetime object to a serial time float
	'''
	import datetime
	import time
	import numpy as np
	ts = []
	try:
		for t in dtobj:		  
			ts.append(time.mktime(datetime.datetime.timetuple(t))+t.microsecond/1.e6)
		
		ts = np.array(ts)
	except TypeError: # this means that we dont have an array
		ts = time.mktime(datetime.datetime.timetuple(dtobj))+dtobj.microsecond/1.e6
	return ts
	
def tstamp2tdobj(tstamp):
	'''
	function that converts a time stamp serial to a datetimeobject
	'''
	import datetime 
	return datetime.datetime.fromtimestamp(tstamp)
	
def YYYYmmdd_HHMM_to_dtobj(dstr):
	'''
	function that converts str datetimes in YYYYmmdd_HHMM to a datetime object
	'''
	import datetime

	fmt = '%Y%m%d_%H%M'
	dtobj = datetime.datetime.strptime(dstr,fmt)
	return dtobj

def YYYYmmdd_to_dobj(dstr):
	'''
	function that converts str datetimes in YYYYmmdd to a date object
	'''
	import datetime

	fmt = '%Y%m%d'
	dtobj = datetime.datetime.strptime(dstr,fmt).date()
	return dtobj
	
def datetime2matlabdn(dt):
   import datetime

   mdn = dt + datetime.timedelta(days = 366)
   frac_seconds = (dt-datetime.datetime(dt.year,dt.month,dt.day,0,0,0)).seconds / (24.0 * 60.0 * 60.0)
   frac_microseconds = dt.microsecond / (24.0 * 60.0 * 60.0 * 1000000.0)
   return mdn.toordinal() + frac_seconds + frac_microseconds
   
def fractional_year(dr):
	
	#'''
	#function that converts a datetime object into a fractional year float
	import datetime

	doy = dr.year + (dr.dayofyear + dr.hour / 24.0 + dr.minute / (24.0 * 60))/365.0
	return doy