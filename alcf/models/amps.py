import ds_format as ds
import os
import numpy as np
import aquarius_time as aq
from alcf.models import META
from alcf import misc

KAPPA = 0.2854 # Poisson constant for dry air.

VARS = [
	'QCLOUD',
	'QICE',
	'PSFC',
	'P_HYD',
	'P',
	'PB',
	'PHB',
	'PH',
	'HGT',
	'XTIME',
	'XLONG',
	'XLAT',
	'T',
	'T00',
]

def read(dirname, track, warnings=[], step=3./24.):
	dd_index = ds.readdir(dirname, variables=['XTIME'], jd=True)
	start_time = track['time'][0]
	end_time = track['time'][-1]
	dd = []
	for d_index in dd_index:
		time = d_index['XTIME'][0]
		time0 = d_index['.']['.']['SIMULATION_START_DATE']
		time0 = aq.from_iso(time0.replace('_', 'T'))
		if time < 2000000.:
			time = time0 + time/(24.*60.)
		filename = d_index['filename']
		if (time >= start_time - step*0.5) & (time < end_time + step*0.5):
			k = np.argmin(np.abs(track['time'] - time))
			lon0 = track['lon'][k]
			lat0 = track['lat'][k]
			d = ds.read(filename, variables=VARS, sel={'Time': 0})
			lon = np.where(d['XLONG'] < 0., 360. + d['XLONG'], d['XLONG'])
			lat = d['XLAT']
			l = np.argmin((lon - lon0)**2 + (lat - lat0)**2)
			i, j = np.unravel_index(l, lon.shape)
			clw = d['QCLOUD'][:,i,j]
			cli = d['QICE'][:,i,j]
			cl = 100.*np.ones(len(clw), dtype=np.float64)
			ps = d['PSFC'][i,j]
			orog = d['HGT'][i,j]
			pfull = d['PB'][:,i,j] + d['P'][:,i,j]
			zfull = (d['PHB'][:,i,j] + d['PH'][:,i,j])/9.81
			zfull = 0.5*(zfull[1:] + zfull[:-1])
			theta = d['T'][:,i,j] + d['T00']
			ta = theta*(pfull/ps)**KAPPA
			newshape3 = [1] + list(clw.shape)
			newshape2 = [1] + list(ps.shape)
			d_new = {
				'clw': clw.reshape(newshape3),
				'cli': cli.reshape(newshape3),
				'ta': ta.reshape(newshape3),
				'cl': cl.reshape(newshape3),
				'pfull': pfull.reshape(newshape3),
				'zfull': zfull.reshape(newshape3),
				'ps': ps.reshape(newshape2),
				'orog': orog.reshape(newshape2),
				'lon': np.array([lon[i,j]]),
				'lat': np.array([lat[i,j]]),
				'time': np.array([time]),
				'.': META,
			}
			dd.append(d_new)
	d = ds.op.merge(dd, 'time')
	if 'time' in d:
		d['time_bnds'] = misc.time_bnds(d['time'], step, start_time, end_time)
		d['time'] = np.mean(d['time_bnds'], axis=1)
	d['.'] = META
	return d
