import os
from misc import parse_time

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

- input: input filename or directory
- output: output filename or directory
- start: start time (see Time format below)
- end: end time (see Time format below)

Time format:

"YYYY-MM-DD[THH:MM[:SS]]", where YYYY is year, MM is month, DD is day,
HH is hour, MM is minute, SS is second. Example: 2000-01-01T00:00:00.
	"""
	time_jd = parse_time(time) if time is not None else None

	if os.path.isdir(input_):
		files = os.listdir(input_)
		for file in files:
			filename = os.path.join(input_, file)
			if not os.path.isfile():
				continue
			if time_jd is not None:
				d = ds.read(file, ['time'])

			else:
				d = ds.read(file, VARIABLES)
