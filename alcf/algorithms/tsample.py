import copy
import numpy as np
from alcf import misc
import ds_format as ds
import aquarius_time as aq

def tsample(d, tres):
	w = d['time_bnds'][:,1] - d['time_bnds'][:,0]
	d['time_bnds'] = np.array([[
		np.amin(d['time_bnds'][:,0]),
		np.amax(d['time_bnds'][:,1])
	]])
	d['time'] = np.array(np.mean(d['time_bnds'], axis=1))
	if 'backscatter_sd' in d:
		n = d['backscatter_sd'].shape[0]
		shape1 = list(d['backscatter_sd'].shape[1:])
		d['backscatter_sd'] = np.sqrt(1./n*np.average(
			d['backscatter_sd']**2,
			axis=0,
			weights=w,
		))
		d['backscatter_sd'] = d['backscatter_sd'].reshape([1] + shape1)
	for var in ds.get_vars(d):
		if var in ('time', 'time_bnds', 'backscatter_sd'):
			continue
		if 'time' not in d['.'][var]['.dims']:
			continue
		i = d['.'][var]['.dims'].index('time')
		shape = list(d[var].shape)
		d[var] = np.average(d[var], axis=i, weights=w)
		shape[i] = 1
		d[var] = d[var].reshape(shape)

def stream(dd, state, tres=None, align=True, **options):
	if tres is not None:
		state['aggregate_state'] = state.get('aggregate_state', {})
		dd = misc.aggregate(dd, state['aggregate_state'], tres, align=align)
		return misc.stream(dd, state, tsample, tres=tres)
	return dd
