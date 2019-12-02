import sys
import ds_format as ds
import os
import numpy as np
from alcf.models import META
from alcf import misc
import aquarius_time as aq

VARIABLES = [
	'air_pressure',
	'air_temperature',
	'mass_fraction_of_cloud_liquid_water_in_air',
	'mass_fraction_of_cloud_ice_in_air',
	'cloud_volume_fraction_in_atmosphere_layer',
]

TRANS = {
	'air_pressure': 'pfull',
	'air_temperature': 'ta',
	'mass_fraction_of_cloud_liquid_water_in_air': 'clw',
	'mass_fraction_of_cloud_ice_in_air': 'cli',
	'cloud_volume_fraction_in_atmosphere_layer': 'cl',
}

def read(dirname, track, warnings=[], step=6./24.):
	dd_index = ds.readdir(dirname,
		variables=['time', 'latitude', 'longitude', 'level_height'],
		jd=True,
		full=True,
		warnings=warnings,
	)
	start_time = track['time'][0]
	end_time = track['time'][-1]
	d_var = {}
	for var in VARIABLES:
		dd = []
		for d_index in dd_index:
			if var not in d_index['.']:
				continue
			time = d_index['time']
			time_half = misc.half(time)
			lat = d_index['latitude']
			lon = d_index['longitude']
			level_height = d_index['level_height']
			filename = d_index['filename']
			ii = np.nonzero((time_half[1:] >= start_time) & (time_half[:-1] < end_time))[0]
			for i in ii:
				t = time[i]
				i2 = np.argmin(np.abs(track['time'] - time[i]))
				lat0 = track['lat'][i2]
				lon0 = track['lon'][i2]
				j = np.argmin(np.abs(lat - lat0))
				k = np.argmin(np.abs(lon - lon0))
				d = ds.read(filename, variables=[var],
					sel={'time': i, 'latitude': j, 'longitude': k})
				d_new = {
					'lat': np.array([lat[j]]),
					'lon': np.array([lon[k]]),
					'time': np.array([t]),
					'level_height': np.array([level_height]),
					'.': META,
				}
				d_new['.']['level_height'] = {
					'.dims': ['level']
				}
				d_new[TRANS[var]] = d[var].reshape([1] + list(d[var].shape))
				if TRANS[var] == 'cl':
					d_new[TRANS[var]] *= 100.
				dd.append(d_new)
		if len(dd) > 0:
			d_var[TRANS[var]] = ds.op.merge(dd, 'time')
	time_list = [
		set(d_var[var]['time'])
		for var in d_var.keys()
	]
	time = time_list[0].intersection(*time_list[1:]) \
		if len(time_list) > 0 \
		else set()
	d = {}
	d['.'] = {}
	if len(time) == 0:
		return None
	for var in d_var.keys():
		idx = [i for i, t in enumerate(d_var[var]['time']) if t in time]
		ds.select(d_var[var], {'time': idx})
		d[var] = d_var[var][var]
		d['lat'] = d_var[var]['lat']
		d['lon'] = d_var[var]['lon']
		d['time'] = d_var[var]['time']
		d['level_height'] = d_var[var]['level_height']
	if 'ps' not in d:
		n, m = d['pfull'].shape
		d['ps'] = np.full(n, np.nan, dtype=np.float64)
		for i in range(n):
	 		d['ps'][i] = 2*d['pfull'][i,0] - d['pfull'][i,1]
	if 'zfull' not in d:
		n, m = d['pfull'].shape
		d['zfull'] = np.full((n, m), np.nan, dtype=np.float64)
		for i in range(n):
			d['zfull'][i,:] = d['level_height']
	del d['level_height']
	if 'orog' not in d:
		n, m = d['zfull'].shape
		d['orog'] = np.full(n, np.nan, dtype=np.float64)
		for i in range(n):
			d['orog'][i] = 2*d['zfull'][i,0] - d['zfull'][i,1]
	if 'time' in d:
		d['time_bnds'] = misc.time_bnds(d['time'], step)
	d['.'] = META
	return d
