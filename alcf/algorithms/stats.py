import copy
from warnings import warn
import numpy as np
import ds_format as ds
from alcf import misc, algorithms

META = {
	'backscatter_sd_z': {
		'.dims': [],
		'long_name': 'total attenuated volume backscattering coefficient standard deviation height above reference ellipsoid',
		'units': 'm',
	},
	'cl': {
		'long_name': 'cloud area fraction',
		'standard_name': 'cloud_area_fraction_in_atmosphere_layer',
		'units': '%',
	},
	'cbh': {
		'long_name': 'cloud base height',
		'units': '%',
	},
	'clt': {
		'long_name': 'total cloud fraction',
		'standard_name': 'cloud_area_fraction',
		'units': '%',
	},
	'n': {
		'long_name': 'number of profiles',
		'units': '1',
	},
	'time_total': {
		'long_name': 'total time',
		'standard_name': 'time',
		'units': 's',
	},
	'zfull': {
		'.dims': ['zfull'],
		'long_name': 'altitude of model full-levels',
		'standard_name': 'height_above_reference_ellipsoid',
		'units': 'm',
	},
}

def expand_column(d, vars_):
	for var in vars_:
		if var in ds.vars(d):
			x = ds.var(d, var)
			size = ds.size(d, var)
			dims = ds.dims(d, var)
			if isinstance(x, np.ndarray):
				ds.var(d, var, x.reshape(size + [1]))
			else:
				ds.var(d, var, np.array([x]))
			ds.dims(d, var, dims + ['column'])

def shrink_column(d):
	for var in ds.vars(d):
		dims = ds.dims(d, var)
		size = ds.size(d, var)
		x = ds.var(d, var)
		if len(dims) > 0 and dims[-1] == 'column' and size[-1] == 1:
			ds.var(d, var, x.reshape(size[:-1]))
			ds.dims(d, var, dims[:-1])

def init_meta(d, s, var_from, var_to):
	s['meta'][var_to] = ds.attrs(d, var_from)

def init_vector(d, s, var, dtype=np.float64, size=None, dims=None):
	if size is None: size = s['size'][1:]
	if dims is None: dims = s['dims'][1:]
	s[var] = np.zeros(size, dtype)
	s['meta'][var]['.dims'] = dims

def init_scalar(d, s, var, dtype=np.float64):
	s[var] = np.zeros(s['size'][2], dtype)
	s['meta'][var]['.dims'] = [s['dims'][2]]

def init_hist(d, s, var, ndim, x1, x2, res, log=False):
	if log:
		s[var+'_half'] = np.exp(np.arange(
			np.log(x1),
			np.log(x2 + res),
			np.log(x1 + res) - np.log(x1)
		))
	else:
		s[var+'_half'] = np.arange(x1, x2, res)
	s[var+'_full'] = misc.full(s[var+'_half'])
	o = len(s[var+'_full'])
	k = 2 if ndim == 1 else 1
	size = [o] + s['size'][k:]
	dims = [var+'_full'] + s['dims'][k:]
	s[var+'_hist'] = np.zeros(size)
	init_meta(d, s, var, var+'_full')
	s['meta'][var+'_full']['.dims'] = [var+'_full']
	s['meta'][var+'_hist'] = {
		'.dims': dims,
		'long_name': ds.attr(d, 'long_name', var=var) + ' histogram',
		'units': '1',
	}

def init_avg(d, s, var, with_n=False, dtype=np.float64):
	init_meta(d, s, var, var+'_avg')
	s['meta'][var+'_avg'].update({
		'.dims': s['dims'][1:],
		'long_name': s['meta'][var+'_avg']['long_name'] + ' average',
	})
	init_vector(d, s, var+'_avg', dtype=dtype)
	if with_n:
		s['meta'][var+'_n'].updae({
			'.dims': s['dims'][2:],
			'long_name': 'number of profiles used to calculate %s_avg' % var,
			'units': '1',
		})
		init_scalar(d, s, var+'_n', dtype=np.int64)

