import sys
import ds_format as ds
import os
import numpy as np
from alcf.models import META
from alcf import misc
import aquarius_time as aq

VARS_INDEX = ['time', 'valid_time', 'latitude', 'longitude']

VARS_PLEV = [
	'time',
	'clwc',
	'ciwc',
	'cc',
	'latitude',
	'longitude',
	'level',
	'pressure_level',
	't',
	'z',
]

VARS_SURF = [
	'time',
	'valid_time',
	'sp',
	'z',
	'latitude',
	'longitude',
	'siconc',
	'crr',
	'lsrr',
	't2m',
]

VARS_DAY = [
	'clwc',
	'ciwc',
	'tisr',
	'tsr',
	'ttr',
]

TRANS_PLEV = {
	'latitude': 'lat',
	'longitude': 'lon',
	'z': 'zfull',
	'cc': 'cl',
	'level': 'pfull',
	'pressure_level': 'pfull',
	'clwc': 'clw',
	'ciwc': 'cli',
	't': 'ta',
}

TRANS_SURF = {
	'latitude': 'lat',
	'longitude': 'lon',
	'z': 'orog',
	'sp': 'ps',
	'siconc': 'input_sic',
	't2m': 'input_tas',
	'tisr': 'rsdt',
	'tsr': 'rsnt',
	'ttr': 'rlnt',
}

STEP = 1/24

def read0(type_, dirname, track, t1, t2,
	warnings=[], step=STEP, recursive=False):

	print('<- %s' % dirname)
	dd_idx = ds.readdir(dirname,
		VARS_INDEX,
		jd=True,
		full=True,
		warnings=warnings,
		recursive=recursive,
	)

	req_vars = {
		'surf': VARS_SURF,
		'plev': VARS_PLEV,
	}[type_]

	trans = {
		'surf': TRANS_SURF,
		'plev': TRANS_PLEV,
	}[type_]

	dd = []
	for d_idx in dd_idx:
		ds.rename(d_idx, 'valid_time', 'time')
		#misc.require_vars(d_idx, VARS_INDEX)
		time = d_idx['time']
		lat = d_idx['latitude']
		lon = d_idx['longitude']
		lon = lon % 360
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
			d = ds.read(filename, req_vars,
				sel={'time': [i], 'valid_time': [i], 'latitude': j, 'longitude': k},
				jd=True,
			)
			d_day = ds.read(filename, VARS_DAY,
				sel={'latitude': j, 'longitude': k},
				jd=True,
			)
			ds.rename(d, 'valid_time', 'time')
			#d_alltime = ds.read(filename, req_vars,
			#	sel={'latitude': j, 'longitude': k},
			#	jd=True,
			#)
			#misc.require_vars(d, req_vars)
			for a, b in trans.items():
				if a in d.keys():
					ds.rename(d, a, b)
				if a in d_day.keys():
					ds.rename(d_day, a, b)
			for var in ['rsdt', 'rsnt', 'rlnt', 'clw', 'cli']:
				if var not in d_day: continue
				shape = list(d_day[var].shape)
				shape[0] = 1
				d_day[var] = np.mean(d_day[var], axis=0).reshape(shape)
			d['lat'] = np.array([d['lat']])
			d['lon'] = np.array([d['lon']])
			d['lon'] = d['lon'] % 360
			d['.']['lat']['.dims'] = ['time']
			d['.']['lon']['.dims'] = ['time']
			if type_ == 'surf':
				d['input_rsdt'] = d_day['rsdt']/3600
				d['input_rsut'] = -d_day['rsnt']/3600 + d_day['rsdt']/3600
				d['input_rlut'] = -d_day['rlnt']/3600
			if type_ == 'plev':
				order = np.argsort(d['pfull'])[::-1]
				d['pfull'] = d['pfull'].reshape([1, len(d['pfull'])])
				d['.']['pfull']['.dims'] = ['time', 'level']
				d['cl'] = d['cl'][:,order]
				d['clw'] = d['clw'][:,order]
				d['cli'] = d['cli'][:,order]
				d['ta'] = d['ta'][:,order]
				d['zfull'] = d['zfull'][:,order]
				d['pfull'] = d['pfull'][:,order]
				zhalf = misc.half(d['zfull'][0,:])
				dz = np.diff(zhalf)
				clivi = np.sum(dz*d_day['cli'][0,:])
				clwvi = np.sum(dz*d_day['clw'][0,:])
				d['input_clivi'] = clivi.reshape((1,))
				d['input_clwvi'] = clwvi.reshape((1,))
			for var in ['clivi', 'clwvi', 'rsdt', 'rsut', 'rlut']:
				d['.']['input_'+var] = {'.dims': ['time']}
			dd.append(d)
	d = ds.op.merge(dd, 'time')
	if 'pfull' in d:
		d['pfull'] = 1e2*d['pfull']
	if 'zfull' in d:
		d['zfull'] /= 9.80665
	if 'orog' in d:
		d['orog'] /= 9.80665
	if 'cl' in d:
		d['cl'] = np.minimum(1, np.maximum(0, d['cl']))
		d['cl'] *= 100.
	if 'input_sic' in d:
		d['input_sic'] *= 100
	if 'crr' in d and 'lsrr' in d:
		d['input_pr'] = d['crr'] + d['lsrr']
		del d['crr'], d['lsrr']
	return d

def read(dirname, index, track, t1, t2,
	warnings=[], step=STEP, recursive=False):

	d_surf = read0('surf', os.path.join(dirname, 'surf'), track, t1, t2,
		warnings=warnings, step=step, recursive=recursive)
	d_plev = read0('plev', os.path.join(dirname, 'plev'), track, t1, t2,
		warnings=warnings, step=step, recursive=recursive)
	d = {**d_surf, **d_plev}
	d['.'] = META
	return d
