import os
import ds_format as ds
from alcf.algorithms import interp
from alcf.algorithms import stats
from alcf.misc import parse_time

VARIABLES = [
	'cloud_mask',
	'zfull',
]

def run(input_, output, time=None):
	"""
alcf stats

Calculate cloud occurrence statistics.

Usage:

    alcf stats <input> <output> [time: { <start> <end> }]

Arguments:

- `input`: input filename or directory
- `output`: output filename or directory
- `start`: start time (see Time format below)
- `end`: end time (see Time format below)

Time format:

"YYYY-MM-DD[THH:MM[:SS]]", where YYYY is year, MM is month, DD is day,
HH is hour, MM is minute, SS is second. Example: 2000-01-01T00:00:00.
	"""
	time_jd = parse_time(time) if time is not None else None
	state = {}
	options = {}

	if os.path.isdir(input_):
		files = os.listdir(input_)
		for file in sorted(files):
			filename = os.path.join(input_, file)
			if not os.path.isfile(filename):
				continue
			d = ds.read(filename, VARIABLES)
			print('<- %s' % filename)
			dd = stats.stream([d], state, **options)
	dd = stats.stream([None], state, **options)
	print('-> %s' % output)
	ds.to_netcdf(output, dd[0])
