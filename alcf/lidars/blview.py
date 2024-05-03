import numpy as np
import ds_format as ds
from alcf import misc
from alcf.lidars import META

WAVELENGTH = 910 # nm
CALIBRATION_COEFF = 1e-9
SURFACE_LIDAR = True
SC_LR = 18.8 # sr. Stratocumulus lidar ratio (O'Connor et al., 2004).
MAX_RANGE = 15400 # m

VARS = {
	'backscatter': ['profile_data'],
	'zfull': ['range', 'altitude'],
	'altitude': ['altitude'],
}

DEFAULT_VARS = [
	'time',
]

def read(
	filename,
	vars,
	altitude=None,
	lon=None,
	lat=None,
	tlim=None,
	keep_vars=[],
	**kwargs
):
	sel = None
	if tlim is not None:
		d = ds.read(filename, 'time')
		misc.require_vars(d, ['time'])
		d['time'] = d['time']/86400. + 2440587.5
		d['time_bnds'] = misc.time_bnds(d['time'])
		mask = misc.time_mask(d['time_bnds'], tlim[0], tlim[1])
		if np.sum(mask) == 0: return None
		sel = { 'timeDim': mask }

	dep_vars = misc.dep_vars(VARS, vars)
	req_vars = dep_vars + DEFAULT_VARS + keep_vars
	d = ds.read(filename, req_vars, sel=sel, full=True)
	misc.require_vars(d, req_vars)
	dx = {}
	misc.populate_meta(dx, META, set(vars) & set(VARS))
	n = ds.dim(d, 'timeDim')
	m = ds.dim(d, 'range')
	d['time'] = d['time']/86400. + 2440587.5
	if 'time' in vars:
		dx['time'] = d['time']
	if 'time_bnds' in vars:
		args = [] if tlim is None else [tlim[0], tlim[1]]
		dx['time_bnds'] = misc.time_bnds(d['time'], None, *args)
	if 'altitude' in vars:
		dx['altitude'] = d['altitude'][:,0].astype(np.float64).filled(np.nan)
	if 'zfull' in vars:
		range_ = d['range'].astype(np.float64).filled(np.nan)
		dx['zfull'] = np.tile(range_, (n, 1))
		dx['zfull'] = (dx['zfull'].T + dx['altitude']).T
	if 'lon' in vars:
		dx['lon'] = np.full(n, lon, np.float64)
	if 'lat' in vars:
		dx['lat'] = np.full(n, lat, np.float64)
	if 'backscatter' in vars:
		profile_data = d['profile_data'].astype(np.float64).filled(np.nan)
		dx['backscatter'] = profile_data*CALIBRATION_COEFF
		j = np.max(np.nonzero(np.any(np.isfinite(dx['backscatter']), axis=0)))
		dx['backscatter'] = dx['backscatter'][:,:(j + 1)]
		if 'zfull' in vars:
			dx['zfull'] = dx['zfull'][:,:(j + 1)]
	for var in keep_vars:
		misc.keep_var(var, d, dx, {'time': 'timeDim', 'level': 'range'})
	return dx
