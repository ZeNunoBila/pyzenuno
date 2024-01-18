#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 08:41:44 2024

@author: nunop
"""

def getConfigurationFromFile(filepath):
	import configparser
	import sys
	import platform
	import os
	configuration=object()
	configurationFile=config_path
	configuration = configparser.ConfigParser(inline_comment_prefixes="%")
	configuration.optionxform=str
	configuration.read(configurationFile)

	#filter out the channels that have no corresponding section in the configuration
	#for (key, value) in configuration.items('channels'):
	#	 if not value in configuration:
	#		 configuration.remove_option('channels',key)
#except:
#	print("Error reading" , sys.exc_info()[0]);

#	finally:
	return(configuration)

def check_inp_file(index,
				   log_file='/bira-iasb/projects/planetary/nuno/ASIMUT_data/run_log.dat',
				   all_fields=True):
	
	import pandas as pd
	import os
	import configparser
	
	log = pd.read_csv(log_file,header=[0],index_col=[0])
	inp_file = os.path.join(log.iloc[index]['outdir'],'inp_file.inp')

	configuration=object()
	#configurationFile=inp_file
	configuration = configparser.ConfigParser(inline_comment_prefixes="%")
	configuration.optionxform=str
	configuration.read(inp_file)
	
	
	if  all_fields == True: # != True:
		fields = configuration
	else:
		fields = all_fields
		fields.insert(0,'0')
	
	print (inp_file)
		
		 
	for i,secs in enumerate(fields):
		if i > 0:
			try:
				print ('  %s' % secs)
				for ssecs in configuration[secs]:
					print ('    %s = %s' % (ssecs,configuration[secs][ssecs]))
			except:
				print ('    Field %s doesnt exist in inp file' % secs)
#	with open(inp_file) as f:	   
#		data = yaml.load(f, Loader=yaml.FullLoader)
#	print (data)
	#print (log.iloc[index]['tree'])
	
	#return inp




def load_asi_files(indexes=[0],
				   log_file='/bira-iasb/projects/planetary/nuno/ASIMUT_data/run_log.dat',
				   file_prefix='output',
				   spfen='SP1_FEN1',
				   kind='nc',
				   layer=1,
				   convert2lambda=True,
				   spec_redux=1):
	
	import pandas as pd
	import os
	import numpy as np
	
	'''
	typical dir contents:
		asi_file.asi
		inp_file.inp
		log_file.LOG
		output.out
		output_SP1_FEN1_od_Layer1.dat
		output_SP1_FEN1_od_Layer2.dat
		output_SP1_FEN1_radBT_forw.dat
		output_SP1_FEN1_rad_conv.dat
		output_SP1_FEN1_rad_forw.dat
		output_SP1_FEN1_radNC.dat
		output_SP1_FEN1_CvFct.dat
		
	args:
		kind: 'od','bt','co','rf','nc'
	'''
	if kind == 'od':
		layer = '%d' % layer
	else:
		layer = ''
	
	dic_fmt = {'od':'%s_%s_od_Layer%s.dat',
			'bt':'%s_%s_radBT_forw%s.dat',
			'co':'%s_%s_rad_conv%s.dat',
			'rf':'%s_%s_rad_forw%s.dat',
			'nc':'%s_%s_radNC%s.dat',
			'cf':'%s_%s_CvFct%s.dat'
			}
		
	log = pd.read_csv(log_file,header=[0],index_col=[0])
	
	dic_out = {}
	for ix in indexes:
		fn = dic_fmt[kind] % (file_prefix,spfen,layer)
		rf = os.path.join(log.iloc[ix]['outdir'],fn)
		# check data header: line that starts with %#
		fp = open(rf)
		hf,uf = False,False
		for i, line in enumerate(fp):
			if '%#' in line:				
				hf = True
				header = line[2:].split()
				header = [h.strip() for h in header]
			if '%@' in line:				
				uf = True
				units = line[2:].split()
				units = [h.strip() for h in units]
			if hf and uf:
				break				
		fp.close()
		

		##### load data	
		try:
			data = np.loadtxt(rf,delimiter='\t',comments='%')
		except:
			data = np.loadtxt(rf,comments='%')
		##### convert data
		if convert2lambda:
			for i in np.arange(1,data.shape[1]):
				data[:,i] = data[:,0]**2 * data[:,i]
			
			data[:,0] = 1e4/data[:,0]
			data = data[::spec_redux,:]
			data = np.flipud(data)
		
		##### prepare output
		keys = log.columns.tolist()
		keys.insert(0,'header')
		keys.insert(0,'units')
		keys.insert(0,'data')
		
		if not hf:
			header = ['col%d' % d for d in range(data.shape[1])]			
		if not uf:
			units = ['unit%d' % d for d in range(data.shape[1])]
		
		values = list(log.iloc[ix])
		values.insert(0,header)
		values.insert(0,units)
		values.insert(0,data)
		
		new_dic = {ix:dict(zip(keys,values))}
		dic_out.update(new_dic)
		
	return dic_out

		

