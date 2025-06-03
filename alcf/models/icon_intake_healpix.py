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
]

VARS_DAILY = [
	'rlut',
	'rsdt',
	'rsut',
	'cli',
	'clw',
]

STEP = 3/24

def convert_time(time):
	return aq.from_iso('1970-01-01') + \
		(np.array(time).astype('datetime64[s]').astype('int'))/(24*60*60)

def index(dirname, warnings=[], recursive=False, njobs=1):
	import intake
	try: path, model, run, timestep, zoom = dirname
	except Exception as e:
		raise ValueError('Invalid input format: "%s"' % dirname) from e
	cat = intake.open_catalog(path)
	obj = getattr(getattr(cat, model), run)
	ids = obj(time=timestep, zoom=zoom).to_dask()
	ids_daily = obj(time='P1D', zoom=zoom).to_dask()
	time = convert_time(ids.time)
	time_daily = convert_time(ids_daily.time)
	return {
		'ids': ids,
		'ids_daily': ids_daily,
		'time': time,
		'time_daily': time_daily,
	}

def read(dirname, index, track, t1, t2,
	warnings=[], step=STEP, recursive=False):

	import healpy
	ids = index['ids']
	ids_daily = index['ids_daily']
	time = index['time']
	time_daily = index['time_daily']
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
		dt = t - time_daily
		dt[dt < 0] = np.nan
		i_daily = np.nanargmin(dt)
		if dt[i_daily] > 1:
			raise RuntimeError('No daily data found for time %s' % aq.to_iso(t))
		j = healpy.ang2pix(ids.crs.healpix_nside, lon, lat,
			lonlat=True,
			nest=nest
		)
		j_daily = healpy.ang2pix(ids_daily.crs.healpix_nside, lon, lat,
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
			elif var in ['pr', 'sic', 'tas']:
				d['input_'+var] = x
				dims = []
			else:
				d[var] = x[::-1]
				dims = ['level']
			ds.dims(d, var, dims)
		for var in VARS_DAILY:
			x = np.array(ids_daily[var].isel(cell=j_daily, time=i_daily))
			if var in ['rsdt', 'rsut', 'rlut']:
				d['input_'+var] = x
				ds.dims(d, 'input_'+var, [])
			else:
				d['input_'+var] = x[::-1]
				ds.dims(d, 'input_'+var, ['level'])
		zhalf = misc.half(d['zfull'])
		dz = np.diff(zhalf)
		d['input_clivi'] = np.sum(dz*d['input_cli'])
		d['input_clwvi'] = np.sum(dz*d['input_clw'])
		del d['input_cli'], d['input_clw']
		ds.dims(d, 'input_clivi', [])
		ds.dims(d, 'input_clwvi', [])
		dd += [d]
	d = ds.merge(dd, 'time')
	d['cl'] = np.full(d['cli'].shape, 100., np.float64)
	return d
