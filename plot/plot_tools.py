def secondary_axis(ax,conversion_factor,position='top'):
	import matplotlib.pyplot as plt
	
	def first2sec(x):
		print (x*conversion_factor)
		return x * conversion_factor

	def sec2first(x):
		print (x/conversion_factor)

		return x / conversion_factor
		
		
	if (position == 'top') or (position == 'bottom'):
		return ax.secondary_xaxis(position, functions=(first2sec, sec2first))
	if (position =='left') or (position == 'right'):
		return ax.secondary_yaxis(position, functions=(first2sec, sec2first))
		
		




def my_formatter_fun(x, p):
    """ Own formatting function """
	# usage:
	# ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(plot_tools.my_formatter_fun))
    import numpy as np
    return r"$10^{%d}$" % np.log10(x)  #  raw string to avoid "\\"


def neg_exp(ax,axis='x'):
	if axis == 'x':
		labels = ax.get_xticklabels()
		ticks = ax.get_xticks()
	elif axis == 'y':
		labels = ax.get_yticklabels()
		ticks = ax.get_yticks()

	try:
	
		for l in labels:
			l.set_text(l.get_text().replace('\\mathdefault',''))
	
	except:
	
	# https://stackoverflow.com/questions/63723514/userwarning-fixedformatter-should-only-be-used-together-with-fixedlocator

	if axis == 'x':
		ax.set_xticks(ticks)
		ax.set_xticklabels(labels)
		
	elif axis == 'y':
		ax.set_yticks(ticks)
		ax.set_yticklabels(labels)



def join_legends(ax1,ax2):
	handles1,labels1 = ax1.get_legend_handles_labels()
	handles2,labels2 = ax2.get_legend_handles_labels()
	handles = handles1 + handles2
	labels = labels1 + labels2
	return handles, labels
	
	
	


def load_custom_font(font='hershey',fonts_dir='/home/nunop/fonts/'):
	import matplotlib.font_manager as font_manager
	import matplotlib as mpl
	import os
	font_dir = os.path.join(fonts_dir,dic_fonts[font]['dirf'])
	
	dic_fonts = {'hershey':{'dirf':'AVHershey','name':'AVHershey Simplex'},\
			 'msyi':{'dirf':'msyi','name':'Microsoft Yi Baiti'},\
			 'dina':{'dirf':'dina','name':'Dina ttf 10px'},\
			 'terminus':{'dirf':'Terminus (TTF)','name':'terminus-ttf-4.49.2'}
			 }

	for found_font in font_manager.findSystemFonts(fontpaths=font_dir, fontext='ttf'):
		#print (font)
		font_manager.fontManager.addfont(found_font)
		
	#import matplotlib.font_manager as fm
	#for f in fm.fontManager.ttflist:
	#	print(f.name)
   
   
   #print ('===============')	
   #for f in fm.fontManager.afmlist:
   #print(f.name)
	
	mpl.rcParams['font.family'] = dic_fonts[font]['name']
	mpl.rcParams['text.usetex'] = False # necessary so that latex font dont overwrite everything else on the plot
	mpl.rcParams['mathtext.fontset'] = 'custom'
	mpl.rcParams['mathtext.bf']=dic_fonts[font]['name']
	mpl.rcParams['mathtext.cal']=dic_fonts[font]['name']
	mpl.rcParams['mathtext.it']=dic_fonts[font]['name']
	mpl.rcParams['mathtext.rm']=dic_fonts[font]['name']
	mpl.rcParams['mathtext.sf']=dic_fonts[font]['name']
	mpl.rcParams['mathtext.tt']=dic_fonts[font]['name']

	
	# https://stackoverflow.com/questions/58361594/matplotlib-glyph-8722-missing-from-current-font-despite-being-in-font-manager
	
	mpl.rc('axes', unicode_minus=False)
	mpl.rcParams['mathtext.fallback'] = 'cm'
	
	
