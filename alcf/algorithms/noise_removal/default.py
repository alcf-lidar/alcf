import numpy as np
from alcf import misc

def noise_removal(d, **options):
	b = d['backscatter']
	z = d['zfull']
	bt = b[:,-1]
	zt = z[-1]
	n, m = b.shape
	b2 = np.zeros((n, m), np.float64)
	b_sd = np.zeros((n, m), np.float64)
	c = (1.0*z/zt)**2
	noise_m = np.mean(bt)
	noise_sd = np.std(bt)
	b_sd0 = noise_sd*c
	for i in range(n):
		b2[i] = b[i] - noise_m*c
		b_sd[i] = b_sd0
	d['backscatter'] = b2
	d['backscatter_sd'] = b_sd
	d['.']['backscatter_sd'] = {
		'.dims': ['time', 'range'],
		'long_name': 'backscatter_standard_deviation',
		'units': 'm-1 sr-1',
	}

def stream(dd, state, noise_removal_sampling=300, **options):
	state['aggregate_state'] = state.get('aggregate_state', {})
	dd = misc.aggregate(dd, state['aggregate_state'],
		noise_removal_sampling/60./60./24.
	)
	return misc.stream(dd, state, noise_removal, **options)