def init(d, s, *,
	blim,
	bres,
	bsd_lim,
	bsd_log,
	bsd_res,
	zlim,
	zres,
	bsd_z,
	keep_vars,
):
	s['meta'] = copy.deepcopy(META)
	n = ds.dim(d, 'time')
	m = len(d['zfull'])
	l = ds.dim(d, 'column')
	s['size'] = [n, m, l]
	s['dims'] = ['time', 'zfull', 'column']
	s['zfull'] = d['zfull']
	if zlim is not None and zres is not None:
		s['zfull2'] = np.arange(zlim[0] + 0.5*zres, zlim[1], zres)
	else:
		s['zfull2'] = s['zfull']
	s['zhalf'] = misc.half(s['zfull'])
	s['zhalf2'] = misc.half(s['zfull2'])
	m2 = len(s['zfull2'])
	s['size2'] = [n, m2, l]
	s['dims2'] = ['time', 'zfull2', 'column']
	init_hist(d, s, 'backscatter', 2, blim[0], blim[1] + bres, bres)
	if 'backscatter_sd' in ds.vars(d):
		init_hist(d, s, 'backscatter_sd', 1, bsd_lim[0], bsd_lim[1], bsd_res,
			log=bsd_log)
	init_avg(d, s, 'backscatter')
	if 'backscatter_mol' in ds.vars(d):
		init_avg(d, s, 'backscatter_mol')
	init_scalar(d, s, 'n', np.int64)
	init_scalar(d, s, 'time_total')
	init_scalar(d, s, 'clt')
	init_vector(d, s, 'cl')
	init_vector(d, s, 'cbh', size=s['size2'][1:], dims=s['dims2'][1:])
	s['backscatter_sd_j'] = np.argmin(np.abs(s['zfull'] - bsd_z))
	s['backscatter_sd_z'] = s['zfull'][s['backscatter_sd_j']]
	s['keep_vars'] = []
	for var in keep_vars:
		if var not in ds.vars(d):
			continue
		s['keep_vars'] += [var]
		dims = ds.dims(d, var)
		if dims not in [['time'], ['time', 'level']]:
			warn('variable "%s" must have dimensions ("time") or ("time", "level") in order to be kept' % var)
			continue
		s['meta'][var+'_n'] = {
			'.dims': dims[1:],
			'long_name': 'number of profiles used to calculate %s_avg' % var,
			'units': '1',
		}
		init_avg(d, s, var, with_n=True)

def hist(d, s, var, ndim, mask, level=None):
	if ndim == 1:
		for k in range(s['size'][2]):
			s[var+'_hist'][:,k] += np.histogram(
				d[var][mask[:,k],level,k],
				bins=s[var+'_half']
			)[0]
	else:
		for j in range(s['size'][1]):
			for k in range(s['size'][2]):
				s[var+'_hist'][:,j,k] += np.histogram(
					d[var][mask[:,k],j,k],
					bins=s[var+'_half']
				)[0]

def create_filter_mask(filters, time, l):
	n = len(time)
	if len(filters) == 0:
		filter_mask = np.zeros(n, bool)
	else:
		filter_mask = np.ones(n, bool)
	for filter_ in filters:
		filter_mask_tmp = np.zeros(n, bool)
		m = filter_.shape[0]
		for i in range(m):
			t1, t2 = filter_[i]
			filter_mask_tmp |= (time >= t1) & (time < t2)
		filter_mask &= filter_mask_tmp
	filter_mask = np.tile(filter_mask, [l, 1]).T
	return filter_mask

def create_mask(d, filter, filters_exclude, filters_include,
	tlim, lat_lim, lon_lim):

	n = ds.dim(d, 'time')
	l = ds.dim(d, 'column')

	lonm = ~np.isnan(d['lon'])
	latm = ~np.isnan(d['lat'])
	llm = lonm & latm

	mask = np.ones(n, bool)
	if tlim is not None:
		mask &= (d['time'] >= tlim[0]) & (d['time'] < tlim[1])
	if lat_lim is not None:
		mask &= (d['lat'] >= lat_lim[0]) & (d['lat'] < lat_lim[1])
		mask[~latm] = False
	if lon_lim is not None:
		mask &= (d['lon'] >= lon_lim[0]) & (d['lon'] < lon_lim[1])
		mask[~lonm] = False

	mask &= np.all(~np.isnan(d['backscatter']), axis=(1, 2))
	mask = np.tile(mask, [l, 1]).T

	if 'cloudy' in filter:
		mask &= np.any(d['cloud_mask'], axis=1)
	if 'clear' in filter:
		mask &= ~np.any(d['cloud_mask'], axis=1)
	if 'day' in filter:
		tmp = np.zeros(n, bool)
		tmp[llm] = misc.sun_altitude(
			d['time'][llm],
			d['lon'][llm],
			d['lat'][llm]
			) >= 0
		mask &= np.tile(tmp, [l, 1]).T
	if 'night' in filter:
		tmp = np.zeros(n, bool)
		tmp[llm] = misc.sun_altitude(
			d['time'][llm],
			d['lon'][llm],
			d['lat'][llm]
			) < 0
		mask &= np.tile(tmp, [l, 1]).T

	if filters_exclude is not None:
		mask &= ~create_filter_mask(filters_exclude, d['time'], l)

	if filters_include is not None:
		mask &= create_filter_mask(filters_include, d['time'], l)

	return mask

