import os
import ds_format as ds
import aquarius_time as aq
from alcf.lidars import LIDARS
from alcf.algorithms.calibration import CALIBRATION
from alcf.algorithms.noise_removal import NOISE_REMOVAL
from alcf.algorithms.cloud_detection import CLOUD_DETECTION
from alcf.algorithms.cloud_base_detection import CLOUD_BASE_DETECTION
from alcf.algorithms import tsampling, zsampling, lidar_ratio
from alcf import misc

VARIABLES = [
	'backscatter',
	'time',
	'zfull',
	# 'range',
]

def run(type_, input_, output,
	tres=300,
	tlim=None,
	zres=50,
	zlim=[0., 15000.],
	cloud_detection='default',
	cloud_base_detection='default',
	noise_removal='default',
	calibration='default',
	output_sampling=86400,
	eta=0.7,
	**options
):
	"""
alcf lidar

Process lidar data. The processing is done in the following order:

- noise removal
- calibration
- time resampling
- height resampling
- cloud detection
- cloud base detection

Usage: `alcf lidar <type> <lidar> <output> [options] [algorithm_options]`

Arguments:

- `type`: lidar type (see Types below)
- `lidar`: input lidar data directory or filename
- `output`: output filename or directory
- `options`: see Options below
- `algorithm_options`: see Algorithm options below

Types:

- `chm15k`: Lufft CHM 15k
- `cl51`: Vaisala CL51
- `mpl`: Sigma Space MiniMPL
- `cosp`: COSP simulated lidar

Options:

- `eta`: Multiple-scattering factor to assume in lidar ratio calculation.
Default: 0.7.
- `cloud_detection`: Cloud detection algorithm. Available algorithms: "default".
	Default: "default".
- `cloud_base_detection`: Cloud base detection algorithm. Available algorithms:
	"default". Default: "default".
- `noise_removal`: Noise removal algorithm. Available algorithms: "default".
	Default: "default".
- `calibration`: Backscatter calibration algorithm. Available algorithms:
	"default". Default: "default".
- `tres`: Time resolution (seconds). Default: 60.
- `tlim`: { <low> <high> }: Time limits (see Time format below). Default: none.
- `zres`: Height resolution (m). Default: 50.
- `zlim`: { <low> <high> }: Height limits (m). Default: { 0 15000 }.
- `output_sampling`: Output sampling period (seconds). Default: 86400.

Algorithm options:

- Cloud detection:
    - `default`: cloud detection based on backscatter threshold
        - `cloud_threshold`: Cloud detection threshold.
            Default: 20e-6 sr^-1.m^-1.
        - `cloud_nsd`: Number of noise standard deviations to subtract.
        	Default: 3.

- Cloud base detection:
	- `default`: cloud base detection based cloud mask produced by the cloud
		detection algorithm

- Calibration:
    - `default`:
        - `calibration_coeff`: Calibration coefficient. Default: ?.

- Noise removal:
    - `default`:
        - `noise_removal_sampling`: Sampling period for noise removal (seconds).
        	Default: 300.
	"""
	# if time is not None:
	# 	start, end = misc.parse_time(time)

	lidar = LIDARS.get(type_)
	if lidar is None:
		raise ValueError('Invalid type: %s' % type_)

	if type_ != 'cosp':
		noise_removal_mod = NOISE_REMOVAL.get(noise_removal)
		if noise_removal_mod is None:
			raise ValueError('Invalid noise removal algorithm: %s' % noise_removal)
	else:
		noise_removal_mod = None

	calibration_mod = CALIBRATION.get(calibration)
	if calibration_mod is None:
		raise ValueError('Invalid calibration algorithm: %s' % calibration)

	cloud_detection_mod = CLOUD_DETECTION.get(cloud_detection)
	if cloud_detection_mod is None:
		raise ValueError('Invalid cloud detection algorithm: %s' % cloud_detection)

	cloud_base_detection_mod = CLOUD_BASE_DETECTION.get(cloud_base_detection)
	if cloud_base_detection_mod is None:
		raise ValueError('Invalid cloud base detection algorithm: %s' % cloud_base_detection)

	calibration_coeff = lidar.CALIBRATION_COEFF

	def write(d, output):
		filename = os.path.join(output, '%s.nc' % aq.to_iso(d['time'][0]))
		ds.to_netcdf(filename, d)
		print('-> %s' % filename)
		return []

	def output_stream(dd, state, output_sampling=None, **options):
		if output_sampling is not None:
			state['aggregate_state'] = state.get('aggregate_state', {})
			dd = misc.aggregate(dd, state['aggregate_state'],
				output_sampling/60./60./24.
			)
		return misc.stream(dd, state, write, output=output)

	def process(dd, state, **options):
		state['noise_removal'] = state.get('noise_removal', {})
		state['calibration'] = state.get('calibration', {})
		state['tsampling'] = state.get('tsampling', {})
		state['zsampling'] = state.get('zsampling', {})
		state['cloud_detection'] = state.get('cloud_detection', {})
		state['cloud_base_detection'] = state.get('cloud_base_detection', {})
		state['lidar_ratio'] = state.get('lidar_ratio', {})
		state['output'] = state.get('output', {})
		if noise_removal_mod is not None:
			dd = noise_removal_mod.stream(dd, state['noise_removal'], **options)
		if calibration_mod is not None:
			dd = calibration_mod.stream(dd, state['calibration'], **options)
		if zres is not None or zlim is not None:
			dd = zsampling.stream(dd, state['zsampling'], zres=zres, zlim=zlim)
		if tres is not None or tlim is not None:
			dd = tsampling.stream(dd, state['tsampling'], tres=tres/24./60./60., tlim=tlim)
		if cloud_detection_mod is not None:
			dd = cloud_detection_mod.stream(dd, state['cloud_detection'], **options)
		if cloud_base_detection_mod is not None:
			dd = cloud_base_detection_mod.stream(dd, state['cloud_base_detection'], **options)
		dd = lidar_ratio.stream(dd, state['lidar_ratio'], eta=eta)
		dd = output_stream(dd, state['output'], output_sampling=output_sampling)
		return dd

	options['output'] = output

	state = {}
	if os.path.isdir(input_):
		files = os.listdir(input_)
		for file in sorted(files):
			input_filename = os.path.join(input_, file)
			print('<- %s' % input_filename)
			d = lidar.read(input_filename, VARIABLES)
			dd = process([d], state, **options)
		dd = process([None], state, **options)
	else:
		d = lidar.read(input_, VARIABLES)
		dd = process([d, None], state, **options)
