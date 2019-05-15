import numpy as np

def stats_map(d, state, tlim=None, blim=None, bres=None, **kwargs):
	state['zfull'] = state.get('zfull', d['zfull'])
	state['n'] = state.get('n', 0)
	state['backscatter_half'] = state.get('backscatter_half',
		np.arange(blim[0], blim[1] + bres, bres)
	)
	state['backscatter_full'] = state.get('backscatter_full',
		0.5*(state['backscatter_half'][1:] + state['backscatter_half'][:-1])
	)
	o = len(state['backscatter_full'])
	if len(d['cloud_mask'].shape) == 3:
		n, m, l = d['cloud_mask'].shape
		dims = (m, l)
		hist_dims = (o, m, l)
	else:
		n, m = d['cloud_mask'].shape
		l = 0
		dims = (m,)
		hist_dims = (o, m)
	state['cloud_occurrence'] = state.get(
		'cloud_occurrence',
		np.zeros(dims, dtype=np.float64)
	)
	state['backscatter_hist'] = state.get(
		'backscatter_hist',
		np.zeros(hist_dims, dtype=np.float64)
	)
	if tlim is not None:
		mask = (d['time'] >= tlim[0]) & (d['time'] < tlim[1])
	else:
		mask = np.ones(n, dtype=np.bool)
	if not np.any(mask):
		return
	for j in range(m):
		if l > 0:
			for k in range(l):
				state['backscatter_hist'][:,j,k] += np.histogram(
					d['backscatter'][:,j,k], bins=state['backscatter_half'])[0]
		else:
			state['backscatter_hist'][:,j] += np.histogram(
				d['backscatter'][:,j], bins=state['backscatter_half'])[0]
	for i in range(n):
		if not mask[i]:
			continue
		if l > 0:
			state['cloud_occurrence'][:,:] += d['cloud_mask'][i,:,:]
		else:
			state['cloud_occurrence'][:] += d['cloud_mask'][i,:]
		state['n'] += 1

def stats_reduce(state, **kwargs):
	if state['n'] != 0:
		state['backscatter_hist'] /= state['n']
	return {
		'cloud_occurrence': 100.*state['cloud_occurrence']/state['n'],
		'zfull': state['zfull'],
		'n': state['n'],
		'backscatter_full': state['backscatter_full'],
		'backscatter_hist': state['backscatter_hist'],
		'.': {
			'zfull': {
				'.dims': ['zfull'],
				'standard_name': 'height_above_reference_ellipsoid',
				'units': 'm',
			},
			'cloud_occurrence': {
				'.dims': ['zfull', 'column'] \
					if len(state['cloud_occurrence'].shape) == 2 \
					else ['zfull'],
				'long_name': 'cloud_occurrence',
				'units': '%',
			},
			'n': {
				'.dims': [],
				'long_name': 'number_of_profiles',
				'units': '1',
			},
			'backscatter_full': {
				'.dims': ['backscatter_full'],
				'long_name': 'total_attenuated_backscatter_coefficient',
				'units': 'm-1 sr-1',
			},
			'backscatter_hist': {
				'.dims': ['backscatter_full', 'zfull'] \
					if len(state['backscatter_hist'].shape) == 2 \
					else ['backscatter_full', 'zfull', 'column'],
				'long_name': 'backscatter_histogram',
				'units': '%',
			},
		}
	}

def stream(dd, state, **options):
	state['state'] = state.get('state', {})
	for d in dd:
		if d is None:
			return [stats_reduce(state['state'], **options)]
		stats_map(d, state['state'], **options)
	return []
