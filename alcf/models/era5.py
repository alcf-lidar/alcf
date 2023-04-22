import sys
import ds_format as ds
import os
import numpy as np
from alcf.models import META
from alcf import misc
import aquarius_time as aq

VARS_PLEV = [
	'time',
	'clwc',
	'ciwc',
	'cc',
	'latitude',
	'longitude',
	'level',
	't',
	'z',
]

VARS_SURF = [
	'time',
	'sp',
	'z',
	'latitude',
	'longitude',
]

TRANS_PLEV = {
	'latitude': 'lat',
	'longitude': 'lon',
	'z': 'zfull',
	'cc': 'cl',
	'level': 'pfull',
	'clwc': 'clw',
	'ciwc': 'cli',
	't': 'ta',
}

TRANS_SURF = {
	'latitude': 'lat',
	'longitude': 'lon',
	'z': 'orog',
	'sp': 'ps',
}

def read0(type_, dirname, track, warnings=[], step=1./24., recursive=False):
	dd_idx = ds.readdir(dirname,
		variables=['time', 'latitude', 'longitude'],
		jd=True,
		full=True,
		warnings=warnings,
		recursive=recursive,
	)
	start_time = track['time'][0]
	end_time = track['time'][-1]

	vars = {
		'surf': VARS_SURF,
		'plev': VARS_PLEV,
	}[type_]

	trans = {
		'surf': TRANS_SURF,
		'plev': TRANS_PLEV,
	}[type_]

	dd = []
	for d_idx in dd_idx:
		time = d_idx['time']
		lat = d_idx['latitude']
		lon = d_idx['longitude']
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
			d = ds.read(filename, vars,
				sel={'time': [i], 'latitude': j, 'longitude': k},
				jd=True,
			)
			for a, b in trans.items():
				if a in d.keys():
					ds.rename(d, a, b)
			d['lat'] = np.array([d['lat']])
			d['lon'] = np.array([d['lon']])
			d['.']['lat']['.dims'] = ['time']
			d['.']['lon']['.dims'] = ['time']
			if type_ == 'plev':
				d['pfull'] = d['pfull'].reshape([1, len(d['pfull'])])
				d['.']['pfull']['.dims'] = ['time', 'level']
				d['cl'] = d['cl'][:,::-1]
				d['clw'] = d['clw'][:,::-1]
				d['cli'] = d['cli'][:,::-1]
				d['ta'] = d['ta'][:,::-1]
				d['zfull'] = d['zfull'][:,::-1]
				d['pfull'] = d['pfull'][:,::-1]
			dd.append(d)
	d = ds.op.merge(dd, 'time')
	if 'time' in d:
		d['time_bnds'] = misc.time_bnds(d['time'], step, start_time, end_time)
	if 'pfull' in d:
		d['pfull'] = 1e2*d['pfull']
	if 'zfull' in d:
		d['zfull'] /= 9.80665
	if 'orog' in d:
		d['orog'] /= 9.80665
	if 'cl' in d:
		d['cl'] *= 100.
	d['.'] = META
	return d

def read(dirname, index, track, warnings=[], recursive=False):
	d_surf = read0('surf', os.path.join(dirname, 'surf'), track, warnings,
		recursive=recursive)
	d_plev = read0('plev', os.path.join(dirname, 'plev'), track, warnings,
		recursive=recursive)
	d = {**d_surf, **d_plev}
	d['.'] = META
	return d
