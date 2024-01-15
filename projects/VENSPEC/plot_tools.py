def setup_plot_signal_SNR(ax, param):
	from functools import partial
	import grating_functions as grating
	import radiometry_tools as rad
	def forward(signal, pars):
		return rad.signal2SNR_shotOnly(signal,pars) #,pars['it'])

	def inv(snr, pars):		
		return rad.SNR2signal_shotOnly(snr,pars) #,pars['it'])
        

	return ax.secondary_yaxis("right", functions=(partial(forward, pars=param),partial(inv, pars=param)))


def setup_plot_rad_wn_wl(ax, param):
	from functools import partial
	import grating_functions as grating
	import radiometry_tools as rad
	def forward(p, m):

		return m**2 * p
	

	def inv(p, m):		
		return p/m**2
        

	return ax.secondary_yaxis("right", functions=(partial(forward, m=param),partial(inv, m=param)))

def setup_plot_wl(ax, param):
	from functools import partial
	import grating_functions as grating
	import radiometry_tools as rad
	def forward(p, m):

		return grating.p2wl(p,m)
	

	def inv(wl, m):		
		return grating.wl2p(wl,m)
        

	return ax.secondary_xaxis("top", functions=(partial(forward, m=param),partial(inv, m=param)))



def setup_plot_wn(ax, param):
	from functools import partial
	import grating_functions as grating
	def forward(p, m):
		return grating.p2wn(p,m)
	

	def inv(wl, m):		
		return grating.wn2p(wl,m)
        

	return ax.secondary_xaxis("top", functions=(partial(forward, m=param),partial(inv, m=param)))