import numpy as np
import ds_format as ds
import datetime as dt
from alcf.lidars import META

WAVELENGTH = 532 # nm
CALIBRATION_COEFF = 3.75e-6
SURFACE_LIDAR = True
SC_LR = 16.0 # sr
MAX_RANGE = 30000 # m

VARIABLES = [
	'nrb_copol',
	'nrb_crosspol',
	'c',
	'bin_time',
	'time',
	'elevation_angle',
	'gps_altitude',
]

def read(filename, vars, altitude=None, **kwargs):
	d = ds.read(filename, VARIABLES, jd=True)
	mask = d['elevation_angle'] == 0.0
	dx = {}
	n, m = d['nrb_copol'].shape
	if altitude is None:
		altitude = d['gps_altitude']
	else:
		altitude = np.full(n, altitude, np.float64)
	if 'time' in vars:
		dx['time'] = d['time']
	if 'zfull' in vars:
		dx['zfull'] = np.full((n, m), np.nan, np.float64)
		for i in range(n):
			range_ = 0.5*d['bin_time'][i]*d['c']*(np.arange(m) + 0.5)
			dx['zfull'][i,:] = range_*np.sin(d['elevation_angle'][i]/180.0*np.pi)
			dx['zfull'][i,:] += altitude[i]
	if 'backscatter' in vars:
		dx['backscatter'] = (d['nrb_copol'] + 2.*d['nrb_crosspol'])*CALIBRATION_COEFF
	if 'altitude' in vars:
		dx['altitude'] = altitude
	dx['backscatter'] = dx['backscatter'][:,10:]
	dx['zfull'] = dx['zfull'][:,10:]
	dx['.'] = META
	dx['.'] = {
		x: dx['.'][x]
		for x in vars
		if x in dx['.']
	}
	return dx