def stats_map(d, s,
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
	n = ds.dim(d, 'time')
	l = ds.dim(d, 'column')

	if l == 0:
		tmp = copy.copy(d)
		tmp['.'] = copy.deepcopy(d['.'])
		d = tmp
		expand_column(d, [
			'backscatter',
			'backscatter_sd',
			'cbh',
			'cloud_mask',
			'lr',
		] + keep_vars)
		s['expanded_column'] = True
		l = 1

	if not s.get('initialized'):
		init(d, s,
			blim=blim,
			bres=bres,
			bsd_lim=bsd_lim,
			bsd_log=bsd_log,
			bsd_res=bsd_res,
			zlim=zlim,
			zres=zres,
			bsd_z=bsd_z,
			keep_vars=keep_vars,
		)
		s['interp'] = interp
		s['initialized'] = True
	
	mask = create_mask(d, filter, filters_exclude, filters_include,
		tlim, lon_lim, lat_lim)

	if not np.any(mask):
		return

	hist(d, s, 'backscatter', 2, mask)
	if 'backscatter_sd' in ds.vars(d):
		hist(d, s, 'backscatter_sd', 1, mask, level=s['backscatter_sd_j'])

	for i in range(n):
		dt = 24*60*60*(d['time_bnds'][i,1] - d['time_bnds'][i,0])
		for k in range(s['size'][2]):
			if not mask[i,k]:
				continue
			s['cl'][:,k] += d['cloud_mask'][i,:,k]
			if np.isfinite(d['cbh'][i,k]):
				j = np.argmin(np.abs(s['zfull2'] - d['cbh'][i,k]))
				s['cbh'][j,k] += 1
			s['backscatter_avg'][:,k] += d['backscatter'][i,:,k]
			if 'backscatter_mol' in ds.vars(d):
				s['backscatter_mol_avg'][:,k] += d['backscatter_mol'][i,:]
			s['n'][k] += 1
			s['time_total'][k] += dt
			s['clt'][k] += np.any(d['cloud_mask'][i,:,k])
			for var in s['keep_vars']:
				if not np.any(np.isnan(d[var][i])):
					s[var+'_avg'][...,k] += d[var][i]
					s[var+'_n'][var][k] += 1

def reduce_var(s, var, var_n):
	def interp(x):
		return algorithms.interp(
			s['interp'],
			s['zfull'],
			s['zhalf'],
			x,
			s['zfull2'],
			s['zhalf2']
		)
	size = list(s[var].shape)
	size2 = copy.copy(size)
	dims = s['meta'][var]['.dims']
	dims2 = copy.copy(dims)
	try: i = dims.index('zfull')
	except ValueError: i = None
	if i is not None:
		size2[i] = len(s['zfull2'])
		dims2[i] = 'zfull2'
	tmp = np.full(size2, np.nan)
	for k in range(s['size'][2]):
		if s[var].ndim == 3 and dims[1] == 'zfull':
			for i in range(s[var].shape[0]):
				tmp[i,:,k] = interp(s[var][i,:,k])
		elif s[var].ndim == 2 and dims[0] == 'zfull':
			tmp[:,k] = interp(s[var][:,k])
		else:
			tmp[...,k] = s[var][...,k]
		tmp[...,k] = tmp[...,k]/s[var_n][k] \
			if s[var_n][k] > 0 \
			else np.nan
	s['meta'][var]['.dims'] = dims2
	s[var] = tmp

def stats_reduce(s, bsd_z=None, **kwargs):
	if not s.get('initialized'):
		return {}
	reduce_var(s, 'backscatter_avg', 'n')
	reduce_var(s, 'backscatter_hist', 'n')
	if 'backscatter_mol_avg' in s:
		reduce_var(s, 'backscatter_mol_avg', 'n')
	if 'backscatter_sd_hist' in s:
		reduce_var(s, 'backscatter_sd_hist', 'n')
	reduce_var(s, 'cl', 'n')
	reduce_var(s, 'cbh', 'clt')
	reduce_var(s, 'clt', 'n')
	for var in s['keep_vars']:
		reduce_var(s, var+'_avg', var+'_n')

	do = {
		'backscatter_avg': s['backscatter_avg'],
		'backscatter_full': s['backscatter_full'],
		'backscatter_hist': s['backscatter_hist'],
		'cl': 100.*s['cl'],
		'cbh': 100.*s['cbh'],
		'clt': 100.*s['clt'],
		'n': s['n'],
		'time_total': s['time_total'],
		'zfull': s['zfull2'],
		'.': s['meta'],
	}
	if 'backscatter_mol_avg' in s:
		do['backscatter_mol_avg'] = s['backscatter_mol_avg']
	if 'backscatter_sd_hist' in s:
		do['backscatter_sd_full'] = s['backscatter_sd_full']
		do['backscatter_sd_hist'] = s['backscatter_sd_hist']
		do['backscatter_sd_z'] = s['backscatter_sd_z']
	for var in s['keep_vars']:
		do[var+'_avg'] = s[var+'_avg']
		do[var+'_n'] = s[var+'_n']

	ds.rename_dim(do, 'zfull2', 'zfull')

	if s.get('expanded_column'):
		shrink_column(do)

	return do

def stream(dd, state, **options):
	state['state'] = state.get('state', {})
	for d in dd:
		if d is None:
			return [stats_reduce(state['state'], **options)]
		stats_map(d, state['state'], **options)
	return []
