import numpy as np
import ds_format as ds

wavelength = 1064

VARS = {
	'backscatter': ['time', 'range', 'beta_raw'],
	'time': ['time'],
	'range': ['range'],
	'zfull': ['range', 'altitude'],
}

def read(filename, vars):
	dep_vars = list(set([y for x in vars if x in VARS for y in VARS[x]]))
	d = ds.from_netcdf(
		filename,
		dep_vars,
	)
	dx = {}
	if 'time' in vars:
		dx['time'] = d['time']/(24.0*60.0*60.0) + 2416480.5 # Julian date
	if 'backscatter' in vars:
		dx['backscatter'] = d['beta_raw']*1e-11
	if 'range' in vars:
		dx['range'] = d['range']
	if 'zfull' in vars:
		dx['zfull'] = d['range'] + d['altitude']
	dx['.'] = {
		'time': {
			'.dims': ['time'],
			'long_name': 'time',
			'units': 'days since -4712-01-01 12:00',
		},
		'range': {
			'.dims': ['range'],
			'long_name': 'range',
			'units': 'm',
		},
		'zfull': {
			'.dims': ['range'],
			'long_name': '',
			'units': 'm',
		},
		'backscatter': {
			'.dims': ['time', 'range'],
			'long_name': 'backscatter',
			'units': 'm-1 sr-1',
		},
	}
	dx['.'] = {
		x: dx['.'][x]
		for x in vars
	}
	return dx
