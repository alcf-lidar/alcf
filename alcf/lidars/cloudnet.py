import numpy as np
import ds_format as ds
import datetime as dt
from alcf import misc
from alcf.lidars import META

VARS = {
	'backscatter': ['beta_raw'],
	'zfull': ['height'],
}

DEFAULT_VARS = [
	'time',
	'height',
	'altitude',
]

def params(type_):
	if not type_.startswith('cn_'):
		raise ValueError('Lidar type must start with "cn_"')
	instrument = type_[3:]
	from alcf.lidars import LIDARS
	lidar = LIDARS[instrument]
	p = lidar.params(instrument)
	p['calibration_coeff'] = 1
	return p

def read(type_, filename, vars,
	altitude=None,
	tlim=None,
	keep_vars=[],
	**kwargs
):
	p = params(type_)
	sel = None
	if tlim is not None:
		d = ds.read(filename, 'time', jd=True)
		misc.require_vars(d, ['time'])
		d['time_bnds'] = misc.time_bnds(d['time'])
		mask = misc.time_mask(d['time_bnds'], tlim[0], tlim[1])
		if np.sum(mask) == 0: return None
		sel = {'time': mask}

	dep_vars = misc.dep_vars(VARS, vars)
	req_vars = dep_vars + DEFAULT_VARS + keep_vars
	d = ds.read(filename, req_vars, jd=True, sel=sel, full=True)
	misc.require_vars(d, req_vars)
	dx = {}
	misc.populate_meta(dx, META, set(vars) & set(VARS))
	n = ds.dim(d, 'time')
	if 'time' in vars:
		dx['time'] = d['time']
	if 'time_bnds' in vars:
		args = [] if tlim is None else [tlim[0], tlim[1]]
		dx['time_bnds'] = misc.time_bnds(d['time'], None, *args)
	if 'altitude' in vars:
		if altitude is not None:
			dx['altitude'] = np.full(n, altitude, np.float64)
		else:
			dx['altitude'] = np.full(n, d['altitude'], np.float64)
	if 'zfull' in vars:
		dx['zfull'] = np.tile(d['height'], (n, 1))
	if 'backscatter' in vars:
		dx['backscatter'] = d['beta_raw']*p['calibration_coeff']
	for var in keep_vars:
		misc.keep_var(var, d, dx)
	return dx
