import os
import sys
import numpy as np
import ds_format as ds
import alcf
from alcf.algorithms import stats
from alcf import misc

VARS = [
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

def get_filenames(input_):
	filenames = []
	if os.path.isdir(input_):
		files = sorted(os.listdir(input_))
		for file_ in files:
			filename = os.path.join(input_, file_)
			if not os.path.isfile(filename):
				continue
			filenames += [filename]
	else:
		filenames += [input_]
	return filenames

def create_common_filter(input_):
	time_bnds = []
	times = set()
	for input1 in input_:
		dd = []
		for filename in get_filenames(input1):
			print('<- %s' % filename)
			d = ds.read(filename, ['time_bnds'])
			dd += [d]
		d = ds.merge(dd, 'time')
		time_bnds += [d['time_bnds']]
		times |= set(d['time_bnds'].flatten())
	times = np.array(sorted(times))
	mask = np.ones(len(times), bool)
	for time_bnds1 in time_bnds:
		ii = np.searchsorted(time_bnds1[:,0], times) - 1
		mask1 = ii == -1
		ii[mask1] = 0
		mask &= time_bnds1[:,1][ii] >= times
		mask[mask1] = 0
	md = np.diff(mask.astype(int))
	ii = list(np.where(md == 1)[0])
	jj = list(np.where(md == -1)[0])
	if mask[0]:
		ii = [0] + ii
	if mask[-1]:
		jj += [len(times) - 1]
	n = len(ii)
	time_bnds = np.full((n, 2), np.nan, np.float64)
	time_bnds[:,0] = times[ii]
	time_bnds[:,1] = times[jj]
	return time_bnds

def create_columns(d, vars, n):
	for var in vars:
		x = ds.var(d, var)
		shape = list(x.shape) + [n]
		dims = ds.dims(d, var) + ['column']
		x = np.repeat(x, n).reshape(shape)
		ds.var(d, var, x)
		ds.dims(d, var, dims)

def merge(dd):
	vars = []
	n = 0
	for d in dd:
		for var in ds.vars(d):
			if 'column' in ds.dims(d, var):
				n = ds.dim(d, 'column')
				vars += [var]
	if n > 0:
		for d in dd:
			if 'column' not in ds.dims(d):
				create_columns(d, vars, n)
	return ds.merge(dd, 'input')

def run(*args,
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
	interp='area_linear',
	lat_lim=None,
	label=None,
	lon_lim=None,
	keep_vars=[],
	**kwargs
):
	'''
alcf-stats -- Calculate cloud occurrence statistics.
==========

Synopsis
--------

    alcf stats [<options>] [--] <input>... <output>

Description
-----------

Arguments following `--` are treated as literal strings. Use this delimiter if the input or output file names might otherwise be interpreted as non-strings, e.g. purely numerical file names.

Multiple input files or directories can be supplied for a comparison - only time periods present in all inputs are included [experimental]. The output of alcf stats with multiple inputs is not yet supported by alcf plot.

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
- `interp: <value>`: Vertical interpolation method. `area_block` for area-weighting with block interpolation, `area_linear` for area-weighting with linear interpolation or `linear` for simple linear interpolation. Default: `area_linear`.
- `keep_vars: { <var>... }`: Keep the listed input variables [experimental]. The variable must be numerical and have a time dimension. The input must be stored in daily files, otherwise the results are undefined. Default: `{ }`.
- `lat_lim: { <from> <to> }`: Latitude limits. Default: `none`.
- `label: { <value...> }`: Input labels. Default: `none`.
- `lon_lim: { <from> <to> }`: Longitude limits. Default: `none`.
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
	if len(args) < 2:
		raise TypeError('invalid arguments')
	input_ = args[:-1]
	output = args[-1]

	tlim_jd = misc.parse_time(tlim) if tlim is not None else None

	if lon_lim is not None:
		lon_lim = [x % 360 for x in lon_lim]

	keep_vars_prefixed = ['input_' + var for var in keep_vars]
	vars = VARS + keep_vars_prefixed

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
		'lat_lim': lat_lim,
		'lon_lim': lon_lim,
		'keep_vars': keep_vars_prefixed,
	}

	if filter_exclude is not None:
		dd = read_filters(filter_exclude)
		options['filters_exclude'] = [d['time_bnds'] for d in dd]

	if filter_include is not None:
		dd = read_filters(filter_include)
		options['filters_include'] = [d['time_bnds'] for d in dd]

	if len(input_) > 1:
		common_filter = create_common_filter(input_)
		options['filters_include'] = options.get('filters_include', []) + \
			[common_filter]

	dd = []
	for input1 in input_:
		state = {}
		dd1 = []
		for filename in get_filenames(input1):
			print('<- %s' % filename)
			d = ds.read(filename, vars)
			dd1 = stats.stream([d], state, **options)
		dd1 = stats.stream([None], state, **options)
		if dd1[0] == {}:
			raise RuntimeError('%s: no input files' % input1)
		else:
			dd += [dd1[0]]

	do = dd[0] if len(dd) == 1 else merge(dd)

	if label is not None:
		do['label'] = label
		do['.']['label'] = {
			'.dims': [] if len(dd) == 1 else ['input'],
			'long_name': 'input label',
		}

	print('-> %s' % output)
	ds.attrs(do, None, alcf.META)
	ds.write(output, do)
