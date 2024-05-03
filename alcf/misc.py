import copy
import numpy as np
import astropy.coordinates
import astropy.time
import astropy.units
import ds_format as ds
import aquarius_time as aq

def parse_time(time):
	if len(time) != 2:
		raise ValueError('Invalid time: %s' % time)
	start = aq.from_iso(time[0])
	end = aq.from_iso(time[1])
	if start is None or end is None:
		raise ValueError('Invalid time: %s' % time)
	return [start, end]

def aggregate(dd, state, period, epsilon=1./86400., align=True):
	dd = state.get('dd', []) + dd
	state['dd'] = []

	if len(dd) == 0 or dd[0] is None:
		return dd

	def merge(dd, t1, t2):
		if len(ddb) > 0:
			dx = ds.merge(ddb, 'time')
			dx['time_bnds'][0,0] = max(t1, dx['time_bnds'][0,0])
			dx['time_bnds'][-1,1] = min(t2, dx['time_bnds'][-1,1])
			if dx['time_bnds'][-1,1] > dx['time_bnds'][0,0]:
				return [dx]
		return []

	ddo = []
	ddb = []
	t = dd[0]['time_bnds'][0,0]
	if align:
		r = (t + 0.5 + epsilon) % period
		t1 = state.get('t1', t - r + epsilon)
	else:
		t1 = state.get('t1', t)
	t2 = state.get('t2', t1 + period)
	for d in dd:
		if d is None:
			ddo += merge(ddb, t1, t2) + [None]
			break
		i1 = 0
		i = 0
		while i < len(d['time']):
			if not (d['time_bnds'][i,1] - t2 > epsilon):
				i += 1
				continue
			ii = np.arange(i1, i + (t2 - d['time_bnds'][i,0] > epsilon))
			if len(ii) > 0:
				dx = copy.copy(d)
				ds.select(dx, {'time': ii})
				ddb += [dx]
			ddo += merge(ddb, t1, t2)
			i1 = i
			t = d['time_bnds'][i,0]
			if align:
				r = (t + 0.5 + epsilon) % period
				t1 = max(t2, t - r + epsilon)
			else:
				t1 = max(t2, t)
			t2 = t1 + period
			ddb = []
		ii = np.arange(i1, len(d['time']))
		if len(ii) > 0:
			dx = copy.copy(d)
			ds.select(dx, {'time': ii})
			ddb += [dx]
	state['dd'] = ddb
	state['t1'] = t1
	state['t2'] = t2
	return ddo

def stream(dd, state, f, **options):
	dd = dd + state.get('dd', [])
	i = 0
	for i, d in enumerate(dd):
		if d is None:
			break
		f(d, **options)
	state['dd'] = []
	return dd[:(i+1)]

def half(xfull):
	xhalf = np.zeros(len(xfull) + 1, dtype=xfull.dtype)
	xhalf[1:-1] = 0.5*(xfull[1:] + xfull[:-1])
	xhalf[0] = 2.*xfull[0] - xfull[1]
	xhalf[-1] = 2.*xfull[-1] - xfull[-2]
	return xhalf

def time_bnds(time, step=None, start=None, end=None):
	n = len(time)
	if step is None:
		if len(time) < 2:
			raise ValueError('Too few profiles to determine temporal resolution')
		step = time[1] - time[0]
	bnds = np.full((n, 2), np.nan, time.dtype)
	bnds[:,0] = time - step*0.5
	bnds[:,1] = time + step*0.5
	bnds[1:,0] = np.maximum(bnds[:-1,1], bnds[1:,0])
	bnds[:-1,1] = np.minimum(bnds[1:,0], bnds[:-1,1])
	if start is not None:
		bnds[0,0] = max(bnds[0,0], start)
	if end is not None:
		bnds[-1,1] = min(bnds[-1,1], end)
	return bnds

def sun_altitude(t, lon, lat):
	loc = astropy.coordinates.EarthLocation(
		lon=lon*astropy.units.deg,
		lat=lat*astropy.units.deg
	)
	time = astropy.time.Time(t, format='jd')
	altaz = astropy.coordinates.AltAz(location=loc, obstime=time)
	sun = astropy.coordinates.get_sun(time)
	return sun.transform_to(altaz).alt.hour/24.*360.

def require_vars(d, variables):
	for v in variables:
		if v not in d:
			raise ValueError('Variable "%s" is required' % v)

