import numpy as np
import ds_format as ds
from alcf import misc
from alcf.lidars import META

WAVELENGTH = 910 # nm
CALIBRATION_COEFF = 1
SURFACE_LIDAR = True
SC_LR = 18.8 # sr. Stratocumulus lidar ratio (O'Connor et al., 2004).
MAX_RANGE = 15400 # m

VARS = {
	'backscatter': ['beta_att'],
	'time': ['time'],
	'time_bnds': ['time'],
	'zfull': ['time', 'range', 'elevation'],
	'altitude': ['time', 'elevation'],
	'lon': ['time'],
	'lat': ['time'],
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
	d = ds.read(filename, dep_vars, sel=sel)
	dx = {}
	if 'time' in vars:
		n = len(d['time'])
		dx['time'] = d['time']/86400. + 2440587.5
		if tres is None: tres = dx['time'][1] - dx['time'][0]
		dx['time_bnds'] = misc.time_bnds(dx['time'], tres)
	if 'altitude' in vars:
		if d['elevation'].ndim == 0:
			dx['altitude'] = np.full(n, d['elevation'], np.float64)
		else:
			dx['altitude'] = d['elevation']
	if 'zfull' in vars:
		dx['zfull'] = np.tile(d['range'], (n, 1))
		dx['zfull'] = (dx['zfull'].T + dx['altitude']).T
	if 'lon' in vars:
		dx['lon'] = np.full(n, lon, np.float64)
	if 'lat' in vars:
		dx['lat'] = np.full(n, lat, np.float64)
	if 'backscatter' in vars:
		dx['backscatter'] = d['beta_att']*CALIBRATION_COEFF
	dx['.'] = META
	dx['.'] = {
		x: dx['.'][x]
		for x in vars
		if x in VARS
	}
	return dx
