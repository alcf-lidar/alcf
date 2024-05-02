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

VARS_INDEX = ['TALLTS', 'latitude_t', 'longitude_t', 'DALLTH_zsea_theta']

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

STEP = 1/24

def read(dirname, index, track, t1, t2,
	warnings=[], step=STEP, recursive=False):

	req_vars = ['latitude', 'longitude', 'surface_altitude']
	orog_filename = os.path.join(dirname, 'qrparm.orog.nc')
	print('<- %s' % orog_filename)
	d_orog = ds.read(orog_filename, req_vars)
	misc.require_vars(d_orog, req_vars)

	print('<- %s' % dirname)
	dd_idx = ds.readdir(dirname,
		VARS_INDEX,
		jd=True,
		full=True,
		warnings=warnings,
		recursive=recursive,
	)

	dd = []
	for d_idx in dd_idx:
		if d_idx['filename'] == orog_filename:
			continue
		misc.require_vars(d_idx, VARS_INDEX)

		time = d_idx['TALLTS']
		lat = d_idx['latitude_t']
		lon = d_idx['longitude_t']
		filename = d_idx['filename']

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
			d = ds.read(filename, VARS,
				sel={'TALLTS': [i], 'latitude_t': j, 'longitude_t': k},
				jd=True,
			)
			misc.require_vars(d, VARS)
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
	return d
