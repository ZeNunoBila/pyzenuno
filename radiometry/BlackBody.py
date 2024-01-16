#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 31 10:44:58 2023

@author: nunop
"""


from pyzenuno.constants import *
import numpy as np
	
def BB_Radiance_wavelength(T,wl,c=c,h=h,k=k):
    # Boyd eq 4.12
    # Table 1
    # wl input in nanometers

	wl = wl*1e-9 # convert wl into meters
	L = 2*h*c**2/wl**5 * 1/(np.exp(h*c/(wl*k*T))-1) 

	# units = J . s . (m.s-1)2 . m-5 .srad-1 = J . s-1 . m-3 . srad -1 = W . m-3 .srad-1    	

	return L

def BB_Radiance_wavenumber(T,wn,c=c,h=h,k=k):
	wn = wn*1e2
	L = 2*h*c**2*wn**3 * 1/(np.exp(h*c*wn/(k*T))-1) 
	# units = J . s . (m.s-1)2 . (cm-1)-3 .srad-1 = J . s-1 . m-2 . cm-3 . srad-1
	
	return L

def BB_Radiance_frequency(T,f,c=c,h=h,k=k):
	#wl = wl*1e-9 # convert wl into meters		
	#print (c)
	#print (h)
	#print (k)
	L = 2*h*f**3/c**2 * 1/(np.exp(h*f/(k*T))-1)
	# units = J . s . (s-1)3 . (m-1.s)2 . srad-1 = J .
	return L


def BB_NumberPhotons(T,wl,c=c,h=h,k=k):
	photons = 2*c/wl**4 * 1/(np.exp(h*c/(wl*k*T))-1) # units = s-1 . m-3 . srad-1
	return photons

