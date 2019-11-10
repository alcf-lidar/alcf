import numpy as np
import ds_format as ds
import datetime as dt

WAVELENGTH = 910
CALIBRATION_COEFF = 1.0
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

CALIBRATION_CONST = 5e-3

def read(filename, vars):
	dep_vars = list(set([y for x in vars if x in VARS for y in VARS[x]]))
	required_vars = dep_vars + DEFAULT_VARS
	d = ds.from_netcdf(
		filename,
		required_vars
	)
	dx = {}
	dx['time'] = d['time']/(24.0*60.0*60.0) + 2440587.5
	n = len(dx['time'])
	range_ = d['vertical_resolution'][0]*d['level']
	zfull1 = range_
	dx['zfull'] = np.tile(zfull1, (n, 1))
	if 'backscatter' in vars:
		dx['backscatter'] = d['backscatter']*CALIBRATION_CONST
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
			'.dims': ['time', 'range'],
			'long_name': 'total_attenuated_backscatter_coefficient',
			'units': 'm-1 sr-1'
		},
	}
	dx['.'] = {
		x: dx['.'][x]
		for x in vars
		if x in dx['.']
	}
	return dx
