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

def read(dirname, track, warnings=[], step=3./24.):
	dd_index = ds.readdir(dirname, variables=['time', 'lat', 'lon'], jd=True)
	start_time = track['time'][0]
	end_time = track['time'][-1]
	dd = []
	for d_index in dd_index:
		time = d_index['time']
		lat = d_index['lat']
		lon = d_index['lon']
		lon = np.where(lon < 0., 360. + lon, lon)
		filename = d_index['filename']
		ii = np.nonzero(
			(time >= start_time - step*0.5) &
			(time < end_time + step*0.5)
		)[0]
		for i in ii:
			t = time[i]
			i2 = np.argmin(np.abs(track['time'] - time[i]))
			lat0 = track['lat'][i2]
			lon0 = track['lon'][i2]
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
	if 'time' in d:
		d['time_bnds'] = misc.time_bnds(d['time'], step, start_time, end_time)
		d['time'] = np.mean(d['time_bnds'], axis=1)
	d['.'] = META
	return d
