import ds_format as ds
import os
import numpy as np
from alcf.models import META
from alcf import misc

VARS = [
	'lon',
	'lat',
	'time',
	'H',
	'T',
	'PL',
	'PS',
	'PHIS',
	'QL',
	'QI',
	'CLOUD',
]

STEP=3/24

def read(dirname, index, track, t1, t2,
	warnings=[], step=STEP, recursive=False):

	dd_index = ds.readdir(dirname, variables=['time', 'lat', 'lon'], jd=True,
		recursive=recursive)
	dd = []
	for d_index in dd_index:
		time = d_index['time']
		lat = d_index['lat']
		lon = d_index['lon']
		lon = np.where(lon < 0., 360. + lon, lon)
		filename = d_index['filename']
		ii = np.nonzero(
			(time >= t1 - step*0.5) &
			(time < t2 + step*0.5)
		)[0]
		for i in ii:
			t = time[i]
			lon0, lat0 = track(time[i])
			if np.isnan(lon0) or np.isnan(lat0):
				continue
			j = np.argmin(np.abs(lat - lat0))
			k = np.argmin(np.abs(lon - lon0))
			d = ds.read(filename, variables=VARS,
				sel={'time': i, 'lat': j, 'lon': k}
			)
			clw = d['QL'][::-1]
			cli = d['QI'][::-1]
			cl = d['CLOUD'][::-1]*100.
			ps = d['PS']
			orog = d['PHIS']/9.80665
			pfull = d['PL'][::-1]
			zfull = d['H'][::-1]
			ta = d['T'][::-1]
			nlev = len(clw)
			newshape4 = (1, nlev)
			newshape3 = (1,)
			d_new = {
				'clw': clw.reshape(newshape4),
				'cli': cli.reshape(newshape4),
				'ta': ta.reshape(newshape4),
				'cl': cl.reshape(newshape4),
				'pfull': pfull.reshape(newshape4),
				'zfull': zfull.reshape(newshape4),
				'ps': ps.reshape(newshape3),
				'orog': orog.reshape(newshape3),
				'lat': np.array([lat[j]]),
				'lon': np.array([lon[k]]),
				'time': np.array([t]),
				'.': META,
			}
			dd.append(d_new)
	d = ds.op.merge(dd, 'time')
	return d
