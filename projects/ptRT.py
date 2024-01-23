#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 10:44:19 2024

@author: nunop
"""

from petitRADTRANS import Radtrans
from petitRADTRANS import nat_cst as nc
import numpy as np
import pickle
import os
from datetime import datetime
from pyzenuno.utils.file_IO import write_text_file
import pyzenuno.utils.time_manips as time_manips
import pandas as pd

def convert_data(atmosphere):
	
	# c is in erg: cm.s-1
	atmosphere.wl_m = nc.c / atmosphere.freq * 1e-2
	atmosphere.wl_um = nc.c / atmosphere.freq * 1e4
	atmosphere.wl_nm = nc.c / atmosphere.freq * 1e7	   
		
	atmosphere.flux_Wmu = nc.c/atmosphere.wl_m**2 * atmosphere.flux * 1e-7 * 1e4 * 1e-6 * 1/(np.pi)
	
	return atmosphere



def load(indexes,
		 out_base_dir = '/home/nunop/data/ptrt/',
		 kind='dic'):
	
	log_file = os.path.join(out_base_dir,'ptRT.log')

	log = pd.read_csv(log_file,header=[0],index_col=[0])
	
	dic_out = {}
	for ix in indexes:
		fn = 'atmosphere_ptRT.' + kind
		rf = os.path.join(log.iloc[ix]['outdir'],fn)
		# check data header: line that starts with %#
		file = open(rf, 'rb')
		obj = pickle.load(file)
		file.close()			   
		if kind=='dic':
			data = np.array([obj['wl_um'],obj['flux_Wmu']]).transpose()
		
		
		##### prepare output
		keys = log.columns.tolist()
		keys.insert(0,'data')		
	
		values = list(log.iloc[ix])
		values.insert(0,data)
		
		new_dic = {ix:dict(zip(keys,values))}
		dic_out.update(new_dic)	
	return dic_out


 
	
def save(atmosphere,
				  outdir = '/home/nunop/data/ptrt/',
				  tree = [],
				  comments = []):	 
	
	
	suf = time_manips.tObj2Nicedate()
	suf_short = suf[2:8]
	suf_pattern = '_' + suf
	run_log_name = 'ptRT.log'
	
	# convert data
	atmosphere = convert_data(atmosphere)
	
	# prepare an output dictionary
	dic = {}
	
	for v in vars(atmosphere):
		dic[v] = eval('atmosphere.%s' % v)
		
		
		
	# create directories
	outdir_full = os.path.join(outdir,*tree)
	if os.path.exists(outdir_full):
		print (outdir_full + ' already exists.')
		ow = input('Overwrite [y or n] ?\n')
		if ow == 'n':
			raise ValueError('Exiting')
	else:	
		outdir_full = outdir		 
		for sd in tree:
			outdir_full = os.path.join(outdir_full,sd)
			if not os.path.exists(outdir_full):
				os.mkdir(outdir_full)
	
	# save files
	# 1 ptRT atmosphere object
	fn = os.path.join(outdir_full,'atmosphere_ptRT.obj')
	file = open(fn, 'wb')
	pickle.dump(atmosphere, file)		
	file.close()
	
	# 2 ptRT atmosphere dictionary
	fn = os.path.join(outdir_full,'atmosphere_ptRT.dic')
	file = open(fn, 'wb')
	pickle.dump(dic, file)		
	file.close()
	
	# 3 comments file
	fn = os.path.join(outdir_full,'atmosphere_ptRT.log')	
	now = datetime.now()   
	dt_string = now.strftime("%d/%m/%Y %H:%M:%S")		 
	write_text_file(fn, comments,  dt_string)
	
	
	
	# write log file	
	run_log_file = os.path.join(outdir,run_log_name)
	cols = ['id','timestamp','tree','comment','outdir']
	tree = '/'.join(tree)
	data = [0,suf,tree,(';').join(comments),outdir_full]
	
	if os.path.exists(run_log_file):
		log = pd.read_csv(run_log_file,header=[0])
		if not tree in log['tree'].values:
			data[0] = np.max(log.index) + 1
			log = log._append(pd.DataFrame(data=np.array(data).reshape((1,len(cols))),columns=cols))
		else:
			data[0] = log[log['tree'] == tree]['id'].values[0]
			log[log['tree'] == tree] = data

	else:
			log = pd.DataFrame(data=np.array(data).reshape((1,len(cols))),columns=cols)

	log.to_csv(run_log_file,index=False)

		
		
	
	


#import types


#def convert

#type(atmosphere.calc_flux) == types.MethodType

#dic_out = {}

#for i,v in enumerate(vars(atmosphere)):
 #	 print (i,v)
#	 ts = eval('atmosphere.%s' % v)
	
	#if type(eval(ts)) == types.MethodType:
	#	 print (v)
#	 print (type(ts))
	
#print ('====')

#for i,v in enumerate(dir(atmosphere)):
#	 print (i,v)
#	 ts = eval('atmosphere.%s' % v)
	
	#if type(eval(ts)) == types.MethodType:
#	 print (type(ts))
	