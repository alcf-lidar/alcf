import os
import sys
import numpy as np
import ds_format as ds
from alcf.algorithms import interp
from alcf.algorithms import stats
from alcf.misc import parse_time

VARIABLES = [
	'cloud_mask',
	'zfull',
	'time',
	'backscatter',
	'backscatter_sd',
	'backscatter_mol',
	'lon',
	'lat',
]

def run(input_, output,
	tlim=None,
	blim=[5., 200.],
	bres=5.,
	bsd_lim=[0.001, 10.],
	bsd_log=True,
	bsd_res=0.001,
	bsd_z=8000.,
	filter=None,
	zlim=[0., 15000.],
	zres=100.,
	**kwargs
):
	"""
alcf stats - calculate cloud occurrence statistics

Usage: `alcf stats <input> <output> [<options>]`

Arguments:

- `input`: input filename or directory
- `output`: output filename or directory

Options:

- `blim: <value>`: backscatter histogram limits (1e-6 m-1.sr-1).
    Default: `{ 5 200 }`.
- `bres: <value>`: backscatter histogram resolution (1e-6 m-1.sr-1).
    Default: `10`.
- `filter: <value> | { <value> ... }`: Filter profiles by condition: `cloudy` for
    cloudy profiles only, `clear` for clear sky profiles only, `night` for
    nighttime profiles, `day` for daytime profiles, `none` for all profiles.
    If an array of values is supplied, all conditions must be true. For `night`
    and `day`, lidar profiles must contain valid longitude and latitude
    fields set via the `lon` and `lat` arguments of `alcf lidar` or read
    implicitly from raw lidar data files if available (mpl, mpl2nc).
    Default: `none`.
- `tlim: { <start> <end> }`: Time limits (see Time format below).
    Default: `none`.
- `zlim: { <low> <high> }`: Height limits (m). Default: `{ 0 15000 }`.
- `zres: <value>`: Height resolution (m). Default: `50`.
- `bsd_lim: { <low> <high> }`: backscatter standard deviation histogram limits
    (1e-6 m-1.sr-1). Default: `{ 0.001 10 }`.
- `bsd_log: <value>`: enable/disable logarithmic scale of the backscatter
    standard deviation histogram (`true` or `false`). Default: `true`.
- `bsd_res: <value>`: backscatter standard deviation histogram resolution
    (1e-6 m-1.sr-1). Default: `0.001`.
- `bsd_z: <value>`: backscatter standard deviation histogram height (m).
    Default: `8000`.

Time format:

"YYYY-MM-DD[THH:MM[:SS]]", where YYYY is year, MM is month, DD is day,
HH is hour, MM is minute, SS is second. Example: 2000-01-01T00:00:00.

Examples:

Calculate statistics from processed lidar data in `alcf_cl51_lidar`
and store the output in `alcf_cl51_stats.nc`.

    alcf stats alcf_cl51_lidar alcf_cl51_stats.nc
	"""
	tlim_jd = parse_time(tlim) if tlim is not None else None
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
	}

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
	print('-> %s' % output)
	ds.write(output, dd[0])
