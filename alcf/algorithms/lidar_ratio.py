import numpy as np
from alcf import misc

def lidar_ratio(d, eta=1.):
	lr = np.zeros(len(d['time']))
	for i in range(len(d['time'])):
	 	lr[i] = np.sum(d['backscatter'][i,:]*np.diff([0] + list(d['zfull'])))
	lr = 2.*eta/lr
	d['lr'] = lr
	d['.']['lr'] = {
		'.dims': ['time'],
		'long_name': 'lidar_ratio',
		'units': 'sr',
	}

def stream(dd, state, **options):
	return misc.stream(dd, state, lidar_ratio, **options)
