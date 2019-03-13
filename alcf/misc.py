def parse_time(time):
	if len(time) != 2:
		raise ValueError('Invalid time: %s' % `time`)
	start = aq.from_iso(time[0])
	end = aq.from_iso(time[1])
	if start is None or end is None:
		raise ValueError('Invalid time: %s' % `time`)
	return [start, end]
