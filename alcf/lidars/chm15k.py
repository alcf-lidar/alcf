import numpy as np
import ds_format as ds

WAVELENGTH = 1064
CALIBRATION_COEFF = 1.0

VARS = {
	'backscatter': ['time', 'range', 'beta_raw'],
	'time': ['time'],
	'zfull': ['range', 'altitude'],
}

def read(filename, vars):
	dep_vars = list(set([y for x in vars if x in VARS for y in VARS[x]]))
	d = ds.from_netcdf(
		filename,
		dep_vars,
	)
	dx = {}
	n, m = d['beta_raw'].shape
	if 'time' in vars:
		dx['time'] = d['time']/(24.0*60.0*60.0) + 2416480.5
	if 'backscatter' in vars:
		dx['backscatter'] = d['beta_raw']*1e-11
	if 'zfull' in vars:
		zfull1 = d['range'] + d['altitude']
		dx['zfull'] = np.tile(zfull1, (n, 1))
	dx['.'] = {
		'time': {
			'.dims': ['time'],
			'long_name': 'time',
			'units': 'days since -4712-01-01 12:00',
			'calendar': 'gregorian',
		},
		'zfull': {
			'.dims': ['time', 'level'],
			'standard_name': 'height_above_reference_ellipsoid',
			'units': 'm',
		},
		'backscatter': {
			'.dims': ['time', 'level'],
			'long_name': 'backscatter',
			'units': 'm-1 sr-1',
		},
	}
	dx['.'] = {
		x: dx['.'][x]
		for x in vars
	}
	return dx
