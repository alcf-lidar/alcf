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

VARS_FLX = [
	'PRECTOTCORR',
	'FRSEAICE',
]

VARS_SURF = [
	'T2M',
]

VARS_RAD = [
	'LWTUP',
	'SWTDN',
	'SWTNT',
]

STEP=3/24

def ignore_warnings():
	'''Ignore warnings produced by wrong valid_range in MERRA-2 data files.'''
	warn.filterwarnings('ignore', message='invalid value encountered in cast')
	warn.filterwarnings('ignore', message='WARNING: valid_range not used since it\ncannot be safely cast to variable data type')

def read(dirname, index, track, t1, t2,
	warnings=[], step=STEP, recursive=False):

	dirname_3d = os.path.join(dirname, 'M2I3NVASM')
	dirname_flx = os.path.join(dirname, 'M2T1NXFLX')
	dirname_surf = os.path.join(dirname, 'M2I1NXASM')
	dirname_rad = os.path.join(dirname, 'M2T1NXRAD')

	with warn.catch_warnings():
		ignore_warnings()
		print('<- %s' % dirname_3d)
		dd_index = ds.readdir(dirname_3d, VARS_INDEX, jd=True, recursive=recursive)

	dd = []
	for d_index in dd_index:
		misc.require_vars(d_index, VARS_INDEX)
		time = d_index['time']
		lat = d_index['lat']
		lon = d_index['lon']
		lon = np.where(lon < 0., 360. + lon, lon)
		filename = d_index['filename']
		filename_flx = os.path.join(dirname_flx, os.path.basename(filename))
		filename_surf = os.path.join(dirname_surf, os.path.basename(filename))
		filename_rad = os.path.join(dirname_rad, os.path.basename(filename))
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
			with warn.catch_warnings():
				ignore_warnings()
				print('<- %s' % filename_flx)
				d_flx = ds.read(filename_flx, variables=VARS_FLX,
					sel={'time': i, 'lat': j, 'lon': k}
				)
				misc.require_vars(d_flx, VARS_FLX)

				print('<- %s' % filename_surf)
				d_surf = ds.read(filename_surf, variables=VARS_SURF,
					sel={'time': i, 'lat': j, 'lon': k}
				)
				misc.require_vars(d_surf, VARS_SURF)

				print('<- %s' % filename_rad)
				d_rad = ds.read(filename_rad, variables=VARS_RAD,
					sel={'lat': j, 'lon': k}
				)
				misc.require_vars(d_rad, VARS_RAD)
			clw = d['QL'][::-1]
			cli = d['QI'][::-1]
			cl = d['CLOUD'][::-1]*100.
			ps = d['PS']
			pr = d_flx['PRECTOTCORR']
			sic = d_flx['FRSEAICE']
			tas = d_surf['T2M']
			rlut = np.mean(d_rad['LWTUP'], axis=0)
			rsdt = np.mean(d_rad['SWTDN'], axis=0)
			rsut =  np.mean(d_rad['SWTDN'] - d_rad['SWTNT'], axis=0)
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
				'input_pr': pr.reshape(newshape3),
				'input_sic': sic.reshape(newshape3),
				'input_tas': tas.reshape(newshape3),
				'input_rlut': rlut.reshape(newshape3),
				'input_rsdt': rsdt.reshape(newshape3),
				'input_rsut': rsut.reshape(newshape3),
				'orog': orog.reshape(newshape3),
				'lat': np.array([lat[j]]),
				'lon': np.array([lon[k]]),
				'time': np.array([t]),
				'.': META,
			}
			dd.append(d_new)
	d = ds.op.merge(dd, 'time')
	return d
