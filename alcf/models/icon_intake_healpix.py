import sys
import ds_format as ds
import os
import numpy as np
from alcf.models import META
from alcf import misc
import aquarius_time as aq

VARS = [
	'cli',
	'clw',
	'pfull',
	'phalf',
	'ta',
	'zg',
	'zghalf',
	'pr',
	'sic',
	'tas',
	'rlut',
	'rsdt',
	'rsut',
]

STEP = 3/24

def index(dirname, warnings=[], recursive=False, njobs=1):
	import intake
	try: path, model, run, timestep, zoom = dirname
	except Exception as e:
		raise ValueError('Invalid input format: "%s"' % dirname) from e
	cat = intake.open_catalog(path)
	obj = getattr(getattr(cat, model), run)
	ids = obj(time=timestep, zoom=zoom).to_dask()
	ids_daily = obj(time='P1D', zoom=zoom).to_dask()
	time = aq.from_iso('1970-01-01') + \
		(np.array(ids.time).astype('datetime64[s]').astype('int'))/(24*60*60)
	return {
		'ids': ids,
		'ids_daily': ids,
		'time': time,
	}

def read(dirname, index, track, t1, t2,
	warnings=[], step=STEP, recursive=False):

	import healpy
	ids = index['ids']
	ids_daily = index['ids_daily']
	time = index['time']
	nest = ids.crs.healpix_order == 'nest'
	ii = np.nonzero(
		(time >= t1 - step*0.5) &
		(time < t2 + step*0.5)
	)[0]
	dd = []
	for i in ii:
		t = time[i]
		lon, lat = track(t)
		if np.isnan(lon) or np.isnan(lat):
			continue
		j = healpy.ang2pix(ids.crs.healpix_nside, lon, lat,
			lonlat=True,
			nest=nest
		)
		d = {}
		d['time'] = t
		d['lon'], d['lat'] = healpy.pix2ang(ids.crs.healpix_nside, j,
			lonlat=True,
			nest=nest
		)
		for var in VARS:
			sel = {'cell': j}
			if 'time' in ids[var].coords:
				sel['time'] = i
			if var in ['rlut', 'rsdt', 'rsut']:
				x = np.array(ids_daily[var].isel(**sel))
			else:
				x = np.array(ids[var].isel(**sel))
			if var == 'phalf':
				d['ps'] = x[-1]
				dims = []
			elif var == 'zghalf':
				d['orog'] = x[-1]
				dims = []
			elif var == 'zg':
				d['zfull'] = x[::-1]
				dims = ['level']
			elif var in ['pr', 'sic', 'tas', 'rlut', 'rsdt', 'rsut']:
				d['input_'+var] = x
				dims = []
			else:
				d[var] = x[::-1]
				dims = ['level']
			ds.dims(d, var, dims)
		dd += [d]
	d = ds.merge(dd, 'time')
	d['cl'] = np.full(d['cli'].shape, 100., np.float64)
	return d
