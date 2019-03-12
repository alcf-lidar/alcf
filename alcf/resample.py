import os
import numpy as np
import ds_format as ds
import aquarius_time as aq
from lidars import LIDARS

VARIABLES = [
	'time',
	'range',
	'zfull',
	'range',
	'backscatter',
]

def run(type_, input_, output):
	lidar = LIDARS.get(type_)
	if lidar is None:
		raise ValueError('Invalid type: %s' % type_)

	if os.path.isdir(input_):
		files = os.listdir(input_)
		dd = []
		for file in sorted(files):
			input_filename = os.path.join(input_, file)
			d = lidar.read(input_filename, ['time'])
			d['filename'] = input_filename
			d['.']['filename'] = {
				'.dims': [],
			}
			dd.append(d)
			print(file)
		d = ds.merge(dd, 'time')
	else:
		d = lidar.read(input_, ['time'])

	t1, t2 = d['time'][0], d['time'][-1]
	for t in np.arange(np.floor(t1 - 0.5), np.ceil(t2 - 0.5)) + 0.5:
		dd0 = []
		for d in dd:
			mask = (d['time'] >= t1) & (d['time'] <= t2)
			if np.sum(mask) > 0:
				d0 = lidar.read(d['filename'], VARIABLES)
				ds.select(d0, {'time': mask})
				dd0.append(d0)
		d0 = ds.merge(dd0, 'time')
		print(d0['time'].shape, d0['backscatter'].shape, d0['range'].shape, d0['zfull'].shape)
		print(d0['.'])
		output_filename = os.path.join(output, '%s.nc' % aq.to_iso(t))
		ds.to_netcdf(output_filename, d0)
