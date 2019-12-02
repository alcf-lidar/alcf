import copy
import numpy as np
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

def aggregate(dd, state, period):
	dd = state.get('dd', []) + dd
	state['dd'] = []
	if len(dd) == 0 or dd[0] is None:
		return dd
	dd0 = []
	dd1 = []
	t1 = dd[0]['time'][0] - ((dd[0]['time'][0] + 0.5) % 1.0)
	t2 = t1 + period
	for i, d in enumerate(dd):
		if d is None:
			d1 = ds.merge(dd1, 'time')
			dd0.append(d1)
			dd0.append(None)
			break
		j0 = 0
		j = 0
		while j < len(d['time']):
			t = d['time'][j]
			if t >= t2:
				idx = np.arange(j0, j)
				if len(idx) > 0:
					d_copy = copy.copy(d)
					ds.select(d_copy, {'time': idx})
					dd1.append(d_copy)
				if len(dd1) > 0:
					d1 = ds.merge(dd1, 'time')
					dd0.append(d1)
				j0 = j
				t2 = t + period
				dd1 = []
			j += 1
		idx = np.arange(j0, len(d['time']))
		if len(idx) > 0:
			d_copy = copy.copy(d)
			ds.select(d_copy, {'time': idx})
			dd1.append(d_copy)
	state['dd'] = dd1
	return dd0

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

def time_bnds(time, step):
	n = len(time)
	bnds = np.full((n, 2), np.nan, time.dtype)
	bnds[0,0] = time[0] - step
	bnds[-1,1] = time[-1] + step
	if n < 2:
		return bnds
	m = 0.5*(time[1:] + time[:(n - 1)])
	bnds[1:,0] = m
	bnds[:-1,1] = m
	for i in range(n):
		bnds[i,0] = max(bnds[i,0], time[i] - step)
		bnds[i,1] = min(bnds[i,1], time[i] + step)
	return bnds
