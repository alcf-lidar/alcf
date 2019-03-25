from matplotlib import pyplot

VARIABLES = [
	'cloud_occurrence',
	'zfull',
]

def run(type_, input_, output,
	width=10,
	height=5,
	dpi=300
):
	"""
alcf plot_stats

Plot lidar statistics.

Usage:

	alcf plot <type> <input> <output> [options]

- type: type of lidar (see Types below)
- input: input filename or directory
- output: output filename or directory
- options: see Options below

Options:

- width: Plot width (inches). Default: 10.
- height: Plot height (inches). Default: 5.
- dpi: DPI. Default: 300.
	"""
	d = ds.read(input_, VARIABLES)
	plt.figure(figsize=(width, height))

	plt.savefig(output, bbox_inches='tight', dpi=dpi)
