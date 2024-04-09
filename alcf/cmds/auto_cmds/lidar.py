import os
from alcf.cmds import lidar, stats, plot

STEPS = ['lidar', 'stats', 'plot']

def run(type_, input_, output, *args, skip=None, **kwargs):
	lidar_dir = os.path.join(output, 'lidar')
	stats_dir = os.path.join(output, 'stats')
	stats_filename = os.path.join(stats_dir, 'all.nc')
	stats_fine_filename = os.path.join(stats_dir, 'all_fine.nc')
	stats_clear_fine_filename = os.path.join(stats_dir, 'clear_fine.nc')
	plot_dir = os.path.join(output, 'plot')
	backscatter_dir = os.path.join(plot_dir, 'backscatter')
	cloud_occurrence_filename = os.path.join(plot_dir, 'cloud_occurrence.png')
	cbh_filename = os.path.join(plot_dir, 'cbh.png')
	backscatter_hist_filename = os.path.join(plot_dir, 'backscatter_hist.png')
	backscatter_hist_fine_filename = os.path.join(plot_dir, 'backscatter_hist_all_fine.png')
	backscatter_hist_clear_fine_filename = os.path.join(plot_dir, 'backscatter_hist_clear_fine.png')

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
		stats.run(lidar_dir, stats_fine_filename,
			blim=[-1, 1],
			bres=0.005,
			**kwargs
		)
		stats.run(lidar_dir, stats_clear_fine_filename,
			filter='clear',
			blim=[-1, 1],
			bres=0.005,
			**kwargs
		)
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
		print('! alcf plot cbh')
		plot.run('cbh', stats_filename, cbh_filename,
			**kwargs
		)
		print('! alcf plot backscatter_hist')
		plot.run('backscatter_hist', stats_filename, backscatter_hist_filename,
			**kwargs
		)
		plot.run(
			'backscatter_hist',
			stats_fine_filename,
			backscatter_hist_fine_filename,
			vlog=True,
			vlim=[1e-3, 5],
			**kwargs
		)
		plot.run(
			'backscatter_hist',
			stats_clear_fine_filename,
			backscatter_hist_clear_fine_filename,
			vlog=True,
			vlim=[1e-3, 5],
			**kwargs
		)
