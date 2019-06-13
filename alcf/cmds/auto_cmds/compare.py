import os
from alcf.cmds import lidar, stats, plot

def run(*args, **options):
	input_ = args[:-1]
	output = args[-1]
	stats_dirs = [
		os.path.join(dir, 'stats')
		for dir in input_
	]
	stats_filenames = [
		os.path.join(stats_dir, 'all.nc')
		for stats_dir in stats_dirs
	]
	options['labels'] = options.get('labels',
		[os.path.dirname(dir) for dir in input_]
	)
	options['title'] = options.get('title',
		os.path.basename(output)
	)
	plot_dir = os.path.join(output, 'plot')
	cloud_occurrence_filename = os.path.join(plot_dir, 'cloud_occurrence.png')

	print('-> %s' % output)
	try: os.mkdir(output)
	except OSError: pass
	print('-> %s' % plot_dir)
	try: os.mkdir(plot_dir)
	except OSError: pass
	print('! alcf plot cloud_occurrence')
	print(options)
	plot.run('cloud_occurrence', *stats_filenames, cloud_occurrence_filename,
		**options
	)
