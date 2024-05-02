import ds_format as ds
import os
import numpy as np
from alcf.models import META
from alcf import misc

VARS_INDEX = ['time0', 'latitude', 'longitude']

VARS = [
	'hybridt32',
	'latitude',
	'longitude',
	'model_press',
	'model_qcf',
	'model_qcl',
	'theta_lev_temp',
	'time0',
]

STEP = 2/24

def read(dirname, index, track, t1, t2,
	warnings=[], step=STEP, recursive=False):

	print('<- %s' % dirname)
	dd_index = ds.readdir(dirname, VARS_INDEX,
		jd=True, recursive=recursive)
	dd = []
	for d_index in dd_index:
		misc.require_vars(d_index, VARS_INDEX)
		time = d_index['time0']
		lon = d_index['longitude']
		lon = np.where(lon < 0., 360. + lon, lon)
		lat = d_index['latitude']
		filename = d_index['filename']
		ii = np.where((time >= t1 - step*0.5) & (time <= t2 + step*0.5))[0]
		print('<- %s' % filename)
		for i in ii:
			lon0, lat0 = track(time[i])
			if np.isnan(lon0) or np.isnan(lat0):
				continue
			l = np.argmin((lon - lon0)**2 + (lat - lat0)**2)
			j, k = np.unravel_index(l, lon.shape)
			d = ds.read(filename, VARS, sel={'time0': i, 'rlat': j, 'rlon': k})
			misc.require_vars(d, VARS)
			clw = d['model_qcl']
			cli = d['model_qcf']
			cl = 100.*np.ones(len(clw), dtype=np.float64)
			ps = 2*d['model_press'][0] - d['model_press'][1]
			orog = max(0., 2*d['hybridt32'][0] - d['hybridt32'][1])
			pfull = d['model_press']
			zfull = d['hybridt32']
			ta = d['theta_lev_temp']
			newshape4 = (1, len(clw))
			newshape3 = (1,)
			d_new = {
				'clw': clw.reshape(newshape4),
				'cli': cli.reshape(newshape4),
				'ta': ta.reshape(newshape4),
				'cl': cl.reshape(newshape4),
				'pfull': pfull.reshape(newshape4),
				'zfull': zfull.reshape(newshape4),
				'ps': [ps],
				'orog': [orog],
				'lon': np.array([lon[j,k]]),
				'lat': np.array([lat[j,k]]),
				'time': np.array([time[i]]),
				'.': META,
			}
			dd.append(d_new)
	d = ds.op.merge(dd, 'time')
	return d
