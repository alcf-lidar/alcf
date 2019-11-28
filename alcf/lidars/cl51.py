import numpy as np
import ds_format as ds
import datetime as dt
from alcf.lidars import META

WAVELENGTH = 910
CALIBRATION_COEFF = 3e-3
SURFACE_LIDAR = True
SC_LR = 18.8 # Stratocumulus lidar ratio (O'Connor et al., 2004)

VARS = {
	'backscatter': ['backscatter'],
}

DEFAULT_VARS = [
	'vertical_resolution',
	'level',
	'time',
]

def read(filename, vars, altitude=None):
	dep_vars = list(set([y for x in vars if x in VARS for y in VARS[x]]))
	required_vars = dep_vars + DEFAULT_VARS
	d = ds.from_netcdf(
		filename,
		required_vars
	)
	dx = {}
	dx['time'] = d['time']/(24.0*60.0*60.0) + 2440587.5
	n = len(dx['time'])
	if 'zfull' in vars:
		range_ = d['vertical_resolution'][0]*d['level']
		zfull1 = range_
		dx['zfull'] = np.tile(zfull1, (n, 1))
		if altitude is not None:
			dx['zfull'] += altitude
	if 'backscatter' in vars:
		dx['backscatter'] = d['backscatter']*CALIBRATION_COEFF
	if 'altitude' in vars:
		dx['altitude'] = np.full(n, altitude, np.float64)
	dx['.'] = META
	dx['.'] = {
		x: dx['.'][x]
		for x in vars
		if x in dx['.']
	}
	return dx
