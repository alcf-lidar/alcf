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
]

def run(input_, output,
	tlim=None,
	blim=[5., 200.],
	bres=5.,
	bsd_lim=[0., 10.],
	bsd_log=True,
	bsd_res=0.001,
	bsd_z=5000.,
	filter=None,
	zlim=[0., 15000.],
	zres=100.,
):
	"""
alcf stats - calculate cloud occurrence statistics

Usage: `alcf stats <input> <output> [<options>]`

Arguments:

- `input`: input filename or directory
- `output`: output filename or directory

Options:

- `blim`: backscatter histogram limits (1e-6 m-1.sr-1). Default: `{ 5 200 }`.
- `bres`: backscatter histogram resolution (1e-6 m-1.sr-1). Default: `10`.
- `filter`: filter profiles by condition: `cloudy` for cloudy profiles only,
    `clear` for clear sky profiles only, `none` for all profiles.
    Default: `none`.
- `tlim`: Time limits `{<start> <end> }` (see Time format below).
    Default: `none`.
- `zlim`: `{ <low> <high> }`: Height limits (m). Default: `{ 0 15000 }`.
- `zres`: Height resolution (m). Default: `50`.
- `bsd_lim`: backscatter standard deviation histogram limits (1e-6 m-1.sr-1).
    Default: `{0 10}`.
- `bsd_log`: enable/disable logarithmic scale of the backscatter standard
    deviation histogram (`true` or `false`). Default: `true`.
- `bsd_res`: backscatter standard deviation histogram resolution
    (1e-6 m-1.sr-1). Default: `0.1`.
- `bsd_z`: backscatter standard deviation histogram height (m). Default: `8000`.

Time format:

"YYYY-MM-DD[THH:MM[:SS]]", where YYYY is year, MM is month, DD is day,
HH is hour, MM is minute, SS is second. Example: 2000-01-01T00:00:00.
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
		'filter': filter,
		'zlim': zlim,
		'zres': zres,
	}

	if os.path.isdir(input_):
		files = os.listdir(input_)
		for file in sorted(files):
			filename = os.path.join(input_, file)
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
	ds.to_netcdf(output, dd[0])
