import numpy as np
import ds_format as ds
from alcf import misc
from alcf.lidars import META

WAVELENGTH = 1064 # nm
CALIBRATION_COEFF = 0.34
SURFACE_LIDAR = True
SC_LR = 18.2 # sr. Stratocumulus lidar ratio (O'Connor et al., 2004).
MAX_RANGE = 15400 # m

VARS = {
	'backscatter': ['beta_raw'],
	'zfull': ['range', 'altitude'],
}

DEFAULT_VARS = [
	'time',
	'altitude'
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
	d = ds.read(filename, req_vars, jd=True, sel=sel, full=True)
	misc.require_vars(d, req_vars)
	dx = {}
	misc.populate_meta(dx, META, set(vars) & set(VARS))
	n = ds.dim(d, 'time')
	m = ds.dim(d, 'range')
	if 'altitude' in vars or 'zfull' in vars:
		if altitude is not None:
			dx['altitude'] = np.full(n, altitude, np.float64)
		else:
			dx['altitude'] = d['altitude']
	if 'time' in vars:
		dx['time'] = d['time']
	if 'time_bnds' in vars:
		args = [] if tlim is None else [tlim[0], tlim[1]]
		dx['time_bnds'] = misc.time_bnds(d['time'], None, *args)
	if 'backscatter' in vars:
		dx['backscatter'] = d['beta_raw']*1e-11*CALIBRATION_COEFF
	if 'zfull' in vars:
		zfull1 = d['range'] + dx['altitude']
		dx['zfull'] = np.tile(zfull1, (n, 1))
	for var in keep_vars:
		misc.keep_var(var, d, dx)
	return dx
