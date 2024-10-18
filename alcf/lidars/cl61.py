import numpy as np
import ds_format as ds
from alcf import misc
from alcf.lidars import META

WAVELENGTH = 910 # nm
CALIBRATION_COEFF = 1
SURFACE_LIDAR = True
SC_LR = 18.8 # sr. Stratocumulus lidar ratio (O'Connor et al., 2004).
MAX_RANGE = 15400 # m

VARS = {
	'backscatter': ['beta_att'],
	'zfull': ['range', 'elevation'],
	'altitude': ['elevation'],
}

DEFAULT_VARS = [
	'time'
]

def read(
	filename,
	vars,
	altitude=None,
	tlim=None,
	keep_vars=[],
	**kwargs
):
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
	d = ds.read(filename, req_vars, sel=sel, full=True)
	misc.require_vars(d, req_vars)
	dx = {}
	misc.populate_meta(dx, META, set(vars) & set(VARS))
	n = len(d['time'])
	d['time'] = d['time']/86400. + 2440587.5
	if 'time' in vars:
		dx['time'] = d['time']
	if 'time_bnds' in vars:
		args = [] if tlim is None else [tlim[0], tlim[1]]
		dx['time_bnds'] = misc.time_bnds(d['time'], None, *args)
	if 'altitude' in vars or 'zfull' in vars:
		if altitude is not None:
			dx['altitude'] = np.full(n, altitude, np.float64)
		else:
			if d['elevation'].ndim == 0:
				dx['altitude'] = np.full(n, d['elevation'], np.float64)
			else:
				dx['altitude'] = d['elevation']
	if 'zfull' in vars:
		dx['zfull'] = np.tile(d['range'], (n, 1))
		dx['zfull'] = (dx['zfull'].T + dx['altitude']).T
	if 'backscatter' in vars:
		dx['backscatter'] = d['beta_att']*CALIBRATION_COEFF
	for var in keep_vars:
		misc.keep_var(var, d, dx, {'time': 'profile', 'level': 'range'})
	return dx
