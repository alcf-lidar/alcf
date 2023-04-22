import sys
import ds_format as ds
import os
import numpy as np
from alcf.models import META
from alcf import misc
import aquarius_time as aq

VARS = [
	'cli',
	'clw',
	'pfull',
	'ta',
	'ps',
]

def index(dirname, warnings=[], recursive=False, njobs=1):
	dd = ds.readdir(dirname,
		variables=['time'],
		jd=True,
		full=True,
		warnings=warnings,
		recursive=recursive,
		parallel=(njobs > 1),
		njobs=njobs,
	)

	d_g = ds.read(os.path.join(dirname, 'vgrid.nc'), [
		'clon', 'clat'
	], full=True)
	d_g['clon'] *= 180/np.pi
	d_g['clat'] *= 180/np.pi

	return [dd, d_g]

def read(dirname, index, track, warnings=[], step=6./24., recursive=False):
	start_time = track['time'][0]
	end_time = track['time'][-1]
	vgrid_filename = os.path.join(dirname, 'vgrid.nc')
	dd_out = []
	dd_idx, d_g = index
	ncells = ds.dim(d_g, 'ncells')

	for var in VARS:
		dd = []
		for d_idx in dd_idx:
			if var not in d_idx['.']:
				continue
			time = d_idx['time']
			filename = d_idx['filename']
			ii = np.nonzero(
				(time >= start_time - step*0.5) &
				(time < end_time + step*0.5)
			)[0]
			for i in ii:
				lon0, lat0 = misc.track_at(track, time[i])
				dist = misc.geo_distance(
					np.full(ncells, lon0),
					np.full(ncells, lat0),
					d_g['clon'],
					d_g['clat'],
					method='gc'
				)
				cell = np.argmin(dist)

				d_g2 = ds.read(vgrid_filename, ['zg', 'zghalf'], sel={
					'ncells': cell,
					'height': ds.dim(d_g, 'height') - 1,
				})

				d = ds.read(filename, [var],
					sel={
						'time': [i],
						'ncells': cell,
					},
					jd=True,
				)
				ds.rename_dim(d, 'height', 'level')
				d['time'] = np.array([time[i]])
				d['lat'] = np.array([d_g['clat'][cell]])
				d['lon'] = np.array([d_g['clon'][cell]])
				d['orog'] = np.array([d_g2['zghalf']])
				d['zfull'] = d_g2['zg'][::-1]
				d['zfull'] = d['zfull'].reshape((1, len(d['zfull'])))
				ds.dims(d, 'time', ['time'])
				ds.dims(d, 'lat', ['time'])
				ds.dims(d, 'lon', ['time'])
				ds.dims(d, 'orog', ['time'])
				ds.dims(d, 'zfull', ['time', 'level'])
				if d[var].ndim == 2:
					d[var] = d[var][:,::-1]
				dd.append(d)
		d = ds.op.merge(dd, 'time')
		dd_out += [d]

	time = set.intersection(*[set(d['time']) for d in dd_out])
	d_out = {}
	for d in dd_out:
		ii = [t in time for t in d['time']]
		ds.select(d, {'time': ii})
		d_out.update(d)

	d_out['cl'] = np.full(d_out['cli'].shape, 100., np.float64)
	if 'time' in d_out:
		d_out['time_bnds'] = misc.time_bnds(d_out['time'], step, start_time, end_time)
	d_out['.'] = META

	return d_out
