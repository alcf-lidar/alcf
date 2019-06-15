import os
from alcf.cmds import lidar, stats, plot

STEPS = ['lidar', 'stats', 'plot']

def run(type_, input_, output, *args, skip=None, **kwargs):
	lidar_dir = os.path.join(output, 'lidar')
	stats_dir = os.path.join(output, 'stats')
	stats_filename = os.path.join(stats_dir, 'all.nc')
	plot_dir = os.path.join(output, 'plot')
	backscatter_dir = os.path.join(plot_dir, 'backscatter')
	cloud_occurrence_filename = os.path.join(plot_dir, 'cloud_occurrence.png')
	backscatter_hist_filename = os.path.join(plot_dir, 'backscatter_hist.png')

	if skip is not None:
		try: i = STEPS.index(skip)
		except ValueError:
			raise ValueError('Invalid step "%s"' % skip)
	else:
		i = -1

	print('-> %s' % output)
	try: os.mkdir(output)
	except OSError: pass

	if i < STEPS.index('lidar'):
		print('-> %s' % lidar_dir)
		try: os.mkdir(lidar_dir)
		except OSError: pass
		print('! alcf lidar')
		lidar.run(type_, input_, lidar_dir, *args, **kwargs)
	if i < STEPS.index('stats'):
		print('-> %s' % stats_dir)
		try: os.mkdir(stats_dir)
		except OSError: pass
		print('! alcf stats')
		stats.run(lidar_dir, stats_filename, **kwargs)
	if i < STEPS.index('plot'):
		print('-> %s' % plot_dir)
		try: os.mkdir(plot_dir)
		except OSError: pass
		print('-> %s' % backscatter_dir)
		try: os.mkdir(backscatter_dir)
		except OSError: pass
		print('! alcf plot backscatter')
		plot.run('backscatter', lidar_dir, backscatter_dir, **kwargs)
		print('! alcf plot cloud_occurrence')
		plot.run('cloud_occurrence', stats_filename, cloud_occurrence_filename,
			**kwargs
		)
		print('! alcf plot backscatter_hist')
		plot.run('backscatter_hist', stats_filename, backscatter_hist_filename,
			**kwargs
		)
