import numpy as np
import ds_format as ds
from alcf.lidars import META

WAVELENGTH = 1064 # nm
CALIBRATION_COEFF = 0.34
SURFACE_LIDAR = True
SC_LR = 18.2 # sr. Stratocumulus lidar ratio (O'Connor et al., 2004).
MAX_RANGE = 15400 # m

VARS = {
	'backscatter': ['beta_raw'],
	'time': ['time'],
	'zfull': ['range', 'altitude'],
	'altitude': ['altitude'],
}

def read(filename, vars, altitude=None, **kwargs):
	dep_vars = list(set([y for x in vars if x in VARS for y in VARS[x]]))
	d = ds.from_netcdf(
		filename,
		dep_vars,
	)
	dx = {}
	n, m = d['beta_raw'].shape
	if altitude is None:
		altitude = d['altitude']
	if 'time' in vars:
		dx['time'] = d['time']/(24.0*60.0*60.0) + 2416480.5
	if 'backscatter' in vars:
		dx['backscatter'] = d['beta_raw']*1e-11*CALIBRATION_COEFF
	if 'zfull' in vars:
		zfull1 = d['range'] + altitude
		dx['zfull'] = np.tile(zfull1, (n, 1))
	if 'altitude' in vars:
		dx['altitude'] = np.full(n, altitude, np.float64)
	dx['.'] = META
	dx['.'] = {
		x: dx['.'][x]
		for x in vars
		if x in VARS
	}
	return dx
