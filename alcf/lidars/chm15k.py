import numpy as np
import ds_format as ds
from alcf import misc
from alcf.lidars import META

WAVELENGTH = 1064 # nm
CALIBRATION_COEFF = 0.34
SURFACE_LIDAR = True
SC_LR = 18.2 # sr. Stratocumulus lidar ratio (O'Connor et al., 2004).
MAX_RANGE = 15400 # m

VARS = {
	'backscatter': ['beta_raw'],
	'time': ['time'],
	'time_bnds': ['time'],
	'zfull': ['range', 'altitude'],
	'altitude': ['altitude'],
	'lon': [],
	'lat': [],
}

def read(filename, vars, altitude=None, lon=None, lat=None, **kwargs):
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
		dx['time_bnds'] = misc.time_bnds(dx['time'], dx['time'][1] - dx['time'][0])
	if 'backscatter' in vars:
		dx['backscatter'] = d['beta_raw']*1e-11*CALIBRATION_COEFF
	if 'zfull' in vars:
		zfull1 = d['range'] + altitude
		dx['zfull'] = np.tile(zfull1, (n, 1))
	if 'altitude' in vars:
		dx['altitude'] = np.full(n, altitude, np.float64)
	if 'lon' in vars:
		dx['lon'] = np.full(n, lon, np.float64)
	if 'lat' in vars:
		dx['lat'] = np.full(n, lat, np.float64)
	dx['.'] = META
	dx['.'] = {
		x: dx['.'][x]
		for x in vars
		if x in VARS
	}
	return dx
