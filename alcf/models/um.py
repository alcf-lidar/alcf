import sys
import ds_format as ds
import os
import numpy as np
from alcf.models import META
from alcf import misc
import aquarius_time as aq

VARS = [
	'TALLTS',
	'latitude_t',
	'longitude_t',
	'DALLTH_eta_theta',
	'STASH_m01s00i265',
	'STASH_m01s00i408',
	'STASH_m01s00i409',
	'STASH_m01s00i254',
	'STASH_m01s00i012',
	'STASH_m01s16i004',
]

TRANS = {
	'TALLTS': 'time',
	'latitude_t': 'lat',
	'longitude_t': 'lon',
	'DALLTH_eta_theta': 'eta',
	'STASH_m01s00i265': 'cl',
	'STASH_m01s00i408': 'pfull',
	'STASH_m01s00i409': 'ps',
        'STASH_m01s00i254': 'clw',
        'STASH_m01s00i012': 'cli',
	'STASH_m01s16i004': 'ta',
}

def read(dirname, track, warnings=[], step=1./24.):
	d_orog = ds.read(os.path.join(dirname, 'qrparm.orog.nc'), [
		'latitude',
		'longitude',
		'surface_altitude',
	])

	dd_idx = ds.readdir(dirname,
		variables=['TALLTS', 'latitude_t', 'longitude_t', 'DALLTH_zsea_theta'],
		jd=True,
		full=True,
		warnings=warnings,
	)
	start_time = track['time'][0]
	end_time = track['time'][-1]

	dd = []
	for d_idx in dd_idx:
		if 'TALLTS' not in d_idx:
			continue

		time = d_idx['TALLTS']
		lat = d_idx['latitude_t']
		lon = d_idx['longitude_t']
		filename = d_idx['filename']

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
			d = ds.read(filename, VARS,
				sel={'TALLTS': [i], 'latitude_t': j, 'longitude_t': k},
				jd=True,
			)
			for a, b in TRANS.items():
				if a in d.keys():
					ds.rename(d, a, b)
			d['lat'] = np.array([d['lat']])
			d['lon'] = np.array([d['lon']])
			d['.']['lat']['.dims'] = ['time']
			d['.']['lon']['.dims'] = ['time']
			orog = d_orog['surface_altitude'][j,k]
			d['zfull'] = d['eta']*85000. + orog*(1. - d['eta']/d['eta'][51])**2
			d['zfull'] = d['zfull'].reshape([1, len(d['zfull'])])
			d['.']['zfull'] = {'.dims': ['time', 'level']}
			d['orog'] = np.array([orog], np.float64)
			d['.']['orog'] = {'.dims': ['time']}
			del d['eta']
			dd.append(d)
	d = ds.op.merge(dd, 'time')
	d['cl'] *= 100.
	if 'time' in d:
		d['time_bnds'] = misc.time_bnds(d['time'], step, start_time, end_time)
		d['time'] = np.mean(d['time_bnds'], axis=1)
	d['.'] = META
	return d
