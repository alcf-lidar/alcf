import numpy as np
from alcf import misc

def lidar_ratio(d, eta=1.):
	dz = np.diff([0] + list(d['zfull']))
	if len(d['backscatter'].shape) == 3:
		n, m, l = d['backscatter'].shape
		lr = np.zeros((len(d['time']), l), dtype=np.float64)
		dims = ['time', 'column']
		for j in range(l):
			for i in range(len(d['time'])):
		 		lr[i,j] = np.sum(d['backscatter'][i,:,j]*dz)
	else:
		n, m = d['backscatter'].shape
		lr = np.zeros(n, dtype=np.float64)
		dims = ['time']
		for i in range(n):
		 	lr[i] = np.sum(d['backscatter'][i,:]*dz)
	lr = 2.*eta/lr
	d['lr'] = lr
	d['.']['lr'] = {
		'.dims': dims,
		'long_name': 'lidar_ratio',
		'units': 'sr',
	}

def stream(dd, state, **options):
	return misc.stream(dd, state, lidar_ratio, **options)
