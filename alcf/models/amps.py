import ds_format as ds
import os
import re
import numpy as np
import aquarius_time as aq
from alcf.models import META
from alcf import misc

KAPPA = 0.2854 # Poisson constant for dry air.

# Variables in NetCDF files produces by the AMPS project (probably discontinued).
VARS_NC = [
	'QCLOUD',
	'QICE',
	'PSFC',
	'P',
	'PB',
	'PHB',
	'PH',
	'HGT',
	'XTIME',
	'XLONG',
	'XLAT',
	'T',
]

# Variables in NetCDF files converted from GRIB with ncl_convert2nc.
VARS_NCL = [
	'g5_lon_1',
	'g5_lat_0',
	'PRES_GDS5_SFC',
	'HGT_GDS5_SFC',
	'HGT_GDS5_ISBL',
	'TMP_GDS5_ISBL',
	'CLWMR_GDS5_ISBL',
	'ICMR_GDS5_ISBL',
]

STEP = 3/24

def index(dirname, warnings=[], recursive=False, njobs=1):
	print('<- %s' % dirname)
	return ds.readdir(dirname, ['XTIME'],
		jd=True,
		recursive=recursive,
		warnings=warnings,
		parallel=(njobs > 1),
		njobs=njobs,
		full=True,
	)

def read_nc(d_index, track, t1, t2, step):
	time = d_index['XTIME'][0]
	time0 = d_index['.']['.']['SIMULATION_START_DATE']
	time0 = aq.from_iso(time0.replace('_', 'T'))
	if time < 2000000.:
		time = time0 + time/(24*60)
	if (time >= t1 - step*0.5) & (time < t2 + step*0.5):
		lon0, lat0 = track(time)
		if np.isnan(lon0) or np.isnan(lat0):
			return
		print('<- %s' % d_index['filename'])
		d = ds.read(d_index['filename'], VARS_NC, sel={'Time': 0})
		misc.require_vars(d, VARS_NC)
		lon = np.where(d['XLONG'] < 0, 360 + d['XLONG'], d['XLONG'])
		lat = d['XLAT']
		l = np.argmin((lon - lon0)**2 + (lat - lat0)**2)
		i, j = np.unravel_index(l, lon.shape)
		clw = d['QCLOUD'][:,i,j]
		cli = d['QICE'][:,i,j]
		cl = np.full(len(clw), 100, dtype=np.float64)
		ps = d['PSFC'][i,j]
		orog = d['HGT'][i,j]
		pfull = d['PB'][:,i,j] + d['P'][:,i,j]
		zfull = (d['PHB'][:,i,j] + d['PH'][:,i,j])/9.81
		zfull = 0.5*(zfull[1:] + zfull[:-1])
		theta = d['T'][:,i,j] + 300
		ta = theta*(pfull/ps)**KAPPA
		newshape3 = [1] + list(clw.shape)
		newshape2 = [1] + list(ps.shape)
		return {
			'clw': clw.reshape(newshape3),
			'cli': cli.reshape(newshape3),
			'ta': ta.reshape(newshape3),
			'cl': cl.reshape(newshape3),
			'pfull': pfull.reshape(newshape3),
			'zfull': zfull.reshape(newshape3),
			'ps': ps.reshape(newshape2),
			'orog': orog.reshape(newshape2),
			'lon': np.array([lon[i,j]]),
			'lat': np.array([lat[i,j]]),
			'time': np.array([time]),
			'.': META,
		}

def read_ncl(d_index, track, t1, t2, step):
	s = d_index['.']['.']['grib_source']
	m = re.match(r'^(\d\d\d\d)(\d\d)(\d\d)(\d\d)_.*_f(\d\d\d)\.grb', s)
	g = m.groups()
	year = int(g[0])
	month = int(g[1])
	day = int(g[2])
	hour = int(g[3])
	forecast = int(g[4])
	time = aq.from_date([1, year, month, day, hour]) + forecast/24

	dim1 = ds.dims(d_index, 'HGT_GDS5_ISBL')[0]
	dim2 = ds.dims(d_index, 'CLWMR_GDS5_ISBL')[0]

	if (time >= t1 - step*0.5) & (time < t2 + step*0.5):
		lon0, lat0 = track(time)
		if np.isnan(lon0) or np.isnan(lat0):
			return
		req_vars = VARS_NCL + [dim1, dim2]
		print('<- %s' % d_index['filename'])
		d = ds.read(d_index['filename'], req_vars)
		misc.require_vars(d, req_vars)
		lon = np.where(d['g5_lon_1'] < 0, 360 + d['g5_lon_1'], d['g5_lon_1'])
		lat = d['g5_lat_0']
		l = np.argmin((lon - lon0)**2 + (lat - lat0)**2)
		i, j = np.unravel_index(l, lon.shape)
		k1 = ds.dim(d, dim1)
		k2 = ds.dim(d, dim2)
		dk = k1 - k2
		clw = d['CLWMR_GDS5_ISBL'][::-1,i,j]
		cli = d['ICMR_GDS5_ISBL'][::-1,i,j]
		cl = np.full(len(clw), 100, dtype=np.float64)
		ps = d['PRES_GDS5_SFC'][i,j]
		orog = d['HGT_GDS5_SFC'][i,j]
		pfull = d[dim2][::-1]*100
		zfull = d['HGT_GDS5_ISBL'][dk:,i,j][::-1]
		ta = d['TMP_GDS5_ISBL'][dk:,i,j][::-1]
		newshape3 = [1] + list(clw.shape)
		newshape2 = [1] + list(ps.shape)
		return {
			'clw': clw.reshape(newshape3),
			'cli': cli.reshape(newshape3),
			'ta': ta.reshape(newshape3),
			'cl': cl.reshape(newshape3),
			'pfull': pfull.reshape(newshape3),
			'zfull': zfull.reshape(newshape3),
			'ps': ps.reshape(newshape2),
			'orog': orog.reshape(newshape2),
			'lon': np.array([lon[i,j]]),
			'lat': np.array([lat[i,j]]),
			'time': np.array([time]),
			'.': META,
		}

def read(dirname, index, track, t1, t2,
	warnings=[], step=STEP, recursive=False):

	dd = []
	for d_index in index:
		if 'XTIME' in d_index:
			d = read_nc(d_index, track, t1, t2, step)
		else:
			d = read_ncl(d_index, track, t1, t2, step)
		if d is not None:
			dd.append(d)
	d = ds.op.merge(dd, 'time')
	return d
