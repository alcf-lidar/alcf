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

def read(filename, vars, altitude=None, lon=None, lat=None, time=None, **kwargs):
	sel = None
	tres = None
	if time is not None:
		d = ds.read(filename, 'time', jd=True)
		tres = d['time'][1] - d['time'][0]
		d['time_bnds'] = misc.time_bnds(d['time'], tres)
		mask = misc.time_mask(d['time_bnds'], time[0], time[1])
		if np.sum(mask) == 0: return None
		sel = {'time': mask}

	dep_vars = list(set([y for x in vars if x in VARS for y in VARS[x]]))
	d = ds.read(filename, dep_vars, jd=True, sel=sel)
	dx = {}
	n, m = d['beta_raw'].shape
	if altitude is None:
		altitude = d['altitude']
	if 'time' in vars:
		dx['time'] = d['time']
		if tres is None: tres = dx['time'][1] - dx['time'][0]
		dx['time_bnds'] = misc.time_bnds(dx['time'], tres)
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
