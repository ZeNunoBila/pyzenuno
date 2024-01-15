# -*- coding: utf-8 -*-
"""
atmospheric generic calculations
"""


def eryth_func(wl_grid):
	import numpy as np
	bins = [250,298,328,400,10000]
	erf = [lambda x: 1, lambda x: 10**(0.094*(298-x)), lambda x: 10**(0.015*(139-x)),lambda x:0]
	er = []
	for w,d in zip(wl_grid, np.digitize(wl_grid,bins)):
		er.append(erf[d-1](w))
		
	return np.array(er)
	

def sza(amf):
	import numpy as np
	''' 
	gives approximate sza in degrees as as function of amf
	'''
	sza = np.rad2deg(np.arccos(1./amf*1.0))
	return sza
	
def amf_KY(sza):
	import numpy as np
	'''
	gives amf as a function of sza (degrees)
	'''
	amf = 1.0 / ( np.cos(np.deg2rad(sza)) + 0.50572 * (96.07995 - sza)**-1.6364)
	return amf
	
	

def pressure_height(altitude):
	# altitude in meters
	# pressure in mbar
	press = 100 * ((44331.514 - altitude) / 11880.516) ** (1 / 0.1902632)
	return press*0.01
	
	
def US_std_atm(h_grid,var='T(K)'):
	'''
	table from: https://www.digitaldutch.com/atmoscalc/table.htm
	h_grid: geometric altitude grid to retrieve
	var: quantity to be retrieved: nO3(m-3)	T(K)	Pressure(Pa)	Density(kg/m3)	Speed of sound(m/s)	Viscosity(Pa.s)
	'''
	import pandas as pd
	import numpy as np
	data_file = 'C:/Users/nunop/AppData/Local/Continuum/Anaconda2/Lib/site-packages/pyzenuno/data/US_std_atm.csv'
	std_atm = pd.read_csv(data_file)
	if np.isscalar(h_grid):
		h_grid = std_atm['Z(km)']
		ret = std_atm[var]
	else:
		ret = np.interp(h_grid,std_atm['Z(km)'],std_atm[var])
	return h_grid,ret
	
def refractive_index_std_atm(T,P,wavelength):
	'''
	http://www.kayelaby.npl.co.uk/general_physics/2_5/2_5_7.html
	T in Celsius
	P in Pascal
	wavelength in nanometers
	'''
	# (ns-1) for standard air
	sigma = 1.0/(wavelength/1000.0)
	ns = (8342.54 + 2406147*(130-sigma**2)**-1 + 15998*(38.9 - sigma**2)**-1)/10**8 + 1
	ntp = (ns-1) * P*(1+P*(60.1-0.972*T)*10**-10)/(96095.43*(1+0.003661*T)) + 1	
	return ntp
	
	
def atm_ref_NOAA(elevation):
	'''
	gives atmospheric refraction calculated by NOAA as a function of elevation angle in degrees
	returns refraction in arcsec
	'''
	import numpy as np
	if elevation > 85:
		ref = 0;
	else:
		if elevation > 5:
			ref = 58.1 / np.tan((np.pi / 180) * (elevation)) - 0.07 / np.tan((np.pi / 180) * (elevation)) ** 3 + 0.000086 / np.tan((np.pi / 180) * (elevation)) ** 5
		else:
			if elevation > -0.575:
				ref = 1735 + elevation * (-518.2 + elevation * (103.4 + elevation * (-12.79 + elevation * 0.711)))
			else:
				ref = -20.772 / np.tan((np.pi / 180) * (elevation));
	
	ref = ref / 3600
	return ref
	
def atm_ref_Bennett(elevation):
	'''
	from :
	Bennett, G.G. (1982). "The Calculation of Astronomical Refraction in Marine Navigation"
	elevation in degrees
	returns refraction in arcsec
	'''
	import numpy as np
	R = 1/np.tan(np.deg2rad(elevation+7.31/(elevation+4.4)))
	dR = -0.06 * np.sin(np.deg2rad(14.7*R+13))
	R = R + dR
	return R/60.0
	
def ray_MLO(w):
    # bodhaine et al 1999 eq 31
    tr = 0.0014484*((1.0455996 - 341.29061*w**-2 - 0.90230850*w**2)/(1+0.0027059889*w**-2 - 85.968563*w**2))
    return tr

def ray_IZO(w,p=776):
    # bodhaine et al 1999 eq 13    
    #p0 = 1013.25
    #tr = p/p0**0.00877*w**(-4.05)
    # bodhaine et al 1999 eq 16
    z = 2.3
    tr = 0.0088*w**(-4.15+0.2*w)*np.exp(-0.1188*z-0.00116*z**2)
	
