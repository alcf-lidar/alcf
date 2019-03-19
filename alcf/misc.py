def parse_time(time):
	if len(time) != 2:
		raise ValueError('Invalid time: %s' % `time`)
	start = aq.from_iso(time[0])
	end = aq.from_iso(time[1])
	if start is None or end is None:
		raise ValueError('Invalid time: %s' % `time`)
	return [start, end]

def aggregate(dd, state, period):
	state['dd'].append(dd)
	time = np.concatenate(d['time'] for d in state['dd'])
	t1 = time[0]
	t2 = t1 + period
	dd0 = []
	for i, d in enumerate(state['dd']):
		mask = d['time'] < t2
		if np.sum(mask) > 0:
			d0 = ds.select(d, {'time': mask})
			dd0.append(d0)
		else:
			break
	state['dd'] = state['dd'][i:]
	return [ds.merge(dd0, 'time')]
