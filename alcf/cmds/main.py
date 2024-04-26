import sys
import re
from alcf.cmds import CMDS

def md_to_text(md):
	text = md.strip()
	text += '\n\nBug reporting\n-------------\n\nReport bugs to Peter Kuma (peter@peterkuma.net).\n'
	return text

def run(cmd=None, *args, **kwargs):
	'''alcf -- Tool for processing of automatic lidar and ceilometer (ALC) data and intercomparison with atmospheric models.
====

Synopsis
--------

    alcf <cmd> [<options>]
    alcf <cmd> --help

Arguments
---------

- `cmd`: See Commands below.
- `options`: Command options.

Commands
--------

- `auto`: Peform automatic processing of model or lidar data.
- `calibrate`: Calibrate lidar backscatter.
- `convert`: Convert input instrument or model data to the ALCF standard NetCDF.
- `download`: Download model data.
- `lidar`: Process lidar data.
- `model`: Extract model data at a point or along a track.
- `plot`: Plot lidar data.
- `simulate`: Simulate lidar measurements from model data using COSP.
- `stats`: Calculate cloud occurrence statistics.

Options
-------

- `--help`: Print help for command.
- `--debug`: Enable debugging information.
'''

	if cmd is None:
		sys.stderr.write(md_to_text(run.__doc__))
		return 1

	func = CMDS.get(cmd)
	if func is None:
		raise ValueError('Invalid command: %s' % cmd)
	try:
		func(*args, **kwargs)
	except TypeError as e:
		if str(e).startswith('run() '):
			sys.stderr.write(md_to_text(func.__doc__))
			return 1
		else:
			raise e
	return 0
