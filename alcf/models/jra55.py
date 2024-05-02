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

VARS_INDEX = ['time', 'latitude', 'longitude']

VARS_AUX1 = [
	'time',
	'latitude',
	'longitude',
]

VARS_AUX2 = [
	'level',
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

STEP = 6/24

def read(dirname, index, track, t1, t2,
	warnings=[], step=STEP, recursive=False):

	req_vars = ['latitude', 'longitude', 'z']
	ll_filename = os.path.join(dirname, 'LL125.nc')
	print('<- %s' % ll_filename)
	d_ll = ds.read(ll_filename, req_vars)
	misc.require_vars(d_ll, req_vars)
	lat_ll = d_ll['latitude']
	lon_ll = d_ll['longitude']
	orog_ll = d_ll['z'][0,:,:]/9.80665

	print('<- %s' % dirname)
	dd_idx = ds.readdir(dirname, VARS_INDEX,
		jd=True,
		full=True,
		warnings=warnings,
		recursive=recursive,
	)
	do = {}
	for var in VARS:
		dd = []
		var2 = TRANS[var]
		for d_idx in dd_idx:
			misc.require_vars(d_idx, VARS_INDEX)
			if var not in d_idx['.']:
				continue
			time = d_idx['time']
			lat = d_idx['latitude']
			lon = d_idx['longitude']
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
				j_ll = np.argmin(np.abs(lat_ll - lat0))
				k_ll = np.argmin(np.abs(lon_ll - lon0))
				req_vars = VARS_AUX1 + [var]
				vars_ = req_vars + VARS_AUX2
				d = ds.read(filename, vars_,
					sel={
						'time': [i],
						'latitude': j,
						'longitude': k,
					},
					jd=True,
				)
				misc.require_vars(d, req_vars)
				for a, b in TRANS.items():
					if a in d.keys():
						ds.rename(d, a, b)
				d['lat'] = np.array([d['lat']])
				d['lon'] = np.array([d['lon']])
				d['orog'] = np.array([orog_ll[j_ll,k_ll]])
				d['.']['lat']['.dims'] = ['time']
				d['.']['lon']['.dims'] = ['time']
				d['.']['orog'] = {'.dims': ['time']}
				if 'pfull' in ds.vars(d):
					d['pfull'] = d['pfull'].reshape([1, len(d['pfull'])])
					d['.']['pfull']['.dims'] = ['time', 'pfull']
					d['pfull'] = d['pfull'][:,::-1]
					d[var2] = d[var2][:,::-1]
					ds.select(d, {'pfull': np.arange(27)})
				dd.append(d)
		d = ds.op.merge(dd, 'time')
		for var_aux in (VARS_AUX1 + VARS_AUX2):
			if TRANS[var_aux] in ds.vars(do) \
				and TRANS[var_aux] in ds.vars(d) \
				and not np.all(do[TRANS[var_aux]] == d[TRANS[var_aux]]):
				raise ValueError('%s: Field differs between input files' % TRANS[var_aux])
		do.update(d)
	if 'pfull' in do:
		do['pfull'] = do['pfull']*1e2
	return do
