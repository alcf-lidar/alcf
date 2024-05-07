import os
import sys
import numpy as np
import ds_format as ds
import alcf
from alcf.algorithms import stats
from alcf import misc

VARIABLES = [
	'cloud_mask',
	'cbh',
	'zfull',
	'time',
	'time_bnds',
	'backscatter',
	'backscatter_sd',
	'backscatter_mol',
	'lon',
	'lat',
]

def read_filters(filters):
	if type(filters) in [list, tuple]:
		return [ds.read(filename) for filename in filters]
	else:
		return [ds.read(filters)]

def run(input_, output,
	tlim=None,
	blim=[5., 200.],
	bres=5.,
	bsd_lim=[0.001, 10.],
	bsd_log=True,
	bsd_res=0.001,
	bsd_z=8000.,
	filter=None,
	filter_exclude=None,
	filter_include=None,
	zlim=[0., 15000.],
	zres=100.,
	interp='area_block',
	**kwargs
):
	'''
alcf-stats -- Calculate cloud occurrence statistics.
==========

Synopsis
--------

    alcf stats [<options>] [--] <input> <output>

Description
-----------

Arguments following `--` are treated as literal strings. Use this delimiter if the input or output file names might otherwise be interpreted as non-strings, e.g. purely numerical file names.

Arguments
---------

- `input`: Input filename or directory.
- `output`: Output filename or directory.

Options
-------

- `blim: <value>`: Backscatter histogram limits (10^-6 m-1.sr-1). Default: `{ 5 200 }`.
- `bres: <value>`: Backscatter histogram resolution (10^-6 m-1.sr-1). Default: `10`.
- `bsd_lim: { <low> <high> }`: Backscatter standard deviation histogram limits (10^-6 m-1.sr-1). Default: `{ 0.001 10 }`.
- `bsd_log: <value>`: Enable/disable logarithmic scale of the backscatter standard deviation histogram (`true` or `false`). Default: `true`.
- `bsd_res: <value>`: Backscatter standard deviation histogram resolution (10^-6 m-1.sr-1). Default: `0.001`.
- `bsd_z: <value>`: Backscatter standard deviation histogram height (m). Default: `8000`.
- `filter: <value> | { <value> ... }`: Filter profiles by condition: `cloudy` for cloudy profiles only, `clear` for clear sky profiles only, `night` for nighttime profiles, `day` for daytime profiles, `none` for all profiles. If an array of values is supplied, all conditions must be true. For `night` and `day`, lidar profiles must contain valid longitude and latitude fields set via the `lon` and `lat` arguments of `alcf lidar` or read implicitly from raw lidar data files if available (mpl, mpl2nc). Default: `none`.
- `filter_exclude: <value> | { <value>... }`: Filter by a mask defined in a NetCDF file, described below under Filter file. If multiple files are supplied, they must all apply for a profile to be excluded.
- `filter_include: <value> | { <value>... }`: The same as `filter_exclude`, but with time intervals to be included in the result. If both are defined, `filter_include` takes precedence. If multiple files are supplied, they must all apply for a profile to be included.
- `interp: <value>`: Vertical interpolation method. `area_block` for area-weighting with block interpolation, `area_linear` for area-weighting with linear interpolation or `linear` for simple linear interpolation. Default: `area_block`.
- `tlim: { <start> <end> }`: Time limits (see Time format below). Default: `none`.
- `zlim: { <low> <high> }`: Height limits (m). Default: `{ 0 15000 }`.
- `zres: <value>`: Height resolution (m). Default: `50`.

Time format
-----------

`YYYY-MM-DD[THH:MM[:SS]]`, where `YYYY` is year, `MM` is month, `DD` is day, `HH` is hour, `MM` is minute, `SS` is second. Example: `2000-01-01T00:00:00`.

Filter file
----------

The NetCDF file must define a variable `time_bnds` (float64), which are time intervals to be excluded from or included in the result. `time_bnds` must have two dimensions `time` of an arbitrary size and `bnds` of size 2. The first and second column of the variable should contain the start and end of the interval, respectively. `time_bnds` must be valid time in accordance with the CF Conventions.

Examples
--------

Calculate statistics from processed lidar data in `alcf_cl51_lidar` and store the output in `alcf_cl51_stats.nc`.

    alcf stats alcf_cl51_lidar alcf_cl51_stats.nc
	'''
	tlim_jd = misc.parse_time(tlim) if tlim is not None else None
	state = {}
	options = {
		'tlim': tlim_jd,
		'blim': np.array(blim, dtype=np.float64)*1e-6,
		'bres': bres*1e-6,
		'bsd_lim': np.array(bsd_lim, dtype=np.float64)*1e-6,
		'bsd_log': bsd_log,
		'bsd_res': bsd_res*1e-6,
		'bsd_z': bsd_z,
		'filter': filter if type(filter) is list else [filter],
		'zlim': zlim,
		'zres': zres,
		'interp': interp,
	}

	if filter_exclude is not None:
		dd = read_filters(filter_exclude)
		options['filters_exclude'] = [d['time_bnds'] for d in dd]

	if filter_include is not None:
		dd = read_filters(filter_include)
		options['filters_include'] = [d['time_bnds'] for d in dd]

	if os.path.isdir(input_):
		files = sorted(os.listdir(input_))
		for file_ in files:
			filename = os.path.join(input_, file_)
			if not os.path.isfile(filename):
				continue
			d = ds.read(filename, VARIABLES)
			print('<- %s' % filename)
			dd = stats.stream([d], state, **options)
	else:
		d = ds.read(input_, VARIABLES)
		print('<- %s' % input_)
		dd = stats.stream([d], state, **options)
	dd = stats.stream([None], state, **options)
	if dd[0] == {}:
		raise RuntimeError('No input files')
	else:
		print('-> %s' % output)
		ds.attrs(dd[0], None, alcf.META)
		ds.write(output, dd[0])
