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
	'time': ['time'],
	'time_bnds': ['time'],
	'zfull': ['time', 'range', 'altitude'],
	'altitude': ['time', 'altitude'],
	'lon': ['time'],
	'lat': ['time'],
}

def read(filename, vars, altitude=None, lon=None, lat=None, **kwargs):
	dep_vars = list(set([y for x in vars if x in VARS for y in VARS[x]]))
	d = ds.read(filename, dep_vars)
	dx = {}
	if 'time' in vars:
		n = len(d['time'])
		dx['time'] = d['time']/86400. + 2440587.5
		dx['time_bnds'] = misc.time_bnds(dx['time'], dx['time'][1] - dx['time'][0])
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
		n, m = dx['backscatter'].shape
		j = np.max(np.nonzero(np.any(np.isfinite(dx['backscatter']), axis=0)))
		dx['backscatter'] = dx['backscatter'][:,:(j + 1)]
		if 'zfull' in vars:
			dx['zfull'] = dx['zfull'][:,:(j + 1)]
	dx['.'] = META
	dx['.'] = {
		x: dx['.'][x]
		for x in vars
		if x in VARS
	}
	return dx
