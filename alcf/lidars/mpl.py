import numpy as np
import ds_format as ds
import datetime as dt

WAVELENGTH = 532
CALIBRATION_COEFF = 2e-6*1e1
SURFACE_LIDAR = True

VARS = {
	'backscatter': ['copol_nrb', 'crosspol_nrb'],
	'backscatter_x': ['copol_nrb', 'crosspol_nrb'],
	'backscatter_y': ['copol_nrb', 'crosspol_nrb'],
}

DEFAULT_VARS = [
	'range_nrb',
	'elevation_angle',
	'year',
	'month',
	'day',
	'hour',
	'minute',
	'second',
]

def read(filename, vars):
	dep_vars = list(set([y for x in vars if x in VARS for y in VARS[x]]))
	required_vars = dep_vars + DEFAULT_VARS
	d = ds.from_netcdf(
		filename,
		required_vars
	)
	mask = d['elevation_angle'] == 0.0
	dx = {}
	if 'time' in vars:
		dx['time'] = np.array([
			(dt.datetime(y, m, day, H, M, S) - dt.datetime(1970, 1, 1)).total_seconds()/(24.0*60.0*60.0) + 2440587.5
			for y, m, day, H, M, S
			in zip(d['year'], d['month'], d['day'], d['hour'], d['minute'], d['second'])
		], np.float64)
		# dx['time'] += 13.0/24.0
	if 'zfull' in vars:
		zfull1 = np.outer(
			np.sin(d['elevation_angle']/180.0*np.pi),
			d['range_nrb']*1e3
		)
		dx['zfull'] = np.tile(zfull1, (len(d['year']), 1))
	if 'backscatter' in vars:
		dx['backscatter'] = (d['copol_nrb'] + d['crosspol_nrb'])*CALIBRATION_COEFF
	# if 'backscatter_x' in vars:
	# 	dx['backscatter_x'] = d['copol_nrb']*CALIBRATION_COEFF
	# if 'backscatter_y' in vars:
	# 	dx['backscatter_y'] = d['crosspol_nrb']*CALIBRATION_COEFF
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
		# 'backscatter_x': {
		# 	'.dims': ['time', 'level'],
		# 	'long_name': 'copolarized_attenuated_backscatter_coefficient',
		# 	'units': 'm-1 sr-1',
		# },
		# 'backscatter_y': {
		# 	'.dims': ['time', 'level'],
		# 	'long_name': 'crosspolarized_attenuated_backscatter_coefficient',
		# 	'units': 'm-1 sr-1',
		# },
	}
	dx['.'] = {
		x: dx['.'][x]
		for x in vars
	}
	return dx
