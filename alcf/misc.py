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

def aggregate(dd, state, period, epsilon=1./86400.):
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
	r = (t + 0.5) % period
	t1 = state.get('t1', t - r)
	t2 = state.get('t2', t1 + period)
	for d in dd:
		if d is None:
			ddo += merge(ddb, t1, t2) + [None]
			break
		i1 = 0
		i = 0
		while i < len(d['time']):
			if not (d['time_bnds'][i,1] >= t2):
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
			r = (t + 0.5) % period
			t1 = max(t2, t - r)
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

def time_bnds(time, step, start=None, end=None):
	n = len(time)
	bnds = np.full((n, 2), np.nan, time.dtype)
	bnds[:,0] = time - step*0.5
	bnds[:,1] = time + step*0.5
	bnds[1:,0] = np.maximum(bnds[:-1,1], bnds[1:,0])
	bnds[:-1,1] = np.minimum(bnds[1:,0], bnds[:-1,1])
	if start is not None:
		bnds[0,0] = start
	if end is not None:
		bnds[-1,1] = end
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
