import numpy as np
import ds_format as ds
import datetime as dt
from alcf.lidars import META

WAVELENGTH = 532
CALIBRATION_COEFF = 0.375e-5
SURFACE_LIDAR = True
SC_LR = 16.0
MAX_RANGE = 30000

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
	'altitude',
]

def read(filename, vars, altitude=None, **kwargs):
	dep_vars = list(set([y for x in vars if x in VARS for y in VARS[x]]))
	required_vars = dep_vars + DEFAULT_VARS
	d = ds.from_netcdf(
		filename,
		required_vars
	)
	mask = d['elevation_angle'] == 0.0
	dx = {}
	n = len(d['year'])
	if altitude is None:
		altitude = d['altitude']
	else:
		altitude = np.full(n, altitude, np.float64)
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
		dx['zfull'] = np.tile(zfull1, (n, 1))
		for i in range(n):
			dx['zfull'][i,:] += altitude[i]
	if 'backscatter' in vars:
		dx['backscatter'] = (d['copol_nrb'] + 2.*d['crosspol_nrb'])*CALIBRATION_COEFF
	if 'altitude' in vars:
		dx['altitude'] = altitude
	# if 'backscatter_x' in vars:
	# 	dx['backscatter_x'] = d['copol_nrb']*CALIBRATION_COEFF
	# if 'backscatter_y' in vars:
	# 	dx['backscatter_y'] = d['crosspol_nrb']*CALIBRATION_COEFF
	dx['.'] = META
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
	dx['.'] = {
		x: dx['.'][x]
		for x in vars
		if x in dx['.']
	}
	return dx
