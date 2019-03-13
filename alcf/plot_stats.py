from matplotlib import pyplot

VARIABLES = [
	'cloud_occurrence',
	'zfull',
]

def run(type_, input_, output):
	"""
alcf plot_stats

Plot lidar statistics.

Usage:

	alcf plot <type> <input> <output>

- type: type of lidar (see Types below)
- input: input filename or directory
- output: output filename or directory
	"""
	
	d = ds.read(input_, VARIABLES)

	plt.savefig(output, bbox_inches='tight')
