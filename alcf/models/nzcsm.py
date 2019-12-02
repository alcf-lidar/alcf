import ds_format as ds
import os
import numpy as np
from alcf.models import META
from alcf import misc

VARIABLES = [
	'hybridt32',
	'latitude',
	'longitude',
	'model_press',
	'model_qcf',
	'model_qcl',
	'theta_lev_temp',
	'time0',
]

GRACE_TIME = 1/24.

def read(dirname, track, warnings=[], step=1./24.):
	dd_index = ds.readdir(dirname, variables=['time0', 'latitude', 'longitude'],
		jd=True)
	start_time = track['time'][0]
	end_time = track['time'][1]
	dd = []
	for d_index in dd_index:
		time = d_index['time0']
		lon = d_index['longitude']
		lon = np.where(lon < 0., 360. + lon, lon)
		lat = d_index['latitude']
		filename = d_index['filename']
		ii = np.where((time >= start_time - GRACE_TIME) & (time <= end_time + GRACE_TIME))[0]
		for i in ii:
			i2 = np.argmin(np.abs(track['time'] - time[i]))
			lon0 = track['lon'][i2]
			lat0 = track['lat'][i2]
			l = np.argmin((lon - lon0)**2 + (lat - lat0)**2)
			j, k = np.unravel_index(l, lon.shape)
			# print('<- %s' % filename)
			d = ds.read(filename, variables=VARIABLES, sel={'time0': i, 'rlat': j, 'rlon': k})
			if not set(VARIABLES).issubset(d.keys()):
				continue
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
	if 'time' in d:
		d['time_bnds'] = misc.time_bnds(d['time'], step)
	return d
