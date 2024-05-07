import copy
import numpy as np
import ds_format as ds
import aquarius_time as aq
from alcf import misc, algorithms

VARIABLES = [
	'zfull',
	'backscatter_sd',
	'backscatter_mol',
]

def couple(d, d_idx, interp=None):
	dims = d['backscatter'].shape
	n = dims[0]
	l = dims[2] if len(dims) == 3 else 0
	couple_bsd = False
	couple_bmol = False
	if 'backscatter_sd' not in d:
		couple_bsd = True
		d['backscatter_sd'] = np.full(dims, np.nan, np.float64)
		d['.']['backscatter_sd'] = {
			'.dims': ['time', 'level', 'column'] \
				if len(dims) == 3 \
				else ['time', 'level'],
			'long_name': 'total_attenuated_backscatter_coefficient_standard_deviation',
			'units': 'm-1 sr-1',
		}
	if 'backscatter_mol' not in d:
		couple_bmol = True
		d['backscatter_mol'] = np.full(dims, np.nan, np.float64)
		d['.']['backscatter_mol'] = {
			'.dims': ['time', 'level'],
			'long_name': 'total_attenuated_molecular_backscatter_coefficient',
			'units': 'm-1 sr-1',
		}
	for i in range(n):
		t = d['time'][i]
		j = np.argmin(np.abs(d_idx['time'] - t))
		n1 = d_idx['n'][j]
		filename = d_idx['filename'][n1]
		i1 = d_idx['i'][j]
		d1 = ds.read(filename, VARIABLES, {'time': i1})
		zhalf1 = misc.half(d1['zfull'])
		zhalf = misc.half(d['zfull'][i,:]) \
			if d['zfull'].ndim == 2 \
			else misc.half(d['zfull'])
		if couple_bsd and 'backscatter_sd' in d1:
			b_sd = algorithms.interp(
				interp,
				d1['zfull'], zhalf1,
				d1['backscatter_sd'],
				d['zfull'][i,:], zhalf
			)
			if len(dims) == 3:
				for k in range(l):
					d['backscatter_sd'][i,:,k] = b_sd
			else:
				d['backscatter_sd'][i,:] = b_sd
		if couple_bmol and 'backscatter_mol' in d1:
			b_mol = algorithms.interp(
				interp,
				d1['zfull'], zhalf1,
				d1['backscatter_mol'],
				d['zfull'][i,:], zhalf
			)
			d['backscatter_mol'][i,:] = b_mol

def stream(dd, state, dirname, interp=None):
	if 'd_idx' not in state:
		d_idx = ds.readdir(dirname, ['time'], merge='time')
		state['d_idx'] = d_idx
	return misc.stream(dd, state, couple, d_idx=state['d_idx'], interp=interp)

