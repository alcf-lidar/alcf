import sys
import ds_format as ds
import os
import numpy as np
from alcf.models import META
from alcf import misc
import aquarius_time as aq

VARIABLES = [
	'TALLTS',
	'latitude_t',
	'longitude_t',
	'DALLTH_zsea_theta',
	'STASH_m01s00i265',
	'STASH_m01s00i408',
	'STASH_m01s00i409',
	'STASH_m01s04i205',
	'STASH_m01s04i206',
	'STASH_m01s16i004',
]

TRANS = {
	'TALLTS': 'time',
	'latitude_t': 'lat',
	'longitude_t': 'lon',
	'DALLTH_eta_theta': 'level',
	'DALLTH_zsea_theta': 'zfull',
	'STASH_m01s00i265': 'cl',
	'STASH_m01s00i408': 'pfull',
	'STASH_m01s00i409': 'ps',
	'STASH_m01s04i205': 'clw',
	'STASH_m01s04i206': 'cli',
	'STASH_m01s16i004': 'ta',
}

def read(dirname, track, warnings=[]):
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
		time = d_idx['TALLTS']
		lat = d_idx['latitude_t']
		lon = d_idx['longitude_t']
		filename = d_idx['filename']

		ii = np.nonzero((time >= start_time) & (time < end_time))[0]
		for i in ii:
			t = time[i]
			i2 = np.argmin(np.abs(track['time'] - time[i]))
			lat0 = track['lat'][i2]
			lon0 = track['lon'][i2]
			j = np.argmin(np.abs(lat - lat0))
			k = np.argmin(np.abs(lon - lon0))
			d = ds.read(filename, VARIABLES,
				sel={'TALLTS': [i], 'latitude_t': j, 'longitude_t': k},
				jd=True,
			)
			for a, b in TRANS.items():
				if a in d.keys():
					ds.rename(d, a, b)
			ds.rename_dim(d, 'DALLTH_eta_theta', 'level')
			d['lat'] = np.array([d['lat']])
			d['lon'] = np.array([d['lon']])
			d['.']['lat']['.dims'] = ['time']
			d['.']['lon']['.dims'] = ['time']
			d['zfull'] = d['zfull'].reshape([1, len(d['zfull'])])
			d['.']['zfull']['.dims'] = ['time', 'level']
			dd.append(d)
	d = ds.op.merge(dd, 'time')
	d['orog'] = d['zfull'][:,0]
	d['cl'] *= 100.
	d['.'] = META
	return d
