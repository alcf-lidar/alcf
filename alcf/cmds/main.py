import sys
from alcf.cmds import CMDS

def run(cmd=None, *args, **kwargs):
	"""
alcf - Tool for processing of automatic lidar and ceilometer (ALC) data
and intercomparison with atmospheric models.

Usage:

    alcf <cmd> [<options>]
    alcf <cmd> --help

Arguments:

- `cmd`: see Commands below
- `options`: command options

Options:

`--help`: print help for command
`--debug`: Enable debugging information.

Commands:

- `convert`: convert input instrument or model data to ALCF standard NetCDF
- `model`: extract model data at a point or along a track
- `cosp`: simulate lidar measurements from model data using COSP
- `lidar`: process lidar data
- `stats`: calculate cloud occurrence statistics
- `plot`: plot lidar data
- `plot_stats`: plot lidar statistics
	"""

	if cmd is None:
		sys.stderr.write(run.__doc__.strip() + '\n')
		return 1

	func = CMDS.get(cmd)
	if func is None:
		raise ValueError('Invalid command: %s' % cmd)
	try:
		func(*args, **kwargs)
	except TypeError as e:
		if str(e).startswith('run() '):
			sys.stderr.write(func.__doc__.replace('`', '').strip() + '\n')
			return 1
		else:
			raise e
	return 0
