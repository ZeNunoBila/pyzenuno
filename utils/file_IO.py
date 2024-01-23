#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 13:48:06 2024

@author: nunop
"""

def write_data_file(fn, data, fmt, header):
	import os
	fileEmpty = not os.path.exists(fn)
	fmt += '\n'
	if fileEmpty:
		fid = open(fn, 'a+')	  
		fid.writelines(header + '\n')		
		fid.writelines(fmt % tuple(data))		
		fid.close()
	else:
		fid = open(fn, 'a+')
		fid.writelines(fmt % tuple(data))		
		fid.close()
		
		
def write_text_file(fn, text,  header,fmt='%s'):
	import os
	fileEmpty = not os.path.exists(fn)	
	fmt += '\n'
	fid = open(fn, 'w+')
	fid.writelines(header + '\n')
	for txt in text:
		fid.writelines(fmt % txt)
	fid.close()