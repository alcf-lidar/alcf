import numpy as np
from alcf import misc

def noise_removal(d, **options):
	b = d['backscatter']
	zfull = d['zfull']
	bt = b[:,-1]
	n, m = b.shape
	b2 = np.zeros((n, m), np.float64)
	b_sd = np.zeros((n, m), np.float64)
	w = d['time_bnds'][:,1] - d['time_bnds'][:,0]
	noise_m = np.average(bt, weights=w)
	noise_sd = np.sqrt(np.cov(bt, aweights=w)) if len(bt) > 1 else 0.
	for i in range(n):
		c = (1.0*zfull[i,:]/zfull[i,-1])**2
		b2[i,:] = b[i,:] - noise_m*c
		b_sd[i,:] = noise_sd*c
	d['backscatter'] = b2
	d['backscatter_sd'] = b_sd
	d['.']['backscatter_sd'] = {
		'.dims': ['time', 'range'],
		'long_name': 'total attenuated volume backscattering coefficient standard deviation',
		'units': 'm-1 sr-1',
	}

def stream(dd, state, noise_removal_sampling=300, **options):
	state['aggregate_state'] = state.get('aggregate_state', {})
	dd = misc.aggregate(dd, state['aggregate_state'],
		noise_removal_sampling/60./60./24.
	)
	return misc.stream(dd, state, noise_removal, **options)
