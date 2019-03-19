import os
import ds_format as ds
from lidars import LIDARS
from cloud_detection import CLOUD_DETECTION
from noise_removal import NOISE_REMOVAL
from calibration import CALIBRATION
import misc

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
	if time is not None:
		start, end = misc.parse_time(time)

	lidar = LIDARS.get(type_)
	if lidar is None:
		raise ValueError('Invalid type: %s' % type_)

	cloud_detection_mod = CLOUD_DETECTION.get(cloud_detection)
	if cloud_detection is None:
		raise ValueError('Invalid cloud detection algorithm: %s' % cloud_detection)

	noise_removal_mod = NOISE_REMOVAL.get(noise_removal)
	if noise_removal is None:
		raise ValueError('Invalid noise removal algorithm: %s' % noise_removal)

	calibration_mod = CALIBRATION.get(calibration)
	if calibration is None:
		raise ValueError('Invalid calibration algorithm: %s' % calibration)

	calibration_coeff = lidar.calibration_coeff

	options = {
		'noise_removal_sampling': noise_removal_sampling/60./60./24.,
	}

	def stream(dd, state, options):
		dd = noise_removal_mod.stream(dd, state, options)
		dd = calibration_mod.stream(dd, state, options)
		dd = cloud_detection_mod.stream(dd, state, options)
		dd = output(dd, state, options)
		return dd

	def write(dd, output):
		for d in dd:
			filename = os.path.join(output, '%s.nc' % aq.to_iso(d['time'][0]))
			ds.to_netcdf(d, filename)
			print(filename)

	state = {}
	if os.path.isdir(input_):
		files = os.listdir(input_)
		for file in sorted(files):
			input_filename = os.path.join(input_, file)
			d = lidar.read(input_filename, VARIABLES)
			dd = stream([d], status, options)
			write(dd, output)
		dd = stream([None], state, options)
		write(dd, output)
	else:
		d = lidar.read(input_, VARIABLES)
		dd = stream([d], state, options)
		write([dd], output)
		dd = stream([None], state, options)
		write(dd, output)

	# for t in np.arange(np.floor(t1 - 0.5), np.ceil(t2 - 0.5)) + 0.5:
	# 	dd0 = []
	# 	for d in dd:
	# 		mask = (d['time'] >= t1) & (d['time'] <= t2)
	# 		if np.sum(mask) > 0:
	# 			d0 = lidar.read(d['filename'], VARIABLES)
	# 			ds.select(d0, {'time': mask})
	# 			dd0.append(d0)
	# 	d0 = ds.merge(dd0, 'time')
	# 	print(d0['time'].shape, d0['backscatter'].shape, d0['range'].shape, d0['zfull'].shape)
	# 	print(d0['.'])
	# 	output_filename = os.path.join(output, '%s.nc' % aq.to_iso(t))
	# 	ds.to_netcdf(output_filename, d0)

	# if os.path.isdir(input_):
	# 	files = os.listdir(input_)
	# 	dd = []
	# 	for file in sorted(files):
	# 		print(file)
	# 		input_filename = os.path.join(input_, file)
	# 		output_filename = os.path.join(output, file)
	# 		dd.append(lidar.read(input_filename, ['time']))
	# 	d = ds.merge(dd, 'time')
	# 	t1, t2 = d['time'][0], d['time'][-1]
	# 	print(t1, t2)

	# 		calibration_mod.calibration(d, **options)
	# 		noise_removal_mod.noise_removal(d, **options)
	# 		cloud_detection_mod.cloud_detection(d, **options)
	# 		ds.to_netcdf(output, d)
	# else:
	# 	d = lidar.read(input_, VARIABLES)
	# 	calibration_mod.calibration(d, **options)
	# 	noise_removal_mod.noise_removal(d, **options)
	# 	cloud_detection_mod.cloud_detection(d, **options)
	# 	ds.to_netcdf(output, d)
