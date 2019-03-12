import os
import ds_format as ds
from lidars import LIDARS
from cloud_detection import CLOUD_DETECTION
from noise_removal import NOISE_REMOVAL
from calibration import CALIBRATION

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

    alcf lidar <type> <lidar> <output> [options] [algorithm_options]

- type: lidar type (see Types below)
- lidar: input lidar data directory or filename
- output: output filename or directory
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

Algorithm options:

- Cloud detection:
	- default:
		- cloud_threshold: Cloud detection threshold. Default: ?.

- Calibration:
	- default:
		- calibration_coeff: Calibration coefficient. Default: ?.
	"""
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

	if os.path.isdir(input_):
		files = os.listdir(input_)
		dd = []
		for file in sorted(files):
			print(file)
			input_filename = os.path.join(input_, file)
			output_filename = os.path.join(output, file)
			dd.append(lidar.read(input_filename, ['time']))
		d = ds.merge(dd, 'time')
		t1, t2 = d['time'][0], d['time'][-1]
		print(t1, t2)

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
