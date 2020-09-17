import copy
import numpy as np
import ds_format as ds
import aquarius_time as aq
from alcf import misc
from alcf.algorithms import interp

def couple(d, d_idx):
	n, m, l = d['backscatter'].shape
	d['backscatter_sd'] = np.full((n, m, l), np.nan, np.float64)
	d['.']['backscatter_sd'] = {
		'.dims': ['time', 'range', 'column'],
		'long_name': 'total_attenuated_backscatter_coefficient_standard_deviation',
		'units': 'm-1 sr-1',
	}
	for i in range(n):
		t = d['time'][i]
		j = np.argmin(np.abs(d_idx['time'] - t))
		n1 = d_idx['n'][j]
		filename = d_idx['filename'][n1]
		i1 = d_idx['i'][j]
		d1 = ds.read(filename, ['zfull', 'backscatter_sd'], {'time': i1})
		zhalf1 = misc.half(d1['zfull'])
		zhalf = misc.half(d['zfull'][i,:])
		b_sd = interp(zhalf1, d1['backscatter_sd'], zhalf)
		for k in range(l):
			d['backscatter_sd'][i,:,k] = b_sd

def stream(dd, state, dirname):
	if 'd_idx' not in state:
		d_idx = ds.readdir(dirname, ['time'], merge='time')
		state['d_idx'] = d_idx
	return misc.stream(dd, state, couple, d_idx=state['d_idx'])

