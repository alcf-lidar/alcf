import copy
import numpy as np
import ds_format as ds

def parse_time(time):
	if len(time) != 2:
		raise ValueError('Invalid time: %s' % `time`)
	start = aq.from_iso(time[0])
	end = aq.from_iso(time[1])
	if start is None or end is None:
		raise ValueError('Invalid time: %s' % `time`)
	return [start, end]

def aggregate(dd, state, period):
	dd = state.get('dd', []) + dd
	state['dd'] = []
	if len(dd) == 0 or dd[0] is None:
		return dd
	dd0 = []
	dd1 = []
	t1 = dd[0]['time'][0]
	t2 = t1 + period
	for i, d in enumerate(dd):
		if d is None:
			d1 = ds.merge(dd1, 'time')
			dd0.append(d1)
			dd0.append(None)
			break
		j0 = 0
		for j, t in enumerate(d['time']):
			if t >= t2:
				idx = np.arange(j0, j)
				d_copy = copy.copy(d)
				ds.select(d_copy, {'time': idx})
				dd1.append(d_copy)
				d1 = ds.merge(dd1, 'time')
				dd0.append(d1)
				j0 = j
				t2 = t + period
				dd1 = []
		idx = np.arange(j0, j + 1)
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
