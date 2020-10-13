import numpy as np
from alcf import misc

def lidar_ratio(d):
	dz = np.diff([0] + list(d['zfull']))
	if len(d['backscatter'].shape) == 3:
		n, m, l = d['backscatter'].shape
		bint = np.zeros((len(d['time']), l), dtype=np.float64)
		dims = ['time', 'column']
		for j in range(l):
			for i in range(len(d['time'])):
		 		bint[i,j] = np.sum(d['backscatter'][i,:,j]*dz)
	else:
		n, m = d['backscatter'].shape
		bint = np.zeros(n, dtype=np.float64)
		dims = ['time']
		for i in range(n):
		 	bint[i] = np.sum(d['backscatter'][i,:]*dz)
	d['lr'] = 1./(2.*bint) # See O'Connor et al. (2004), Equation 6.
	d['.']['lr'] = {
		'.dims': dims,
		'long_name': 'effective lidar ratio',
		'units': 'sr',
	}

def stream(dd, state, **options):
	return misc.stream(dd, state, lidar_ratio, **options)
