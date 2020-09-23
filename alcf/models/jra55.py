import sys
import ds_format as ds
import os
import numpy as np
from alcf.models import META
from alcf import misc
import aquarius_time as aq

VARS = [
	'gh',
	't',
	'ciwc',
	'clw',
	'tcc',
	'sp',
]

VARS_AUX = [
	'level',
	'time',
	'latitude',
	'longitude',
]

TRANS = {
	'gh': 'zfull',
	'latitude': 'lat',
	'longitude': 'lon',
	'level': 'pfull',
	't': 'ta',
	'ciwc': 'cli',
	'clw': 'clw',
	'tcc': 'cl',
	'time': 'time',
	'sp': 'ps',
}

def read(dirname, track, warnings=[], step=6./24.):
	d_ll = ds.read(os.path.join(dirname, 'LL125.nc'), [
		'latitude',
		'longitude',
		'z'
	])
	lat_ll = d_ll['latitude']
	lon_ll = d_ll['longitude']
	orog_ll = d_ll['z'][0,:,:]/9.80665

	dd_idx = ds.readdir(dirname,
		variables=['time', 'latitude', 'longitude'],
		jd=True,
		full=True,
		warnings=warnings,
	)
	start_time = track['time'][0]
	end_time = track['time'][-1]
	d_out = {}
	for var in VARS:
		dd = []
		var2 = TRANS[var]
		for d_idx in dd_idx:
			if var not in d_idx['.']:
				continue
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
				j_ll = np.argmin(np.abs(lat_ll - lat0))
				k_ll = np.argmin(np.abs(lon_ll - lon0))
				d = ds.read(filename, VARS_AUX + [var],
					sel={
						'time': [i],
						'latitude': j,
						'longitude': k,
					},
					jd=True,
				)
				for a, b in TRANS.items():
					if a in d.keys():
						ds.rename(d, a, b)
				d['lat'] = np.array([d['lat']])
				d['lon'] = np.array([d['lon']])
				d['orog'] = np.array([orog_ll[j_ll,k_ll]])
				d['.']['lat']['.dims'] = ['time']
				d['.']['lon']['.dims'] = ['time']
				d['.']['orog'] = {'.dims': ['time']}
				if 'pfull' in ds.get_vars(d):
					d['pfull'] = d['pfull'].reshape([1, len(d['pfull'])])
					d['.']['pfull']['.dims'] = ['time', 'pfull']
					d['pfull'] = d['pfull'][:,::-1]
					d[var2] = d[var2][:,::-1]
					ds.select(d, {'pfull': np.arange(27)})
				dd.append(d)
		d = ds.op.merge(dd, 'time')
		for var_aux in VARS_AUX:
			if TRANS[var_aux] in ds.get_vars(d_out) \
				and TRANS[var_aux] in ds.get_vars(d) \
				and not np.all(d_out[TRANS[var_aux]] == d[TRANS[var_aux]]):
				raise ValueError('%s: Field differs between input files' % TRANS[var_aux])
		d_out.update(d)
	d_out['pfull'] = d_out['pfull']*1e2
	if 'time' in d_out:
		d_out['time_bnds'] = misc.time_bnds(d_out['time'], step, start_time, end_time)
		d_out['time'] = np.mean(d_out['time_bnds'], axis=1)
	d_out['.'] = META
	return d_out
