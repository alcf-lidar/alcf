from matplotlib import pyplot

def run(type_, input_, output,
	sampling=24,
	width=10,
	height=5,
	dpi=300,
):
	"""
alcf plot

Plot lidar data.

Usage:

	alcf plot <type> <input> <output> [options]

- type: type of lidar (see Types below)
- input: input filename or directory
- output: output filename or directory
- options: see Options below

Options:

- sampling: Sampling period (hours). Default: 24.
- width: Plot width (inches). Default: 10.
- height: Plot height (inches). Default: 5.
- dpi: DPI. Default: 300.
	"""
	plt.figure(figsize=(width, height))

	plt.savefig(output, bbox_inches='tight', dpi=dpi)