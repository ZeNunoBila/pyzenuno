
def pairwise(iterable):
	'''
	function that iterates over an iterator and its next element
	Example of usage:
	>> for (i1, row1), (i2, row2) in pairwise(df.iterrows()):
	>> bins = [[a,b] for a,b in pyzntools.pairwise(np.arange(440,675,9))]
	....
	'''
	from itertools import tee
	a, b = tee(iterable)
	next(b, None)
	return zip(a, b)
	
	
def dif_2_arrays(A,B):
	'''
	function that gives the minimum difference between 2 different size arrays
	returns: ix[0] -> index at array A
			 ix[1] -> index at array B
			 d_min -> minimal difference between A and B
	'''
	import numpy
	ix = []
	d_min = 0
	for i,a in enumerate(A):
		for j,b in enumerate(B):
			d = np.abs(a-b)
			if (i==0) & (j==0):
				d_min = d
				ix = [0,0]
			else:
				if d<d_min:
					d_min = d
					ix = [i,j]
					
	#print 'min = ', d_min, ' at a[',ix[0],'] b[',ix[1],']' 
	return ix,d_min
	
def intersection(a,b):
	'''
	function that works as matlab intersection
	[c, ia, ib] = intersect(A, B)
	'''
	import numpy as np
	a1, ia = np.unique(a, return_index=True)
	b1, ib = np.unique(b, return_index=True)
	
	aux = np.concatenate((a1, b1))
	aux.sort()
	c = aux[:-1][aux[1:] == aux[:-1]]
	return c, ia[np.in1d(a1, c)], ib[np.in1d(b1, c)]
	'''
	c = np.intersect1d(A, B)
	ma = np.setmember1d(A, B)
	ia = np.nonzero(ma)[0]

	mb = np.setmember1d(B, A)

	ib = np.nonzero(mb)[0]

	return c,ia,ib
	'''
	
def blocks(df,field,time_field):
	'''
	function that groups 'field' of dataframe into consecutive repeated values.
	Example of iteration of all blocks for a desired value G for the 'field' value, with a block length > N
	
	for b in np.arange(df['block'].min(),df['block'].max()+1):
		aa = np.argwhere((df['block']==b)&(df[field]==G)).flatten()
		if len(aa) > 10:
			BLOCK = df[field][aa]	
	'''	
	df['block'] = (df[field].shift(1) != df[field]).astype(int).cumsum()
	df.reset_index().groupby(['field','block'])[time_field].apply(np.array) 
	
	return df

def ASCII_sum(string):
	'''
	function that gives the sum of an ASCII string
	'''
	import numpy as np
	return np.frombuffer(string, "uint8").sum()
	
	
def find_nearest(array,value):
	'''
	function that gives the array index for the closest value
	'''
	import numpy as np
	idx = (np.abs(array-value)).argmin()
	return idx

	
def check_multi_elements(array):
	'''
	function that returns the elements that are repeated in a numpy array	
	'''
	import collections
	rep_items = [item for item, count in collections.Counter(array).items() if count > 1]
	reps = [count for item, count in collections.Counter(array).items() if count > 1]
	return rep_items,reps
	
def construct_gaussian(amp=1,mean=0,stddev=0.5):
	from astropy.modeling import models, fitting	
	g_model = models.Gaussian1D(amplitude=amp, mean=mean, stddev=stddev)
	return g_model
	
	
def splitall(path):
	# https://www.oreilly.com/library/view/python-cookbook/0596001673/ch04s16.html
	import os, sys

	allparts = []
	while 1:
		parts = os.path.split(path)
		if parts[0] == path:  # sentinel for absolute paths
			allparts.insert(0, parts[0])
			break
		elif parts[1] == path: # sentinel for relative paths
			allparts.insert(0, parts[1])
			break
		else:
			path = parts[0]
			allparts.insert(0, parts[1])
	return allparts
	
	