def geo_distance(lon1, lat1, lon2, lat2, method='gc'):
	lon1, lat1, lon2, lat2 = [x/180*np.pi for x in (lon1, lat1, lon2, lat2)]
	if method == 'gc':
		x = np.sin(lat1)*np.sin(lat2) + \
			np.cos(lat1)*np.cos(lat2)*np.cos(lon1 - lon2)
		return 6371*(np.arccos(np.maximum(np.minimum(x, 1), -1)))
	elif method == 'hs':
		dlon = lon2 - lon1
		dlat = lat2 - lat1
		a = np.sin(dlat/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2
		return 2*6371*np.arcsin(np.sqrt(a))
	else:
		raise ValueError('Unrecognized method "%s"' % method)

def time_mask(bnds, t1, t2):
	return ~(((bnds[:,0] < t1) & (bnds[:,1] < t1)) |
	         ((bnds[:,0] > t2) & (bnds[:,1] > t2)))

def track_at(d, t, epsilon=1/86400):
	i = np.searchsorted(d['time_bnds'][:,0], t, side='right')
	if i == 0:
		if t >= d['time_bnds'][0,0] - epsilon:
			return d['lon'][0], d['lat'][0]
		else:
			return np.nan, np.nan
	if t <= d['time_bnds'][i-1,1] + epsilon:
		return d['lon'][i-1], d['lat'][i-1]
	return np.nan, np.nan

def populate_meta(d, meta, vars):
	d_tmp = {'.': meta}
	for var in vars:
		ds.meta(d, var, ds.meta(d_tmp, var))
	ds.meta(d, None, ds.meta(d_tmp))

def keep_var(var, d, do, dim_map={}):
	dim_map_rev = dict((v, k) for k, v in dim_map.items())
	if var in ds.vars(d) and dim_map.get('time', 'time') in ds.dims(d, var):
		name = 'input_' + var
		ds.var(do, name, ds.var(d, var).astype(np.float64))
		dims = [dim_map_rev.get(dim, dim) for dim in ds.dims(d, var)]
		ds.dims(do, name, dims)
		ds.attrs(do, name, ds.attrs(d, var))
		ds.rm_attr(do, '_FillValue', name)

def dep_vars(mapping, vars):
	return list(set([y for x in vars if x in mapping for y in mapping[x]]))

def point_to_track(point, time):
	time_mid = 0.5*(time[0] + time[1])
	return {
		'lon': np.array([point[0] % 360, point[0] % 360], dtype=np.float64),
		'lat': np.array([point[1], point[1]], dtype=np.float64),
		'time': np.array([time[0], time[1]], dtype=np.float64),
		'time_bnds': np.array([[time[0], time_mid], [time_mid, time[1]]],
			dtype=np.float64),
	}

def track_auto_time_bnds(time, track_gap=0):
	n = len(time)
	time_bnds = np.full((n, 2), np.nan, np.float64)
	time_bnds[0,0] = time[0]
	time_bnds[-1,1] = time[-1]
	time_avg = 0.5*(time[:-1] + time[1:])
	time_bnds[1:,0] = time_avg
	time_bnds[:-1,1] = time_avg
	if track_gap != 0:
		time_diff = time[1:] - time[:-1]
		mask1 = np.full(n, False, bool)
		mask2 = np.full(n, False, bool)
		mask1[:-1] = time_diff > track_gap
		mask2[1:] = time_diff > track_gap
		time_bnds[mask1,1] = time[mask1]
		time_bnds[mask2,0] = time[mask2]
	return time_bnds

def read_track(filenames, lon_180=False, track_gap=0):
	if type(filenames) not in [list, tuple]:
		filenames = [filenames]
	dd = []
	for filename in filenames:
		d = ds.read(filename, jd=True)
		if len(d['time']) < 2:
			raise ValueError('%s: Track must contain at least two records', filename)
		if 'time_bnds' not in d:
			d['time_bnds'] = track_auto_time_bnds(d['time'], track_gap)
			d['.']['time_bnds'] = {
				'.dims': ['time', 'bnds'],
				'long_name': 'time bounds',
				'standard_name': 'time',
				'units': 'days since -4713-11-24 12:00 UTC',
				'calendar': 'proleptic_gregorian',
			}
		dd += [d]
	d = ds.merge(dd, 'time')
	d['lon'] = d['lon'] % 360
	return d

def track_has_seg(track, t1, t2):
	mask = (track['time_bnds'][:,0] < t2) & (track['time_bnds'][:,1] >= t1)
	return np.any(mask)

def cmd_point_or_track(point, time, track, track_gap=0):
	time_lim = [-np.inf, np.inf]
	if time is not None:
		for i in [0, 1]:
			time_lim[i] = aq.from_iso(time[i])
			if time_lim[i] is None:
				raise ValueError('Invalid time format: %s' % time[i])
	d = None
	if track is not None:
		d = read_track(track, track_gap/86400.)
	elif point is not None and time is not None:
		d = point_to_track(point, time_lim)
	else:
		raise ValueError('Point and time or track is required')
	return d, time_lim
