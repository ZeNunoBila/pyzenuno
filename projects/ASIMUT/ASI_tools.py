#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 13:58:22 2023

@author: nunop
"""

'''
[Run]
verbose= 3
save= Radiance, RadianceForward, RadNoConv, FullRadConv 
SaveResults= ascii
ConvolutionMethod= 1

[RadiativeCode]
Code = Lidortf90_v3p7

[Directories]
dirAtmosphere=	/bira-iasb/projects/planetary/Asimut/CommonData/Atmosphere/Venus/
dirSolar=	/bira-iasb/projects/planetary/Asimut/CommonData/Solar/
dirAerosol =  /bira-iasb/projects/planetary/Asimut/CommonData/Aerosols/Venus/20221202_LidortG_TUDelft/
dirlidort =  /bira-iasb/projects/planetary/Asimut/CommonData/Aerosols/Venus/
dirInput = 	/bira-iasb/projects/planetary/nuno/envision/input/
dirInstrument = /bira-iasb/projects/planetary/nuno/envision/instrument/
dirLUT = /bira-iasb/projects/planetary/Asimut/CommonData/Spectroscopy/LUT/Venus/
dirLP = /bira-iasb/projects/EnVision/SCIENCE/Auxiliary_Files/Spectroscopy/
dirSAVE = /bira-iasb/projects/planetary/nuno/envision/SAVE/
dirRESULTS = /bira-iasb/projects/planetary/nuno/envision/RESULTS/

[List]
Venus_first_test_AllMolecules_band1_NightSide_LP_FilterNunoTmaxMod0.inp
'''

import os
'''
dic_default_params_V0 = {'Run':
							 {'verbose':'3',
							 'save':'Radiance, RadianceForward, RadNoConv, FullRadConv',
							 'SaveResults':'ascii',
						    'ConvolutionMethod':'1'},
					  'Radiative_code':
						  {'Code':'Lidortf90_v3p7'},
					  'Directories':
						  {'dirAtmosphere':'/bira-iasb/projects/planetary/Asimut/CommonData/Atmosphere/Venus/',
		 				  'dirSolar':'/bira-iasb/projects/planetary/Asimut/CommonData/Solar/',
		           		 'dirAerosol':'/bira-iasb/projects/planetary/Asimut/CommonData/Aerosols/Venus/20221202_LidortG_TUDelft/',
						 'dirlidort':'bira-iasb/projects/planetary/Asimut/CommonData/Aerosols/Venus/',
						 'dirInput':'/bira-iasb/projects/planetary/nuno/envision/input/',
						'dirInstrument':'/bira-iasb/projects/planetary/nuno/envision/INS/',
						 'dirLUT':'/bira-iasb/projects/planetary/Asimut/CommonData/Spectroscopy/LUT/Venus/',
						 'dirLP':'/bira-iasb/projects/EnVision/SCIENCE/Auxiliary_Files/Spectroscopy/',
						 'dirSAVE':'/bira-iasb/projects/planetary/nuno/envision/SAVE/',
						 'dirRESULTS':'/bira-iasb/projects/planetary/nuno/envision/RESULTS/'}						  
							  }

envision_root = '/bira-iasb/projects/planetary/nuno/envision/'
'''

#%%
def create_asi_V0(inp_files,asi_file,asi_default_params_version='V0',\
				  asi_output_dir='/bira-iasb/projects/planetary/nuno/envision/ASI/',\
			   sub_dir_output=True,sub_dir_applies=['dirSAVE','dirRESULTS','dirDATA'],\
				   **kwargs):
	import os
	import utils

	# load asi template	
	asi_template_dir = '/bira-iasb/projects/planetary/nuno/envision/asi_templates/'
	asi_template_fn = 'asi_template_%s.ini' % asi_default_params_version
	conf = utils.getConfigurationFromFile(os.path.join(asi_template_dir,asi_template_fn))
	dict_conf = {s:dict(conf.items(s)) for s in conf.sections()}	 
	
	# asi output file
	asi_output = os.path.join(asi_output_dir,asi_file + '.asi')
	print (asi_output)
	f = open(asi_output, 'w+')
	
	for k,v in dict_conf.items():
		f.write('[%s]\n' % k)
		if isinstance(v, dict):
			for kk,vv in v.items():				
				#print (kk,vv)
				if kk in sub_dir_applies:
					print ('kk')
					vn = os.path.join(vv , asi_file)
					vn += '/'
					print (vv)
				else:
					vn = vv
				f.write('%s = %s\n' % (kk,vn))	

		f.write('\n')
	
	#f.write('\n')
	f.write('[List]\n')
	for inp in inp_files:
		f.write(inp + '.inp\n')
	
	f.close()
		
	return dict_conf


dc = create_asi_V0(['aa','bb'],'test_asi2')
