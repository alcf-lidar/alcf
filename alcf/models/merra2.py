import ds_format as ds
import os
import warnings as warn
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

VARS_INDEX = ['time', 'lat', 'lon']

STEP=3/24

def ignore_warnings():
	'''Ignore warnings produced by wrong valid_range in MERRA-2 data files.'''
	warn.filterwarnings('ignore', message='invalid value encountered in cast')
	warn.filterwarnings('ignore', message='WARNING: valid_range not used since it\ncannot be safely cast to variable data type')

def read(dirname, index, track, t1, t2,
	warnings=[], step=STEP, recursive=False):

	with warn.catch_warnings():
		ignore_warnings()
		print('<- %s' % dirname)
		dd_index = ds.readdir(dirname, VARS_INDEX, jd=True, recursive=recursive)

	dd = []
	for d_index in dd_index:
		misc.require_vars(d_index, VARS_INDEX)
		time = d_index['time']
		lat = d_index['lat']
		lon = d_index['lon']
		lon = np.where(lon < 0., 360. + lon, lon)
		filename = d_index['filename']
		ii = np.nonzero(
			(time >= t1 - step*0.5) &
			(time < t2 + step*0.5)
		)[0]
		print('<- %s' % filename)
		for i in ii:
			t = time[i]
			lon0, lat0 = track(time[i])
			if np.isnan(lon0) or np.isnan(lat0):
				continue
			j = np.argmin(np.abs(lat - lat0))
			k = np.argmin(np.abs(lon - lon0))
			with warn.catch_warnings():
				ignore_warnings()
				d = ds.read(filename, VARS,
					sel={'time': i, 'lat': j, 'lon': k}
				)
				misc.require_vars(d, VARS)
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
