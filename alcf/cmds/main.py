import sys
import re
from alcf import __version__
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

    alcf <cmd> [<options>] [<arguments>]
    alcf [<cmd>] --help
    alcf --version

Arguments
---------

- `cmd`: See Commands below.
- `arguments`: Command arguments. Use `alcf <cmd> --help` for more information.
- `options`: Command options (see Options below).

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

- `--debug`: Enable debugging information.
- `--help`: Print general help or help for a command and exit.
- `--version`: Print version and exit.
'''
	if 'version' in kwargs:
		print(__version__)
		return 0

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
