import copy
from warnings import warn
import numpy as np
import ds_format as ds
from alcf import misc, algorithms

def calc_filter_mask(filters, time, l):
	n = len(time)
	if len(filters) == 0:
		filter_mask = np.zeros(n, dtype=bool)
	else:
		filter_mask = np.ones(n, dtype=bool)
	for filter_ in filters:
		filter_mask_tmp = np.zeros(n, dtype=bool)
		m = filter_.shape[0]
		for i in range(m):
			t1, t2 = filter_[i]
			filter_mask_tmp |= (time >= t1) & (time < t2)
		filter_mask &= filter_mask_tmp
	if l > 0: filter_mask = np.tile(filter_mask, [l, 1]).T
	return filter_mask

def stats_map(d, state,
	tlim=None,
	blim=None,
	bres=None,
	bsd_lim=None,
	bsd_log=None,
	bsd_res=None,
	bsd_z=None,
	filter=None,
	filters_exclude=None,
	filters_include=None,
	zlim=None,
	zres=None,
	lat_lim=None,
	lon_lim=None,
	interp=None,
	keep_vars=[],
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
	o = len(state['backscatter_full'])
	state['backscatter_sd_half'] = state.get('backscatter_sd_half',
		np.exp(np.arange(np.log(bsd_lim[0]), np.log(bsd_lim[1] + bsd_res),
			np.log(bsd_lim[0] + bsd_res) - np.log(bsd_lim[0])))
		if bsd_log is True \
		else np.arange(bsd_lim[0], bsd_lim[1] + bsd_res, bsd_res)
	)
	state['backscatter_sd_full'] = state.get('backscatter_sd_full',
		0.5*(state['backscatter_sd_half'][1:] + state['backscatter_sd_half'][:-1])
	)
	osd = len(state['backscatter_sd_full'])
	jsd = np.argmin(np.abs(d['zfull'] - bsd_z))
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
	state['time_total'] = state.get('time_total',
		0 if l == 0 else np.zeros(l, dtype=np.int64)
	)
	state['backscatter_avg'] = state.get(
		'backscatter_avg',
		np.zeros(dims2, dtype=np.float64)
	)
	state['backscatter_mol_avg'] = state.get(
		'backscatter_mol_avg',
		np.zeros(dims2, dtype=np.float64)
	)
	state['cl'] = state.get(
		'cl',
		np.zeros(dims2, dtype=np.float64)
	)
	state['cbh'] = state.get(
		'cbh',
		np.zeros(dims2, dtype=np.float64)
	)
	state['clt'] = state.get(
		'clt',
		np.zeros(l, dtype=np.float64) if l > 0 else 0
	)
	state['backscatter_hist'] = state.get(
		'backscatter_hist',
		np.zeros(hist_dims2, dtype=np.float64)
	)
	state['backscatter_sd_hist'] = state.get(
		'backscatter_sd_hist',
		np.zeros(sd_hist_dims, dtype=np.float64)
	)
	state['backscatter_sd_z'] = d['zfull'][jsd]

	backscatter_hist_tmp = np.zeros(hist_dims, dtype=np.float64)
	cl_tmp = np.zeros(dims, dtype=np.float64)
	clt_tmp = np.zeros(l, dtype=np.float64) if l > 0 else 0
	backscatter_avg_tmp = np.zeros(dims, dtype=np.float64)
	backscatter_mol_avg_tmp = np.zeros(dims, dtype=np.float64)

	keep_vars_avg_tmp = {}
	keep_vars_n_tmp = {}
	keep_vars_actual = []
	for var in keep_vars:
		if var not in d:
			continue
		shape = list(d[var].shape)
		shape_n = []
		var_dims = ds.dims(d, var)
		if var_dims not in [['time'], ['time', 'level']]:
			warn('variable "%s" must have dimensions ("time") or ("time", "level") in order to be kept' % var)
			continue
		keep_vars_actual += [var]
		del var_dims[0]
		del shape[0]
		if l > 0:
			shape += [l]
			shape_n += [l]
			var_dims += ['column']
		state[var + '_avg'] = state.get(
			var + '_avg',
			np.zeros(shape, dtype=np.float64)
		)
		state[var + '_n'] = state.get(
			var + '_n',
			np.zeros(shape_n, dtype=np.int64)
		)
		state[var + '_meta'] = copy.deepcopy(d['.'][var])
		state[var + '_meta']['.dims'] = var_dims
		state[var + '_meta_n'] = {
			'.dims': ['column'] if l > 0 else [],
			'long_name': 'number of profiles used to calculate %s_avg' % var,
			'units': '1',
		}
		keep_vars_avg_tmp[var] = np.zeros(shape, dtype=np.float64)
		keep_vars_n_tmp[var] = np.zeros(shape_n, dtype=np.int64)

	mask = np.ones(n, dtype=bool)
	if tlim is not None:
		mask &= (d['time'] >= tlim[0]) & (d['time'] < tlim[1])
	if lat_lim is not None:
		mask &= (d['lat'] >= lat_lim[0]) & (d['lat'] < lat_lim[1])
	if lon_lim is not None:
		mask &= (d['lon'] >= lon_lim[0]) & (d['lon'] < lon_lim[1])

	if l > 0:
		mask &= np.all(~np.isnan(d['backscatter']), axis=(1, 2))
	else:
		mask &= np.all(~np.isnan(d['backscatter']), axis=(1,))

	filter_mask = np.ones(filter_mask_dims, dtype=bool)
	if 'cloudy' in filter:
		filter_mask &= np.any(d['cloud_mask'], axis=1)
	if 'clear' in filter:
		filter_mask &= ~np.any(d['cloud_mask'], axis=1)
	if 'day' in filter:
		filter_mask_0 = misc.sun_altitude(d['time'], d['lon'], d['lat']) >= 0
		if l > 0: filter_mask_0 = np.tile(filter_mask_0, [l, 1]).T
		filter_mask &= filter_mask_0
	if 'night' in filter:
		filter_mask_0 = misc.sun_altitude(d['time'], d['lon'], d['lat']) < 0
		if l > 0: filter_mask_0 = np.tile(filter_mask_0, [l, 1]).T
		filter_mask &= filter_mask_0

	if filters_exclude is not None:
		filter_mask &= ~calc_filter_mask(filters_exclude, d['time'], l)

	if filters_include is not None:
		filter_mask &= calc_filter_mask(filters_include, d['time'], l)

	if not np.any(mask):
		return
	for j in range(m):
		if l > 0:
			for k in range(l):
				backscatter_hist_tmp[:,j,k] += np.histogram(
					d['backscatter'][filter_mask[:,k] & mask,j,k],
					bins=state['backscatter_half'])[0]
		else:
			backscatter_hist_tmp[:,j] += np.histogram(
				d['backscatter'][filter_mask & mask,j],
				bins=state['backscatter_half'])[0]

	if 'backscatter_sd' in d:
		if l > 0:
			for k in range(l):
				state['backscatter_sd_hist'][:,k] += np.histogram(
					d['backscatter_sd'][filter_mask[:,k] & mask,jsd,k],
					bins=state['backscatter_sd_half'])[0]
		else:
			state['backscatter_sd_hist'] += np.histogram(
				d['backscatter_sd'][filter_mask & mask,jsd],
				bins=state['backscatter_sd_half'])[0]

	for i in range(o):
		if l > 0:
			for k in range(l):
				state['backscatter_hist'][i,:,k] += algorithms.interp(
					interp,
					d['zfull'], zhalf,
					backscatter_hist_tmp[i,:,k],
					state['zfull2'], zhalf2
				)
		else:
			state['backscatter_hist'][i,:] += algorithms.interp(
				interp,
				d['zfull'], zhalf,
				backscatter_hist_tmp[i,:],
				state['zfull2'], zhalf2
			)
	for i in range(n):
		if not mask[i]:
			continue
		if l > 0:
			for k in range(l):
				if not filter_mask[i,k]:
					continue
				cl_tmp[:,k] += d['cloud_mask'][i,:,k]
				if np.isfinite(d['cbh'][i,k]):
					j = np.argmin(np.abs(state['zfull2'] - d['cbh'][i,k]))
					state['cbh'][j,k] += 1
				backscatter_avg_tmp[:,k] += d['backscatter'][i,:,k]
				if 'backscatter_mol' in d:
					backscatter_mol_avg_tmp[:,k] += d['backscatter_mol'][i,:]
				state['n'][k] += 1
				state['time_total'][k] += \
					24*60*60*(d['time_bnds'][i,1] - d['time_bnds'][i,0])
				state['clt'][k] += np.any(d['cloud_mask'][i,:,k])
				for var in keep_vars_actual:
					if var in d:
						if not np.any(np.isnan(d[var][i])):
							keep_vars_avg_tmp[var][...,k] += d[var][i]
							keep_vars_n_tmp[var][k] += 1
		else:
			if not filter_mask[i]:
				continue
			cl_tmp[:] += d['cloud_mask'][i,:]
			if np.isfinite(d['cbh'][i]):
				j = np.argmin(np.abs(state['zfull2'] - d['cbh'][i]))
				state['cbh'][j] += 1
			backscatter_avg_tmp[:] += d['backscatter'][i,:]
			if 'backscatter_mol' in d:
				backscatter_mol_avg_tmp[:] += d['backscatter_mol'][i,:]
			state['n'] += 1
			state['time_total'] += \
				24*60*60*(d['time_bnds'][i,1] - d['time_bnds'][i,0])
			state['clt'] += np.any(d['cloud_mask'][i,:])
			for var in keep_vars_actual:
				if var in d:
					if not np.isnan(d[var][i]):
						keep_vars_avg_tmp[var] += d[var][i]
						keep_vars_n_tmp[var] += 1
	if l > 0:
		for k in range(l):
			state['cl'][:,k] += algorithms.interp(
				interp,
				d['zfull'], zhalf,
				cl_tmp[:,k],
				state['zfull2'], zhalf2
			)
			state['backscatter_avg'][:,k] += algorithms.interp(
				interp,
				d['zfull'], zhalf,
				backscatter_avg_tmp[:,k],
				state['zfull2'], zhalf2
			)
			state['backscatter_mol_avg'][:,k] += algorithms.interp(
				interp,
				d['zfull'], zhalf,
				backscatter_mol_avg_tmp[:,k],
				state['zfull2'], zhalf2
			)
	else:
		state['cl'] += algorithms.interp(
			interp,
			d['zfull'], zhalf,
			cl_tmp,
			state['zfull2'], zhalf2
		)
		state['backscatter_avg'] += algorithms.interp(
			interp,
			d['zfull'], zhalf,
			backscatter_avg_tmp,
			state['zfull2'], zhalf2
		)
		state['backscatter_mol_avg'] += algorithms.interp(
			interp,
			d['zfull'], zhalf,
			backscatter_mol_avg_tmp,
			state['zfull2'], zhalf2
		)
	for var in keep_vars_actual:
		if var in d and len(d[var].shape) == 2:
			state[var + '_avg'] += algorithms.interp(
				interp,
				d['zfull'], zhalf,
				keep_vars_avg_tmp,
				state['zfull2'], zhalf2
			)
		else:
			state[var + '_avg'] += keep_vars_avg_tmp[var]
		state[var + '_n'] += keep_vars_n_tmp[var]

def stats_reduce(state, bsd_z=None, keep_vars=[], **kwargs):
	if not 'n' in state:
		return {}
	if len(state['cl'].shape) == 2:
		for k in range(len(state['n'])):
			if state['clt'][k] > 0:
				state['cbh'][:,k] /= state['clt'][k]
			if state['n'][k] > 0:
				state['backscatter_hist'][:,:,k] /= state['n'][k]
				state['cl'][:,k] /= state['n'][k]
				state['clt'][k] /= state['n'][k]
				state['backscatter_avg'][:,k] /= state['n'][k]
				state['backscatter_mol_avg'][:,k] /= state['n'][k]

			else:
				state['backscatter_avg'][:,k] = np.nan
				state['backscatter_mol_avg'][:,k] = np.nan
			for var in keep_vars:
				if var + '_avg' in state:
					if state[var + '_n'][k] > 0:
						state[var + '_avg'][...,k] /= state[var + '_n'][k]
					else:
						state[var + '_avg'][...,k] = np.nan
	else:
		if state['clt'] > 0:
			state['cbh'] /= state['clt']
		if state['n'] > 0:
			state['backscatter_hist'] /= state['n']
			state['cl'] /= state['n']
			state['clt'] /= state['n']
			state['backscatter_avg'] /= state['n']
			state['backscatter_mol_avg'] /= state['n']
			state['backscatter_sd_hist'] /= state['n']
		else:
			state['backscatter_avg'] /= np.nan
			state['backscatter_mol_avg'] /= np.nan
		for var in keep_vars:
			if var + '_avg' in state:
				if state[var + '_n'] > 0:
					state[var + '_avg'] /= state[var + '_n']
				else:
					state[var + '_avg'] = np.nan

	do = {
		'cl': 100.*state['cl'],
		'cbh': 100.*state['cbh'],
		'clt': 100.*state['clt'],
		'zfull': state['zfull2'],
		'n': state['n'],
		'time_total': state['time_total'],
		'backscatter_avg': state['backscatter_avg'],
		'backscatter_mol_avg': state['backscatter_mol_avg'],
		'backscatter_full': state['backscatter_full'],
		'backscatter_hist': state['backscatter_hist'],
		'backscatter_sd_hist': state['backscatter_sd_hist'],
		'backscatter_sd_full': state['backscatter_sd_full'],
		'backscatter_sd_z': state['backscatter_sd_z'],
	}
	do['.'] = {
		'zfull': {
			'.dims': ['zfull'],
			'long_name': 'altitude of model full-levels',
			'standard_name': 'height_above_reference_ellipsoid',
			'units': 'm',
		},
		'cl': {
			'.dims': ['zfull', 'column'] \
				if len(state['cl'].shape) == 2 \
				else ['zfull'],
			'long_name': 'cloud area fraction',
			'standard_name': 'cloud_area_fraction_in_atmosphere_layer',
			'units': '%',
		},
		'cbh': {
			'.dims': ['zfull', 'column'] \
				if len(state['cl'].shape) == 2 \
				else ['zfull'],
			'long_name': 'cloud base height',
			'units': '%',
		},
		'clt': {
			'.dims': ['column'] \
				if isinstance(state['clt'], np.ndarray) \
				else [],
			'long_name': 'total cloud fraction',
			'standard_name': 'cloud_area_fraction',
			'units': '%',
		},
		'n': {
			'.dims': ['column'] \
				if len(state['cl'].shape) == 2 \
				else [],
			'long_name': 'number of profiles',
			'units': '1',
		},
		'time_total': {
			'.dims': ['column'] \
				if len(state['cl'].shape) == 2 \
				else [],
			'long_name': 'total time',
			'standard_name': 'time',
			'units': 's',
		},
		'backscatter_avg': {
			'.dims': ['zfull', 'column'] \
				if len(state['cl'].shape) == 2 \
				else ['zfull'],
			'long_name': 'total attenuated volume backscattering coefficient average',
			'units': 'm-1 sr-1',
		},
		'backscatter_mol_avg': {
			'.dims': ['zfull', 'column'] \
				if len(state['cl'].shape) == 2 \
				else ['zfull'],
			'long_name': 'total attenuated molecular volume backscattering coefficient average',
			'units': 'm-1 sr-1',
		},
		'backscatter_full': {
			'.dims': ['backscatter_full'],
			'long_name': 'total attenuated volume backscattering coefficient',
			'units': 'm-1 sr-1',
		},
		'backscatter_hist': {
			'.dims': ['backscatter_full', 'zfull'] \
				if len(state['backscatter_hist'].shape) == 2 \
				else ['backscatter_full', 'zfull', 'column'],
			'long_name': 'total attenuated volume backscattering coefficient histogram',
			'units': '1',
		},
		'backscatter_sd_hist': {
			'.dims': ['backscatter_sd_full'],
			'.dims': ['backscatter_sd_full'] \
				if len(state['backscatter_sd_hist'].shape) == 1 \
				else ['backscatter_sd_full', 'column'],
			'long_name': 'total attenuated volume backscattering coefficient standard deviation histogram',
			'units': '1',
		},
		'backscatter_sd_full': {
			'.dims': ['backscatter_sd_full'],
			'long_name': 'total attenuated volume backscattering coefficient standard deviation',
			'units': 'm-1 sr-1',
		},
		'backscatter_sd_z': {
			'.dims': [],
			'long_name': 'total attenuated volume backscattering coefficient standard deviation height above reference ellipsoid',
			'units': 'm',
		},
	}
	for var in keep_vars:
		if var + '_avg' in state:
			do[var + '_avg'] = state[var + '_avg']
			do[var + '_n'] = state[var + '_n']
			do['.'][var + '_avg'] = state[var + '_meta']
			do['.'][var + '_n'] = state[var + '_meta_n']
	return do

def stream(dd, state, **options):
	state['state'] = state.get('state', {})
	for d in dd:
		if d is None:
			return [stats_reduce(state['state'], **options)]
		stats_map(d, state['state'], **options)
	return []
