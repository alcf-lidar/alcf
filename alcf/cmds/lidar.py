import os
import ds_format as ds
import aquarius_time as aq
from alcf.lidars import LIDARS
from alcf.cloud_detection import CLOUD_DETECTION
from alcf.noise_removal import NOISE_REMOVAL
from alcf.calibration import CALIBRATION
from alcf import misc

VARIABLES = [
	'backscatter',
	'time',
	'zfull',
]

def run(type_, input_, output,
	cloud_detection='default',
	noise_removal='default',
	calibration='default',
	**options
):
	"""
alcf lidar

Process lidar data.

Usage:

    alcf lidar <type> <lidar> <output> [time: { <start> <end> }] [options]
    	[algorithm_options]

Arguments:

- type: lidar type (see Types below)
- lidar: input lidar data directory or filename
- output: output filename or directory
- start: start time (see Time format below)
- end: end time (see Time format below)
- options: see Options below
- algorithm_options: see Algorithm options below

Types:

- chm15k: Lufft CHM 15k
- cl51: Vaisala CL51
- mpl: Sigma Space MiniMPL
- cosp: COSP simulated lidar

Options:

- cloud_detection: Cloud detection algorithm. Available algorithms: "default".
	Default: "default".
- noise_removal: Noise removal algorithm. Available algorithms: "default".
	Default: "default".
- calibration: Backscatter calibration algorithm. Available algorithms:
	"default". Default: "default".
- hres: Horizontal resolution (seconds). Default: 300.
- vres: Vertical resolution (m). Default: 50.
- output_sampling: Output sampling period (seconds). Default: 86400.

Algorithm options:

- Cloud detection:
    - default:
        - cloud_threshold: Cloud detection threshold.
            Default: 20e-6 sr^-1.m^-1.

- Calibration:
    - default:
        - calibration_coeff: Calibration coefficient. Default: ?.

- Noise removal:
    - default:
        - noise_removal_sampling: Sampling period for noise removal (seconds).
        	Default: 300.
	"""
	# if time is not None:
	# 	start, end = misc.parse_time(time)

	lidar = LIDARS.get(type_)
	if lidar is None:
		raise ValueError('Invalid type: %s' % type_)

	noise_removal_mod = NOISE_REMOVAL.get(noise_removal)
	if noise_removal_mod is None:
		raise ValueError('Invalid noise removal algorithm: %s' % noise_removal)

	calibration_mod = CALIBRATION.get(calibration)
	if calibration_mod is None:
		raise ValueError('Invalid calibration algorithm: %s' % calibration)

	cloud_detection_mod = CLOUD_DETECTION.get(cloud_detection)
	if cloud_detection_mod is None:
		raise ValueError('Invalid cloud detection algorithm: %s' % cloud_detection)

	calibration_coeff = lidar.calibration_coeff

	def write(d, output=None, **options):
		filename = os.path.join(output, '%s.nc' % aq.to_iso(d['time'][0]))
		ds.to_netcdf(filename, d)
		print(filename)
		return []

	def output_stream(dd, state, output_sampling=86400, **options):
		state['aggregate_state'] = state.get('aggregate_state', {})
		dd = misc.aggregate(dd, state['aggregate_state'], output_sampling/60./60./24.)
		return misc.stream(dd, state, write, **options)

	def process(dd, state, **options):
		state['noise_removal'] = state.get('noise_removal', {})
		state['calibration'] = state.get('calibration', {})
		state['cloud_detection'] = state.get('cloud_detection', {})
		state['output'] = state.get('output', {})
		dd = noise_removal_mod.stream(dd, state['noise_removal'], **options)
		dd = calibration_mod.stream(dd, state['calibration'], **options)
		dd = cloud_detection_mod.stream(dd, state['cloud_detection'], **options)
		dd = output_stream(dd, state['output'], **options)
		return dd

	options['output'] = output

	state = {}
	if os.path.isdir(input_):
		files = os.listdir(input_)
		for file in sorted(files):
			input_filename = os.path.join(input_, file)
			d = lidar.read(input_filename, VARIABLES)
			dd = process([d], state, **options)
		dd = process([None], state, **options)
	else:
		d = lidar.read(input_, VARIABLES)
		dd = process([d, None], state, **options)
