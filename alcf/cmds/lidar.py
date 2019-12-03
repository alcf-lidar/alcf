import os
import logging
import traceback
import numpy as np
import ds_format as ds
import aquarius_time as aq
from alcf.lidars import LIDARS
from alcf.algorithms.calibration import CALIBRATION
from alcf.algorithms.noise_removal import NOISE_REMOVAL
from alcf.algorithms.cloud_detection import CLOUD_DETECTION
from alcf.algorithms.cloud_base_detection import CLOUD_BASE_DETECTION
from alcf.algorithms import tsample, zsample, output_sample, lidar_ratio
from alcf import misc
import pst

VARIABLES = [
	'backscatter',
	'backscatter_mol',
	'time',
	'time_bnds',
	'zfull',
	'altitude',
	# 'range',
]

def read_calibration_file(filename):
	with open(filename, 'rb') as f:
		return pst.decode(f.read())

def run(type_, input_, output,
	altitude=None,
	tres=300,
	tlim=None,
	tshift=0.,
	zres=50,
	zlim=[0., 15000.],
	cloud_detection='default',
	cloud_base_detection='default',
	noise_removal='default',
	calibration='default',
	output_sampling=86400,
	eta=0.7,
	calibration_file=None,
	**options
):
	"""
alcf lidar - process lidar data

The processing is done in the following order:

- noise removal
- calibration
- time resampling
- height resampling
- cloud detection
- cloud base detection

Usage: `alcf lidar <type> <lidar> <output> [<options>] [<algorithm_options>]`

Arguments:

- `type`: lidar type (see Types below)
- `lidar`: input lidar data directory or filename
- `output`: output filename or directory
- `options`: see Options below
- `algorithm_options`: see Algorithm options below

Types:

- `chm15k`: Lufft CHM 15k
- `cl31`: Vaisala CL31
- `cl51`: Vaisala CL51
- `cosp`: COSP simulated lidar
- `minimpl`: Sigma Space MiniMPL
- `mpl`: Sigma Space MPL

Options:

- `altitude`: Altitude of the instrument (m).
    Default: Taken from lidar data or `0` if not available.
- `calibration: <algorithm>`: Backscatter calibration algorithm.
    Available algorithms: `default`, `none`. Default: `default`.
- `cloud_detection: <algorithm>`: Cloud detection algorithm.
    Available algorithms: `default`, `none`. Default: `default`.
- `cloud_base_detection: <algorithm>`: Cloud base detection algorithm.
    Available algorithms: `default`, `none`. Default: `default`.
- `eta: <eta>`: Multiple-scattering factor to assume in lidar ratio calculation.
    Default: `0.7`.
- `noise_removal: <algorithm>`: Noise removal algorithm.
    Available algorithms: `default`, `none`.  Default: `default`.
- `output_sampling: <period>`: Output sampling period (seconds).
    Default: `86400` (24 hours).
- `tlim: { <low> <high> }`: Time limits (see Time format below).
    Default: `none`.
- `tres: <tres>`: Time resolution (seconds). Default: `300` (5 min).
- `tshift: <tshift>`: Time shift (seconds). Default: `0`.
- `zlim: { <low> <high> }`: Height limits (m). Default: `{ 0 15000 }`.
- `zres: <zres>`: Height resolution (m). Default: `50`.

Algorithm options:

- Cloud detection:
    - `default`: cloud detection based on backscatter threshold
        - `cloud_nsd: <n>`: Number of noise standard deviations to subtract.
        	Default: `3`.
        - `cloud_threshold: <threshold>`: Cloud detection threshold
            (sr^-1.m^-1). Default: `2e-6`.
	- `none`: disable cloud detection

- Cloud base detection:
	- `default`: cloud base detection based cloud mask produced by the cloud
		detection algorithm
	- `none`: disable cloud base detection

- Calibration:
    - `default`: multiply backscatter by a calibration coefficient
        - `calibration_file: <file>`: calibration file
	- `none`: disable calibration

- Noise removal:
    - `default`:
        - `noise_removal_sampling: <period>`: Sampling period for noise removal
            (seconds). Default: 300.
    - `none`: disable noise removal
	"""
	# if time is not None:
	# 	start, end = misc.parse_time(time)

	lidar = LIDARS.get(type_)
	if lidar is None:
		raise ValueError('Invalid type: %s' % type_)

	noise_removal_mod = None
	calibration_mod = None
	cloud_detection_mod = None
	cloud_base_detection_mod = None

	if type_ != 'cosp' and noise_removal is not None:
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
		t1 = d['time'][0]
		if len(d['time'] > 1):
			t1 -= 0.5*(d['time'][1] - d['time'][0])
		t1 = np.round(t1*86400.)/86400.
		filename = os.path.join(output, '%s.nc' % aq.to_iso(t1))
		ds.to_netcdf(filename, d)
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
		return d

	def process(dd, state, **options):
		state['preprocess'] = state.get('preprocess', {})
		state['noise_removal'] = state.get('noise_removal', {})
		state['calibration'] = state.get('calibration', {})
		state['tsample'] = state.get('tsample', {})
		state['zsample'] = state.get('zsample', {})
		state['output_sample'] = state.get('output_sample', {})
		state['cloud_detection'] = state.get('cloud_detection', {})
		state['cloud_base_detection'] = state.get('cloud_base_detection', {})
		state['lidar_ratio'] = state.get('lidar_ratio', {})
		state['output'] = state.get('output', {})
		dd = misc.stream(dd, state['preprocess'], preprocess, tshift=tshift)
		if noise_removal_mod is not None:
			dd = noise_removal_mod.stream(dd, state['noise_removal'], **options)
		if calibration_mod is not None:
			dd = calibration_mod.stream(dd, state['calibration'], **options)
		if zres is not None or zlim is not None:
			dd = zsample.stream(dd, state['zsample'], zres=zres, zlim=zlim)
		if tres is not None or tlim is not None:
			dd = tsample.stream(dd, state['tsample'],
				tres=tres/86400.,
				tlim=tlim
			)
		if output_sampling is not None:
			dd = output_sample.stream(dd, state['output_sample'],
				tres=tres/86400.,
				output_sampling=output_sampling/86400.,
			)
		if cloud_detection_mod is not None:
			dd = cloud_detection_mod.stream(dd, state['cloud_detection'], **options)
		if cloud_base_detection_mod is not None:
			dd = cloud_base_detection_mod.stream(dd, state['cloud_base_detection'], **options)
		dd = lidar_ratio.stream(dd, state['lidar_ratio'], eta=eta)
		dd = output_stream(dd, state['output']) #, output_sampling=output_sampling)
		return dd

	options['output'] = output
	options['calibration_coeff'] = calibration_coeff

	state = {}
	if os.path.isdir(input_):
		files = os.listdir(input_)
		for file in sorted(files):
			input_filename = os.path.join(input_, file)
			print('<- %s' % input_filename)
			try:
				d = lidar.read(input_filename, VARIABLES, altitude=altitude)
				dd = process([d], state, **options)
			except:
				logging.warning(traceback.format_exc())
		dd = process([None], state, **options)
	else:
		print('<- %s' % input_)
		d = lidar.read(input_, VARIABLES)
		dd = process([d, None], state, **options)
