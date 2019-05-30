import numpy as np
from alcf.algorithms import interp
from alcf import misc

def stats_map(d, state,
	tlim=None,
	blim=None,
	bres=None,
	bsd_lim=None,
	bsd_log=None,
	bsd_res=None,
	bsd_z=None,
	filter=None,
	zlim=None,
	zres=None,
	**kwargs
):
	if zlim is not None and zres is not None:
		state['zfull2'] = state.get('zfull2',
			np.arange(zlim[0] + 0.5*zres, zlim[1], zres)
		)
	else:
		state['zfull2'] = state.get('zfull2', d['zfull'])
	zhalf = misc.half(d['zfull'])
	zhalf2 = misc.half(state['zfull2'])
	state['backscatter_half'] = state.get('backscatter_half',
		np.arange(blim[0], blim[1] + bres, bres)
	)
	state['backscatter_full'] = state.get('backscatter_full',
		0.5*(state['backscatter_half'][1:] + state['backscatter_half'][:-1])
	)
	state['backscatter_sd_half'] = state.get('backscatter_sd_half',
		np.exp(np.arange(np.log(bsd_lim[0]), np.log(bsd_lim[1] + bsd_res),
			np.log(bsd_lim[0] + bsd_res) - np.log(bsd_lim[0])))
		# if bsd_log is True \
		# else
		# np.arange(bsd_lim[0], bsd_lim[1] + bsd_res, bsd_res)
	)
	state['backscatter_sd_full'] = state.get('backscatter_sd_full',
		0.5*(state['backscatter_sd_half'][1:] + state['backscatter_sd_half'][:-1])
	)
	o = len(state['backscatter_full'])
	osd = len(state['backscatter_sd_full'])
	m2 = len(state['zfull2'])
	if len(d['cloud_mask'].shape) == 3:
		n, m, l = d['cloud_mask'].shape
		dims = (m, l)
		dims2 = (m2, l)
		hist_dims = (o, m, l)
		hist_dims2 = (o, m2, l)
		sd_hist_dims = (osd, l)
		filter_mask_dims = (n, l)
	else:
		n, m = d['cloud_mask'].shape
		l = 0
		dims = (m,)
		dims2 = (m2,)
		hist_dims = (o, m)
		hist_dims2 = (o, m2)
		sd_hist_dims = (osd,)
		filter_mask_dims = (n,)
	state['n'] = state.get('n',
		0 if l == 0 else np.zeros(l, dtype=np.int64)
	)
	state['cloud_occurrence'] = state.get(
		'cloud_occurrence',
		np.zeros(dims2, dtype=np.float64)
	)
	state['backscatter_hist'] = state.get(
		'backscatter_hist',
		np.zeros(hist_dims2, dtype=np.float64)
	)
	state['backscatter_sd_hist'] = state.get(
		'backscatter_sd_hist',
		np.zeros(sd_hist_dims, dtype=np.float64)
	)
	backscatter_hist_tmp = np.zeros(hist_dims, dtype=np.float64)
	cloud_occurrence_tmp = np.zeros(dims, dtype=np.float64)
	if tlim is not None:
		mask = (d['time'] >= tlim[0]) & (d['time'] < tlim[1])
	else:
		mask = np.ones(n, dtype=np.bool)

	if l > 0:
		mask &= np.all(~np.isnan(d['backscatter']), axis=(1, 2))
	else:
		mask &= np.all(~np.isnan(d['backscatter']), axis=(1,))

	if filter == 'cloudy':
		filter_mask = np.any(d['cloud_mask'], axis=1)
	elif filter == 'clear':
		filter_mask = ~np.any(d['cloud_mask'], axis=1)
	else:
		filter_mask = np.ones(filter_mask_dims, dtype=np.bool)

	if not np.any(mask):
		return
	for j in range(m):
		if l > 0:
			for k in range(l):
				backscatter_hist_tmp[:,j,k] += np.histogram(
					d['backscatter'][filter_mask[:,k],j,k],
					bins=state['backscatter_half'])[0]
		else:
			backscatter_hist_tmp[:,j] += np.histogram(
				d['backscatter'][filter_mask,j],
				bins=state['backscatter_half'])[0]

	if 'backscatter_sd' in d:
		jsd = np.argmin(np.abs(d['zfull'] - bsd_z))
		state['backscatter_sd_z'] = d['zfull'][jsd]
		state['backscatter_sd_hist'] += np.histogram(
			d['backscatter_sd'][filter_mask,jsd],
			bins=state['backscatter_sd_half'])[0]

	for i in range(o):
		if l > 0:
			for k in range(l):
				state['backscatter_hist'][i,:,k] += interp(
					zhalf,
					backscatter_hist_tmp[i,:,k],
					zhalf2
				)
		else:
			state['backscatter_hist'][i,:] += interp(
				zhalf,
				backscatter_hist_tmp[i,:],
				zhalf2
			)
	for i in range(n):
		if not mask[i]:
			continue
		if l > 0:
			for k in range(l):
				if not filter_mask[i,k]:
					continue
				cloud_occurrence_tmp[:,:] += d['cloud_mask'][i,:,k]
				state['n'][k] += 1
		else:
			if not filter_mask[i]:
				continue
			cloud_occurrence_tmp[:] += d['cloud_mask'][i,:]
			state['n'] += 1
	if l > 0:
		for k in range(l):
			state['cloud_occurrence'][:,k] += interp(
				zhalf,
				cloud_occurrence_tmp[:,k],
				zhalf2
			)
	else:
		state['cloud_occurrence'] += interp(
			zhalf,
			cloud_occurrence_tmp,
			zhalf2
		)

def stats_reduce(state, bsd_z=None, **kwargs):
	if state['cloud_occurrence'].shape == 2:
		for k in range(state['n'].shape[1]):
			if state['n'][k] > 0:
				state['backscatter_hist'][:,:,k] /= state['n'][k]
				state['cloud_occurrence'][:,k] /= state['n'][k]
	else:
		if state['n'] != 0:
			state['backscatter_hist'] /= state['n']
			state['cloud_occurrence'] /= state['n']
	state['backscatter_sd_hist'] /= state['n']
	return {
		'cloud_occurrence': 100.*state['cloud_occurrence'],
		'zfull': state['zfull2'],
		'n': state['n'],
		'backscatter_full': state['backscatter_full'],
		'backscatter_hist': state['backscatter_hist'],
		'backscatter_sd_hist': state['backscatter_sd_hist'],
		'backscatter_sd_full': state['backscatter_sd_full'],
		'backscatter_sd_z': state['backscatter_sd_z'],
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
				'.dims': ['column'] \
					if len(state['cloud_occurrence'].shape) == 2 \
					else [],
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
			'backscatter_sd_hist': {
				'.dims': ['backscatter_sd_full'],
				'long_name': 'total_attenuated_backscatter_coefficient_standard_deviation_histogram',
				'units': '%',
			},
			'backscatter_sd_full': {
				'.dims': ['backscatter_sd_full'],
				'long_name': 'total_attenuated_backscatter_coefficient_standard_deviation',
				'units': 'm-1 sr-1',
			},
			'backscatter_sd_z': {
				'.dims': [],
				'long_name': 'total_attenuated_backscatter_coefficient_standard_deviation_height_above_reference_ellipsoid',
				'units': 'm',
			}
		}
	}

def stream(dd, state, **options):
	state['state'] = state.get('state', {})
	for d in dd:
		if d is None:
			return [stats_reduce(state['state'], **options)]
		stats_map(d, state['state'], **options)
	return []
