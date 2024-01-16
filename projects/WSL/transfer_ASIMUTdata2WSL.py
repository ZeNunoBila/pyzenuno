#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 13:57:09 2024

@author: nunop
"""


if __name__ == "__main__":

	import os
	import datetime
	import sys
	sys.path.append('/bira-iasb/projects/planetary/nuno/python_functions/')
	import shutil	
	import glob
	import argparse
	import pandas as pd
	import numpy as np
	
	
		
	parser = argparse.ArgumentParser()
	parser.add_argument('indexes',action='store',nargs='*')
	parser.add_argument('-kind',action='store',default=['nc'],nargs='*')
	parser.add_argument('-log',action='store',default='0')
	parser.add_argument('-print_log',action='store',default='0')
	parser.add_argument('-file_prefix',action='store',default='output')
	parser.add_argument('-spfen',action='store',default='SP1_FEN1')
	parser.add_argument('-layer',action='store',default='1')
	
	args = parser.parse_args()
	kind = args.kind
	args.layer = int(args.layer)

	
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
		
	args:
		kind: 'od','bt','co','rf','nc'
	'''

	dic_fmt = {'od':'%s_%s_od_Layer%s.dat',
		'bt':'%s_%s_radBT_forw%s.dat',
		'co':'%s_%s_rad_conv%s.dat',
		'rf':'%s_%s_rad_forw%s.dat',
		'nc':'%s_%s_radNC%s.dat'
		}
	
	
	# directories definition
	asi_rem_dir = '/home/nunop/projects/planetary/nuno/ASIMUT_data/'
	asi_rem_out_dir = os.path.join(asi_rem_dir,'OUTPUT')
	asi_rem_log = os.path.join(asi_rem_dir,'run_log.dat')
	
	asi_loc_dir = '/home/nunop/data/ASIMUT_data/'
	asi_loc_out_dir = os.path.join(asi_loc_dir,'OUTPUT')
	asi_loc_log = os.path.join(asi_loc_dir,'run_log.dat')

	# try to load new log file
	if args.log=='1':
		try:
			cmd = "scp nunop@hera.oma.be:" + asi_rem_log + " " + asi_loc_log
			os.system(cmd)
			log = pd.read_csv(asi_loc_log)
			print (log[['id','timestamp','tree','comment']])
		except:
			print('>> Not possible to download or read log file')
			
	# try to print log file
	if args.print_log=='1':
		try:
			log = pd.read_csv(asi_loc_log)
			print (log[['id','timestamp','tree','comment']])
		except:
			print('>> Not possible to download or read log file')
			
	# https://stackoverflow.com/questions/16886179/scp-or-sftp-copy-multiple-files-with-single-command
	#scp -T username@ip.of.server.copyfrom:"file1.txt file2.txt" "~/yourpathtocopy"
	# scp user@remote:'/path1/file1 /path2/file2 /path3/file3' /localPath
	print (args.indexes)
	indexes = [int(a) for a in args.indexes]
	if len(indexes) > 0:
		try:
			log = pd.read_csv(asi_loc_log)
			print ('>> indexes to copy:')
			print (log[['id','timestamp','tree','comment']].iloc[indexes])
		except:
			print('>> Not possible to download or read log file')

		try:			
			cmd = 'scp -T -r nunop@hera.oma.be:"'
			for i in indexes:
				outdir = asi_loc_out_dir
				for t in log.iloc[i]['tree'].split('/'):
					print (t)
					outdir = os.path.join(outdir,t)
					if not os.path.exists(outdir):
						os.mkdir(outdir)
					
				if i in log.index:
					for k in kind:
						if k == 'od':
							layer = '%d' % args.layer
						else:
							layer = ''
	
						fn = dic_fmt[k] % (args.file_prefix,args.spfen,layer)
						cmd += '%s ' % os.path.join(log.iloc[i]['outdir'],fn)
						
			cmd += '" '
			cmd += '"%s"' % outdir
			print (cmd)
			os.system(cmd)
		except:
			print ('>> Error in reading/copying')
		


	

