# -*- coding: utf-8 -*-
"""
Created on Tue Nov 07 15:49:03 2017

@author: nunop
"""


import numpy as np
import datetime


class atm_calcs:


	import numpy as np
	import datetime

	time_passed_midnight = None
	julian_day = None
	julian_century = None
	geom_mean_long_sun = None
	geom_mean_anom_sun = None
	ecc_earth_orbit = None
	sun_eq_ctr = None
	sun_true_long = None
	sun_true_anom = None
	sun_rad_vec = None
	sun_app_long_deg = None
	mean_obliq_eclip = None
	obliq_corr = None
	sun_rt_asc = None
	sun_decli = None
	var_y = None
	eq_time = None
	ha_sunrise = None
	solar_noon = None
	sunrise_time = None
	sunset_time = None
	sunlight_dur = None
	true_solar_time = None
	hour_angle = None
	sza = None
	sea = None
	app_atm_ref = None
	sea_corr = None
	saa = None
	sza_corr = None
	amf_KY = None
	
#{"lat":19.539,"lon":-155.578}}
	def __init__(self,dt,tz,site='uccle'):	
		# GMT == UTC
		# Belgium is UTC + 2 in summer and UTC + 1 in winter
		# IZO is UTC in winter and UTC +1 in summer (last saturday october <-> last saturday march)		
		dict_coords = {"uccle":{"lat":50.79679,"lon":4.356953,"tz":2},"mont-rigi":{"lat":50.51127,"lon":6.074233},"mlo":{"lat":19.539,"lon":-155.578,"tz":-10},"izo":{"lon":-16.499,"lat":28.308,"tz":0},"jung":{"lat":46.541831166,"lon": 7.97416277,"tz":2}}
		self.lat = dict_coords[site]["lat"]
		self.lon = dict_coords[site]["lon"]
		self.dt = dt		
		self.tz	= tz	## change in V2, as  TZ changes along the year and from location to location, better to be set here as hard parameter
		self.calc_mins_passed_midnight()
		self.calc_julian_day()
		self.calc_julian_century()
		self.calc_geom_mean_long_sun()
		self.calc_geom_mean_anom_sun()
		self.calc_ecc_earth_orbit()
		self.calc_sun_eq_ctr()
		self.calc_sun_tru_long()
		self.calc_sun_tru_anom()
		self.calc_sun_rad_vec()
		self.calc_sun_app_long_deg()
		self.calc_mean_obliq_eclip()
		self.calc_obli_corr()
		self.calc_sun_rt_asc()
		self.calc_sun_decli()
		self.calc_var_y()
		self.calc_eq_time()
		self.calc_ha_sunrise()
		self.calc_solar_noon()
		self.calc_sunrise_time()
		self.calc_sunset_time()
		self.calc_sunlight_dur()
		self.calc_true_solar_time()
		self.calc_hour_angle()
		self.calc_sza()
		self.calc_sea()
		self.calc_app_atm_ref()
		self.calc_sea_corr()
		self.calc_saa()
		self.calc_sza_corr()	  
		self.calc_amf_KY()
		
		import numpy as np
		import datetime

	def calc_mins_passed_midnight(self):
		dd = np.array([self.dt.year,self.dt.month,self.dt.day,self.dt.hour,self.dt.minute,self.dt.second]) - np.array([self.dt.year,self.dt.month,self.dt.day,0,0,0])
		mpm = dd[3]*60. + dd[4] + dd[5]/60.
		atm_calcs.time_passed_midnight = mpm/(60.*24)
		#print 'time passed midnight ' + str(atm_calcs.time_passed_midnight)

	def calc_julian_day(self):
		dts_ref = datetime.datetime.toordinal(datetime.datetime(1899,12,30,0,0,0))
		dts_aux = datetime.datetime.toordinal(datetime.datetime(self.dt.year,self.dt.month,self.dt.day,0,0,0))
		d_actual = dts_aux-dts_ref
		atm_calcs.julian_day = d_actual + 2415018.5 + atm_calcs.time_passed_midnight
			#print 'julian day ' + str(atm_calcs.julian_day)

	def calc_julian_century(self):
		atm_calcs.julian_century = (atm_calcs.julian_day - 2451545.) / 36525.
		#print 'julian century ' + str(atm_calcs.julian_century)

	def calc_geom_mean_long_sun(self):
		atm_calcs.geom_mean_long_sun = np.mod(280.46646 + atm_calcs.julian_century * (36000.76983 + atm_calcs.julian_century * 0.0003032), 360)
		#print 'geometric mean longitude sun ' + str(atm_calcs.geom_mean_long_sun)

	def calc_geom_mean_anom_sun(self):
		atm_calcs.geom_mean_anom_sun = 357.52911+atm_calcs.julian_century*(35999.05029 - 0.0001537*atm_calcs.julian_century)
		#print 'geometric mean anomaly sun ' + str(atm_calcs.geom_mean_anom_sun)

	def calc_ecc_earth_orbit(self):
		atm_calcs.ecc_earth_orbit = 0.016708634-atm_calcs.julian_century*(0.000042037+0.0000001267*atm_calcs.julian_century)
		#print 'eccentricity earth orbit ' + str(atm_calcs.ecc_earth_orbit)

	def calc_sun_eq_ctr(self):
		atm_calcs.sun_eq_ctr = np.sin((np.pi / 180.) * (atm_calcs.geom_mean_anom_sun)) * (1.914602 - atm_calcs.julian_century * (0.004817 + 0.000014 * atm_calcs.julian_century)) + np.sin(2. * (np.pi / 180) * (atm_calcs.geom_mean_anom_sun)) * (0.019993 - 0.000101 * atm_calcs.julian_century) + np.sin(3. * (np.pi / 180) * (atm_calcs.geom_mean_anom_sun)) * 0.000289
		#print 'sun eq ctr ' + str(atm_calcs.sun_eq_ctr)

	def calc_sun_tru_long(self):
		atm_calcs.sun_true_long = atm_calcs.geom_mean_long_sun + atm_calcs.sun_eq_ctr
		#print 'sun true long ' + str(atm_calcs.sun_true_long)

	def calc_sun_tru_anom(self):
		atm_calcs.sun_true_anom = atm_calcs.geom_mean_anom_sun + atm_calcs.sun_eq_ctr
	
	def calc_sun_rad_vec(self):
		atm_calcs.sun_rad_vec = (1.000001018 * (1 - atm_calcs.ecc_earth_orbit * atm_calcs.ecc_earth_orbit)) / (1 + atm_calcs.ecc_earth_orbit * np.cos((np.pi / 180) * (atm_calcs.sun_true_anom)))
	
	def calc_sun_app_long_deg(self):		
		atm_calcs.sun_app_long_deg = atm_calcs.sun_true_long - 0.00569 - 0.00478 * np.sin((np.pi / 180) * (125.04 - 1934.136 * atm_calcs.julian_century))
		
	def calc_mean_obliq_eclip(self):
		atm_calcs.mean_obliq_eclip = 23 + (26 + ((21.448 - atm_calcs.julian_century * (46.815 + atm_calcs.julian_century * (0.00059 - atm_calcs.julian_century * 0.001813)))) / 60) / 60
		
	def calc_obli_corr(self):
		atm_calcs.obliq_corr = atm_calcs.mean_obliq_eclip + 0.00256 * np.cos((np.pi / 180) * (125.04 - 1934.136 * atm_calcs.julian_century))
	
	def calc_sun_rt_asc(self):
		atm_calcs.sun_rt_asc = (180 / np.pi) * (np.arctan2(np.cos((np.pi / 180) * (atm_calcs.obliq_corr)) * np.sin((np.pi / 180) * (atm_calcs.sun_app_long_deg)), np.cos((np.pi / 180) * (atm_calcs.sun_app_long_deg))))
		
	def calc_sun_decli(self):		
		atm_calcs.sun_decli = (180 / np.pi) * (np.arcsin(np.sin((np.pi / 180) * (atm_calcs.obliq_corr)) * np.sin((np.pi / 180) * (atm_calcs.sun_app_long_deg))))
		
	def calc_var_y(self):
		atm_calcs.var_y = np.tan((np.pi / 180) * (atm_calcs.obliq_corr / 2)) * np.tan((np.pi / 180) * (atm_calcs.obliq_corr / 2))
		
	def calc_eq_time(self):
		atm_calcs.eq_time = 4 * (180 / np.pi) * (atm_calcs.var_y * np.sin((np.pi / 180) * (2 * atm_calcs.geom_mean_long_sun)) - 2 * atm_calcs.ecc_earth_orbit * np.sin((np.pi / 180) * (atm_calcs.geom_mean_anom_sun)) + 4 * atm_calcs.ecc_earth_orbit * atm_calcs.var_y * np.sin(		  (np.pi / 180) * (atm_calcs.geom_mean_anom_sun)) * np.cos((np.pi / 180) * (2 * atm_calcs.geom_mean_long_sun)) - 0.5 * atm_calcs.var_y * atm_calcs.var_y * np.sin(		  (np.pi / 180) * (4 * atm_calcs.geom_mean_long_sun)) - 1.25 * atm_calcs.ecc_earth_orbit * atm_calcs.ecc_earth_orbit * np.sin((np.pi / 180) * (2 * atm_calcs.geom_mean_anom_sun)))
	
	def calc_ha_sunrise(self):
		atm_calcs.ha_sunrise = np.degrees(np.arccos(np.cos((np.pi / 180) * (90.833)) / (np.cos((np.pi / 180) * (self.lat)) * np.cos((np.pi / 180) * (atm_calcs.sun_decli))) - np.tan((np.pi / 180) * (self.lat)) * np.tan((np.pi / 180) * (atm_calcs.sun_decli))))
		
	def calc_solar_noon(self):
		atm_calcs.solar_noon = (720 - 4 * self.lon - atm_calcs.eq_time + self.tz * 60.) / 1440
		
	def calc_sunrise_time(self):
		atm_calcs.sunrise_time = atm_calcs.solar_noon - atm_calcs.ha_sunrise * 4 / 1440
		
	def calc_sunset_time(self):
		atm_calcs.sunset_time = atm_calcs.solar_noon + atm_calcs.ha_sunrise * 4 / 1440
		
	def calc_sunlight_dur(self):
		atm_calcs.sunlight_dur = 8 * atm_calcs.ha_sunrise
	
	def calc_true_solar_time(self):	   
		atm_calcs.true_solar_time = np.mod(atm_calcs.time_passed_midnight * 1440 + atm_calcs.eq_time + 4 * self.lon - 60 * self.tz, 1440)
		
	def calc_hour_angle(self):
		if (atm_calcs.true_solar_time / 4) < 0:
			atm_calcs.hour_angle = atm_calcs.true_solar_time / 4 + 180
		else:
			atm_calcs.hour_angle = atm_calcs.true_solar_time / 4 - 180
	
	def calc_sza(self):
		atm_calcs.sza = (180 / np.pi) * (np.arccos(np.sin((np.pi / 180) * (self.lat)) * np.sin((np.pi / 180) * (atm_calcs.sun_decli)) + np.cos((np.pi / 180) * (self.lat)) * np.cos((np.pi / 180) * (atm_calcs.sun_decli)) * np.cos((np.pi / 180) * (atm_calcs.hour_angle))))
		#print 'sza ' + str(atm_calcs.sza)

	def calc_sea(self):
		atm_calcs.sea = 90 - atm_calcs.sza
		
	def calc_app_atm_ref(self):
		if atm_calcs.sea > 85:
			atm_calcs.app_atm_ref = 0;
		else:
			if atm_calcs.sea > 5:
				atm_calcs.app_atm_ref = 58.1 / np.tan((np.pi / 180) * (atm_calcs.sea)) - 0.07 / np.tan((np.pi / 180) * (atm_calcs.sea)) ** 3 + 0.000086 / np.tan((np.pi / 180) * (atm_calcs.sea)) ** 5
			else:
				if atm_calcs.sea > -0.575:
					atm_calcs.app_atm_ref = 1735 + atm_calcs.sea * (-518.2 + atm_calcs.sea * (103.4 + atm_calcs.sea * (-12.79 + atm_calcs.sea * 0.711)))
				else:
					atm_calcs.app_atm_ref = -20.772 / np.tan((np.pi / 180) * (atm_calcs.sea));
		
		atm_calcs.app_atm_ref = atm_calcs.app_atm_ref / 3600

	def calc_sea_corr(self):
		atm_calcs.sea_corr = atm_calcs.sea + atm_calcs.app_atm_ref

	def calc_saa(self):
		if atm_calcs.hour_angle > 0:
			atm_calcs.saa = np.mod((180 / np.pi) * (np.arccos(((np.sin((np.pi / 180) * (self.lat)) * np.cos((np.pi / 180) * (atm_calcs.sza))) - np.sin((np.pi / 180) * (atm_calcs.sun_decli))) / (np.cos((np.pi / 180) * (self.lat)) * np.sin((np.pi / 180) * (atm_calcs.sza))))) + 180, 360);
		else:
			atm_calcs.saa = np.mod(540 - (180 / np.pi) * (np.arccos(((np.sin((np.pi / 180) * (self.lat)) * np.cos((np.pi / 180) * (atm_calcs.sza))) - np.sin((np.pi / 180) * (atm_calcs.sun_decli))) / (np.cos((np.pi / 180) * (self.lat)) * np.sin((np.pi / 180) * (atm_calcs.sza))))), 360);
	
	def calc_sza_corr(self):
		atm_calcs.sza_corr = 90 - atm_calcs.sea_corr

	def calc_amf_KY(self):
		atm_calcs.amf_KY = 1.0 / ( np.cos(np.deg2rad(atm_calcs.sza_corr)) + 0.50572 * (96.07995 - atm_calcs.sza_corr)**-1.6364)
