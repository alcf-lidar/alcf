from matplotlib import pyplot

def run(type_, input_, output,
	sampling=24,
	width=10,
	height=5,
	dpi=300
):
	"""
alcf plot

Plot lidar data.

Usage:

	alcf plot <type> <input> <output> [time: { <start> <end> }] [options]

- type: type of lidar (see Types below)
- input: input filename or directory
- output: output filename or directory
- start: start time (see Time format below)
- end: end time (see Time format below)
- options: see Options below

Options:

- output_sampling: Output sampling period (seconds). Default: 86400.
- width: Plot width (inches). Default: 10.
- height: Plot height (inches). Default: 5.
- dpi: DPI. Default: 300.
	"""
	plt.figure(figsize=(width, height))

	plt.savefig(output, bbox_inches='tight', dpi=dpi)
