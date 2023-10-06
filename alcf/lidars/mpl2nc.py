import numpy as np
import ds_format as ds
import datetime as dt
from alcf import misc
from alcf.lidars import META

WAVELENGTH = 532 # nm
CALIBRATION_COEFF = 3.75e-6
SURFACE_LIDAR = True
SC_LR = 16.0 # sr
MAX_RANGE = 30000 # m

VARS = {
	'backscatter': ['nrb_copol', 'nrb_crosspol'],
	'zfull': ['bin_time', 'c'],
}

DEFAULT_VARS = [
	'time',
	'elevation_angle',
	'gps_altitude',
	'gps_latitude',
	'gps_longitude',
]

def read(
	filename,
	vars,
	altitude=None,
	lon=None,
	lat=None,
	tlim=None,
	keep_vars=[],
	**kwargs
):
	sel = None
	tres = None
	if tlim is not None:
		d = ds.read(filename, 'time', jd=True)
		tres = d['time'][1] - d['time'][0]
		d['time_bnds'] = misc.time_bnds(d['time'], tres)
		mask = misc.time_mask(d['time_bnds'], tlim[0], tlim[1])
		if np.sum(mask) == 0: return None
		sel = {'profile': mask}

	dep_vars = misc.dep_vars(VARS, vars)
	req_vars = dep_vars + DEFAULT_VARS + keep_vars
	d = ds.read(filename, req_vars, jd=True, sel=sel, full=True)
	mask = d['elevation_angle'] == 0.0
	dx = {}
	misc.populate_meta(dx, META, set(vars) & set(VARS))
	n = ds.dim(d, 'profile')
	m = ds.dim(d, 'range')
	altitude = d['gps_altitude'] if altitude is None else \
		np.full(n, altitude, np.float64)
	lon = d['gps_longitude'] if lon is None else \
		np.full(n, lon, np.float64)
	lat = d['gps_latitude'] if lat is None else \
		np.full(n, lat, np.float64)
	if 'time' in vars:
		dx['time'] = d['time']
	if 'time_bnds' in vars:
		if tres is None: tres = d['time'][1] - d['time'][0]
		args = [] if tlim is None else [tlim[0], tlim[1]]
		dx['time_bnds'] = misc.time_bnds(d['time'], tres, *args)
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
	if 'lon' in vars:
		dx['lon'] = lon
	if 'lat' in vars:
		dx['lat'] = lat
	for var in keep_vars:
		misc.keep_var(var, d, dx, {'time': 'profile', 'level': 'range'})
	return dx
