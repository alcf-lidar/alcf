import numpy as np
from alcf import misc
import ds_format as ds

def tsampling(d, tres=None, tlim=None):
	d['backscatter'] = np.mean(d['backscatter'], axis=0, keepdims=True)
	if 'backscatter_sd' in d:
		d['backscatter_sd'] = np.mean(d['backscatter_sd'], axis=0, keepdims=True)
	d['time'] = np.array(np.mean(d['time'], keepdims=True))

def stream(dd, state, tres=None, tlim=None, **options):
	if tres is not None:
		state['aggregate_state'] = state.get('aggregate_state', {})
		dd = misc.aggregate(dd, state['aggregate_state'], tres)
		return misc.stream(dd, state, tsampling)
	return dd
