import copy
import numpy as np
from alcf import misc
import ds_format as ds
import aquarius_time as aq

def tsample(d, tres):
	n = d['backscatter'].shape[0]
	m = d['backscatter'].shape[1]
	d['backscatter'] = np.mean(d['backscatter'], axis=0, keepdims=True)
	if 'backscatter_sd' in d:
		d['backscatter_sd'] = np.sqrt(1./n*np.mean(d['backscatter_sd']**2, axis=0, keepdims=True))
	d['time'] = np.array(np.mean(d['time'], keepdims=True))

def stream(dd, state, tres=None, tlim=None, **options):
	if tres is not None:
		state['aggregate_state'] = state.get('aggregate_state', {})
		dd = misc.aggregate(dd, state['aggregate_state'], tres)
		return misc.stream(dd, state, tsample, tres=tres)
	return dd
