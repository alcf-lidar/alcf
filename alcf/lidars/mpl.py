import numpy as np
import ds_format as ds
import datetime as dt
import warnings
from alcf import misc
from alcf.lidars import META

WAVELENGTH = 532 # nm
CALIBRATION_COEFF = 0.375e-5
SURFACE_LIDAR = True
SC_LR = 16.0 # sr
MAX_RANGE = 30000 # m

VARS = {
	'backscatter': ['copol_nrb', 'crosspol_nrb'],
	'backscatter_x': ['copol_nrb', 'crosspol_nrb'],
	'backscatter_y': ['copol_nrb', 'crosspol_nrb'],
}

TIME_VARS = [
	'year',
	'month',
	'day',
	'hour',
	'minute',
	'second',
]

DEFAULT_VARS = TIME_VARS + [
	'range_nrb',
	'elevation_angle',
	'altitude',
	'latitude',
	'longitude',
]

def parse_temporal_resolution(s):
	errmsg = 'Unrecognized temporal resolution "%s"' % s
	x = s.split(' ')
	if len(x) != 2:
		raise ValueError(errmsg)
	FACTOR = [
		[['s', 'sec', 'second', 'seconds'], 1./60./60./24.],
		[['m', 'min', 'minute', 'minutes'], 1./60./24.],
		[['h', 'hour', 'hours'], 1./24.],
	]
	try:
		f = float(x[0])
	except:
		raise ValueError(errmsg)
	for item in FACTOR:
		if x[1] in item[0]:
			return f*item[1]
	raise ValueError(errmsg)

def convert_time(d, tlim):
	time = np.array([
		(
			dt.datetime(int(y), int(m), int(day), int(H), int(M), int(S)) -
			dt.datetime(1970, 1, 1)
		).total_seconds()/(24*60*60) + 2440587.5
		for y, m, day, H, M, S
		in zip(d['year'], d['month'], d['day'], d['hour'], d['minute'], d['second'])
	], np.float64)
	tres = parse_temporal_resolution(d['.']['.']['temporal_resolution'])
	args = [] if tlim is None else [tlim[0], tlim[1]]
	time_bnds = misc.time_bnds(time, tres, *args)
	return time, time_bnds, tres

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
		d = ds.read(filename, TIME_VARS)
		misc.require_vars(d, ['time'])
		d['time'], d['time_bnds'], tres = convert_time(d)
		mask = misc.time_mask(d['time_bnds'], tlim[0], tlim[1])
		if np.sum(mask) == 0: return None
		sel = {'time': mask}

	dep_vars = misc.dep_vars(VARS, vars)
	req_vars = dep_vars + DEFAULT_VARS + keep_vars
	with warnings.catch_warnings():
		warnings.filterwarnings('ignore', message='WARNING: valid_range not used since it\ncannot be safely cast to variable data type')
		d = ds.read(filename, req_vars, sel=sel, full=True)
	misc.require_vars(d, req_vars)
	dx = {}
	misc.populate_meta(dx, META, set(vars) & set(VARS))
	n = ds.dim(d, 'time')
	altitude = d['altitude'] if altitude is None else \
		np.full(n, altitude, np.float64)
	lon = d['longitude'] if lon is None else \
		np.full(n, lon, np.float64)
	lat = d['latitude'] if lat is None else \
		np.full(n, lat, np.float64)
	time, time_bnds, tres = convert_time(d, tlim)
	if 'time' in vars:
		dx['time'] = time
		# dx['time'] += 13.0/24.0
	if 'time_bnds' in vars:
		dx['time_bnds'] = time_bnds
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
	if 'lon' in vars:
		dx['lon'] = lon
	if 'lat' in vars:
		dx['lat'] = lat
	# if 'backscatter_x' in vars:
	# 	dx['backscatter_x'] = d['copol_nrb']*CALIBRATION_COEFF
	# if 'backscatter_y' in vars:
	# 	dx['backscatter_y'] = d['crosspol_nrb']*CALIBRATION_COEFF
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
	for var in keep_vars:
		misc.keep_var(var, d, dx, {'level': 'range_nrb'})
	return dx
