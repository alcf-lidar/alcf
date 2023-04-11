import os
from alcf.cmds import model, simulate, lidar, stats, plot
from alcf.cmds.auto_cmds import lidar as auto_lidar

STEPS = ['model', 'simulate'] + auto_lidar.STEPS

def run(model_type, lidar_type, input_, output, *args, skip=None, **kwargs):
	model_dir = os.path.join(output, 'model')
	simulate_dir = os.path.join(output, 'simulate')

	if skip is not None:
		try: i = STEPS.index(skip)
		except ValueError:
			raise ValueError('Invalid step "%s"' % skip)
	else:
		i = -1

	print('-> %s' % output)
	try: os.mkdir(output)
	except OSError: pass

	if i < STEPS.index('model'):
		print('-> %s' % model_dir)
		try: os.mkdir(model_dir)
		except OSError: pass
		print('! alcf model')
		model.run(model_type, input_, model_dir, *args, **kwargs)
	if i < STEPS.index('simulate'):
		print('-> %s' % simulate_dir)
		try: os.mkdir(simulate_dir)
		except OSError: pass
		print('! alcf simulate')
		simulate.run(lidar_type, model_dir, simulate_dir)

	lidar_skip = skip if i > STEPS.index('simulate') else None
	auto_lidar.run('cosp', simulate_dir, output, *args,
		skip=lidar_skip,
		**kwargs
	)
