#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 08:41:29 2024

@author: nunop
"""


def gauss_fwhm(x,fwhm,mean=0.0,amp=False):
	import numpy as np
	'''
	Parameters
	----------
	x : 1-D numpy array of floats
		The grid where to define the gaussian
	fwhm : float
		FWHM of the Gaussian. FWHM = 2.sqrt(2 ln 2) stdev ~ 2.35482 stdev
	mean : float, optional
		The default is 0.0.
	amp : boolean (False) or float, optional
		The default is False. If default the amplitude is set to 1/(stdev.sqrt(2.pi))
		If float, the amplitude is defined by user

	Returns
	-------
	g : numpy array of floats
		The Gaussian curve with the same shape of x

	'''
	stdev = fwhm / (2*np.sqrt(2*np.log(2)*2))
	
	if not amp:
		amp = 1 / (stdev * np.sqrt(2*np.pi))
		
	g = amp * np.exp(-(x-mean)**2/(2*stdev**2))
	
	return g