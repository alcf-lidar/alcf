import numpy as np
import ds_format as ds
import datetime as dt
from alcf import misc
from alcf.lidars import META

WAVELENGTH = 910 # nm
CALIBRATION_COEFF = 1.2e-3
SURFACE_LIDAR = True
SC_LR = 18.8 # sr. Stratocumulus lidar ratio (O'Connor et al., 2004).
MAX_RANGE = 15400 # m

VARS = {
	'backscatter': ['backscatter'],
}

DEFAULT_VARS = [
	'vertical_resolution',
	'level',
	'range',
	'time',
	'detection_status',
]

def read(filename, vars,
	altitude=None,
	lon=None,
	lat=None,
	calibration_coeff=CALIBRATION_COEFF,
	fix_cl_range=False,
	cl_crit_range=6000,
	time=None,
	**kwargs
):
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
	required_vars = dep_vars + DEFAULT_VARS

	d = ds.read(filename, required_vars, jd=True, sel=sel)
	dx = {}
	dx['time'] = d['time']
	if tres is None: tres = dx['time'][1] - dx['time'][0]
	dx['time_bnds'] = misc.time_bnds(dx['time'], tres)

	n = len(dx['time'])
	if 'range' in d: # ARM CL51 format.
		range_ = d['range']
	else: # Generic CL51 format.
		range_ = d['vertical_resolution'][0]*d['level']
	if 'zfull' in vars:
		zfull1 = range_
		dx['zfull'] = np.tile(zfull1, (n, 1))
		if altitude is not None:
			dx['zfull'] += altitude
	if 'backscatter' in vars:
		factor = 1e-4 if (d['.']['backscatter']['units'] == '1/(sr*km*10000)') \
			else 1 # Factor of 1e-4 if ARM CL51 format.
		dx['backscatter'] = d['backscatter']*calibration_coeff*factor
		mask = range_ > 6000
		if fix_cl_range is True:
			for i in range(n):
				if d['detection_status'][i] == b'0':
					dx['backscatter'][i,mask] *= (range_[mask]/6000)**2
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
		if x in dx['.']
	}
	return dx
