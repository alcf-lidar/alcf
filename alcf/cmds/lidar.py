import os
import logging
import traceback
import glob
import numpy as np
import ds_format as ds
import aquarius_time as aq
from alcf.lidars import LIDARS
from alcf.algorithms.calibration import CALIBRATION
from alcf.algorithms.noise_removal import NOISE_REMOVAL
from alcf.algorithms.cloud_detection import CLOUD_DETECTION
from alcf.algorithms.cloud_base_detection import CLOUD_BASE_DETECTION
from alcf.algorithms import tsample, zsample, output_sample, lidar_ratio
from alcf.algorithms import couple as couple_mod
from alcf import misc
import pst

VARIABLES = [
	'backscatter',
	'backscatter_mol',
	'backscatter_sd',
	'time',
	'time_bnds',
	'zfull',
	'altitude',
	'lon',
	'lat',
]

def read_calibration_file(filename):
	with open(filename, 'rb') as f:
		return pst.decode(f.read())

def run(type_, input_, output,
	altitude=None,
	tres=300,
	time=None,
	tshift=0.,
	zres=50,
	zlim=[0., 15000.],
	cloud_detection='default',
	cloud_base_detection='default',
	noise_removal='default',
	calibration='default',
	output_sampling=86400,
	overlap_file=None,
	calibration_file=None,
	couple=None,
	fix_cl_range=False,
	cl_crit_range=6000,
	lat=None,
	lon=None,
	r=False,
	**options
):
	"""
alcf-lidar -- Process lidar data.
==========

Synopsis
--------

    alcf lidar <type> [<options>] [<algorithm_options>] [--] <lidar> <output>

Description
-----------

The processing is done in the following order:

- noise removal
- calibration
- time resampling
- height resampling
- cloud detection
- cloud base detection

Arguments following `--` are treated as literal strings. Use this delimiter if the input or output file names might otherwise be interpreted as non-strings, e.g. purely numerical file names.

Arguments
---------

- `type`: Lidar type (see Types below).
- `lidar`: Input lidar data directory or filename. If a directory, only `.nc` files in the directory are processed. If the option `-r` is supplied, the directory is processed recursively.
- `output`: Output filename or directory.
- `options`: See Options below.
- `algorithm_options`: See Algorithm options below.

Types
-----

- `blview`: Vaisala BL-VIEW L2 product.
- `chm15k`: Lufft CHM 15k.
- `cl31`: Vaisala CL31.
- `cl51`: Vaisala CL51.
- `cl61`: Vaisala CL61.
- `cosp`: COSP simulated lidar.
- `default`: The same format as the output of `alcf lidar`.
- `minimpl`: Sigma Space MiniMPL.
- `mpl`: Sigma Space MPL (converted via SigmaMPL).
- `mpl2nc`: Sigma Space MPL (converted via mpl2nc).

Options
-------

- `altitude: <altitude>`: Altitude of the instrument (m). Default: Taken from lidar data or `0` if not available.
- `calibration: <algorithm>`: Backscatter calibration algorithm. Available algorithms: `default`, `none`. Default: `default`.
- `couple: <directory>`: Couple to other lidar data. Default: `none`.
- `cl_crit_range: <range>`: Critical range for the `fix_cl_range` option (m). Default: 6000.
- `cloud_detection: <algorithm>`: Cloud detection algorithm. Available algorithms: `default`, `none`. Default: `default`.
- `cloud_base_detection: <algorithm>`: Cloud base detection algorithm. Available algorithms: `default`, `none`. Default: `default`.
- `--fix_cl_range`: Fix CL31/CL51 range correction (if `noise_h2` firmware option if off). The critical range is taken from `cl_crit_range`.
- `lat: <lat>`: Latitude of the instrument (degrees North). Default: Taken from lidar data or `none` if not available.
- `lon: <lon>`: Longitude of the instrument (degrees East). Default: Taken from lidar data or `none` if not available.
- `noise_removal: <algorithm>`: Noise removal algorithm. Available algorithms: `default`, `none`.  Default: `default`.
- `output_sampling: <period>`: Output sampling period (seconds). Default: `86400` (24 hours).
- `-r`: Process the input directory recursively.
- `time: { <low> <high> }`: Time limits (see Time format below). Default: `none`.
- `tres: <tres>`: Time resolution (seconds). Default: `300` (5 min).
- `tshift: <tshift>`: Time shift (seconds). Default: `0`.
- `zlim: { <low> <high> }`: Height limits (m). Default: `{ 0 15000 }`.
- `zres: <zres>`: Height resolution (m). Default: `50`.

Cloud detection options
-----------------------

- `default`: Cloud detection based on backscatter threshold.
- `none`: Disable cloud detection.

Cloud detection default options
-------------------------------

- `cloud_nsd: <n>`: Number of noise standard deviations to subtract. Default: `5`.
- `cloud_threshold: <threshold>`: Cloud detection threshold (sr^-1.m^-1). Default: `2e-6`.

Cloud base detection options
----------------------------

- `default`: Cloud base detection based cloud mask produced by the cloud detection algorithm.
- `none`: Disable cloud base detection.

Calibration options
-------------------

- `default`: Multiply backscatter by a calibration coefficient.
- `none`: Disable calibration.

Calibration default options
---------------------------

- `calibration_file: <file>`: Calibration file.

Noise removal options
---------------------

- `default`: Noise removal based on noise distribution on the highest level.
- `none`: Disable noise removal.

Noise removal default options
-----------------------------

- `noise_removal_sampling: <period>`: Sampling period for noise removal (seconds). Default: 300.
- `near_noise: { <scale> <range> }` : Assume additional exponentially-decaying near-range noise. The first argument is the value at zero range (sr^-1.m^-1). The second argument is range at which the function decays to a half (m). Default: `{ 0 0 }`.

Time format
-----------

`YYYY-MM-DD[THH:MM[:SS]]`, where `YYYY` is year, `MM` is month, `DD` is day, `HH` is hour, `MM` is minute, `SS` is second. Example: `2000-01-01T00:00:00`.

Examples
--------

Process Vaisala CL51 data in `cl51_nc` and store the output in `cl51_alcf_lidar`, assuming instrument altitude of 100 m above sea level.

    alcf lidar cl51 cl51_nc cl51_alcf_lidar altitude: 100
	"""
	# if time is not None:
	# 	start, end = misc.parse_time(time)

	lidar = LIDARS.get(type_)
	if lidar is None:
		raise ValueError('Invalid type: %s' % type_)

	time1 = None
	if time is not None:
		time1 = [None, None]
		for i in 0, 1:
			time1[i] = aq.from_iso(time[i])
			if time1[i] is None:
				raise ValueError('Invalid time format: %s' % time[i])

	noise_removal_mod = None
	calibration_mod = None
	cloud_detection_mod = None
	cloud_base_detection_mod = None

	if type_ not in ('default', 'cosp') and noise_removal is not None:
		noise_removal_mod = NOISE_REMOVAL.get(noise_removal)
		if noise_removal_mod is None:
			raise ValueError('Invalid noise removal algorithm: %s' % noise_removal)

	if calibration is not None:
		calibration_mod = CALIBRATION.get(calibration)
		if calibration_mod is None:
			raise ValueError('Invalid calibration algorithm: %s' % calibration)

	if cloud_detection is not None:
		cloud_detection_mod = CLOUD_DETECTION.get(cloud_detection)
		if cloud_detection_mod is None:
			raise ValueError('Invalid cloud detection algorithm: %s' % cloud_detection)

	if cloud_base_detection is not None:
		cloud_base_detection_mod = CLOUD_BASE_DETECTION.get(cloud_base_detection)
		if cloud_base_detection_mod is None:
			raise ValueError('Invalid cloud base detection algorithm: %s' % cloud_base_detection)

	if calibration_file is not None:
		c = read_calibration_file(calibration_file)
		calibration_coeff = c[b'calibration_coeff']/lidar.CALIBRATION_COEFF
	else:
		calibration_coeff = 1.

	def write(d, output):
		if len(d['time']) == 0:
			return
		t1 = d['time_bnds'][0,0]
		t1 = np.round(t1*86400.)/86400.
		filename = os.path.join(output, '%s.nc' % aq.to_iso(t1).replace(':', ''))
		ds.write(filename, d)
		print('-> %s' % filename)
		return []

	def output_stream(dd, state, output_sampling=None, **options):
		# if output_sampling is not None:
		# 	state['aggregate_state'] = state.get('aggregate_state', {})
		# 	dd = misc.aggregate(dd, state['aggregate_state'],
		# 		output_sampling/60./60./24.
		# 	)
		return misc.stream(dd, state, write, output=output)

	def preprocess(d, tshift=None):
		if tshift is not None:
			d['time'] += tshift/86400.
			d['time_bnds'] += tshift/86400.
		return d

	def process(dd, state, **options):
		state['preprocess'] = state.get('preprocess', {})
		state['noise_removal'] = state.get('noise_removal', {})
		state['calibration'] = state.get('calibration', {})
		state['tsample'] = state.get('tsample', {})
		state['zsample'] = state.get('zsample', {})
		state['output_sample'] = state.get('output_sample', {})
		state['output_sample_2'] = state.get('output_sample_2', {})
		state['cloud_detection'] = state.get('cloud_detection', {})
		state['cloud_base_detection'] = state.get('cloud_base_detection', {})
		state['lidar_ratio'] = state.get('lidar_ratio', {})
		state['output'] = state.get('output', {})
		state['couple'] = state.get('couple', {})
		dd = misc.stream(dd, state['preprocess'], preprocess, tshift=tshift)
		if couple is not None:
			dd = couple_mod.stream(dd, state['couple'], couple)
		if noise_removal_mod is not None:
			dd = noise_removal_mod.stream(dd, state['noise_removal'], **options)
		if calibration_mod is not None:
			dd = calibration_mod.stream(dd, state['calibration'], **options)
		if zres is not None or zlim is not None:
			dd = zsample.stream(dd, state['zsample'], zres=zres, zlim=zlim)
		if tres is not None or time is not None:
			dd = tsample.stream(dd, state['tsample'], tres=tres/86400.)
		if output_sampling is not None:
			dd = output_sample.stream(dd, state['output_sample'],
				tres=tres/86400.,
				output_sampling=output_sampling/86400.,
			)
			dd = misc.aggregate(dd, state['output_sample_2'], output_sampling/86400.)
		if cloud_detection_mod is not None:
			dd = cloud_detection_mod.stream(dd, state['cloud_detection'], **options)
		if cloud_base_detection_mod is not None:
			dd = cloud_base_detection_mod.stream(dd, state['cloud_base_detection'], **options)
		dd = lidar_ratio.stream(dd, state['lidar_ratio'])
		dd = output_stream(dd, state['output']) #, output_sampling=output_sampling)
		return dd

	options['output'] = output
	options['calibration_coeff'] = calibration_coeff

	state = {}
	if os.path.isdir(input_):
		pattern = '**/*.nc' if r else '*.nc'
		files = sorted(glob.glob(os.path.join(
			glob.escape(input_),
			pattern
		), recursive=r))
		for file_ in files:
			if not os.path.isfile(file_):
				continue
			print('<- %s' % file_)
			try:
				d = lidar.read(file_, VARIABLES,
					altitude=altitude,
					lon=lon,
					lat=lat,
					fix_cl_range=fix_cl_range,
					cl_crit_range=cl_crit_range,
					time=time1,
				)
				if d is None: continue
				dd = process([d], state, **options)
			except SystemExit:
				raise
			except SystemError:
				raise
			except:
				logging.warning(traceback.format_exc())
		dd = process([None], state, **options)
	else:
		print('<- %s' % input_)
		d = lidar.read(input_, VARIABLES,
			altitude=altitude,
			lon=lon,
			lat=lat,
			fix_cl_range=fix_cl_range,
			cl_crit_range=cl_crit_range,
		)
		dd = process([d, None], state, **options)
