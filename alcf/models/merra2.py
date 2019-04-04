import ds_format as ds
import os
import numpy as np

VARIABLES = [
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

GRACE_TIME = 1/24.

DESCR = {
	'clw': {
		'.dims': ['time', 'level'],
		'standard_name': 'mass_fraction_of_cloud_liquid_water_in_air',
		'units': '1',
	},
	'cli': {
		'.dims': ['time', 'level'],
		'standard_name': 'mass_fraction_of_cloud_ice_in_air',
		'units': '1',
	},
	'ps': {
		'.dims': ['time'],
		'standard_name': 'surface_air_pressure',
		'units': 'Pa',
	},
	'pfull': {
		'.dims': ['time', 'level'],
		'standard_name': 'air_pressure',
		'units': 'Pa',
	},
	'zg': {
		'.dims': ['time', 'level'],
		'standard_name': 'geopotential_height',
		'units': 'm',
	},
	'time': {
		'.dims': ['time'],
		'standard_name': 'time',
		'units': 'days since -4712-01-01T12:00',
	},
	'lon': {
		'.dims': ['time'],
		'standard_name': 'longitude',
		'units': 'degrees_east',
	},
	'lat': {
		'.dims': ['time'],
		'standard_name': 'latitude',
		'units': 'degrees_north',
	},
	'ta': {
		'.dims': ['time', 'level'],
		'standard_name': 'air_temperature',
		'units': 'K',
	},
	'clt': {
		'.dims': ['time', 'level'],
		'standard_name': 'cloud_area_fraction',
		'units': '%',
	},
	'orog': {
		'.dims': ['time'],
		'standard_name': 'surface_altitude',
		'units': 'm',
	},
}

def read(dirname, track):
	dd_index = ds.readdir(dirname, variables=['time', 'lat', 'lon'], jd=True)
	start_time = track['time'][0]
	end_time = track['time'][1]
	dd = []
	for d_index in dd_index:
		time = d_index['time']
		lat = d_index['lat']
		lon = d_index['lon']
		lon = np.where(lon < 0., 360. + lon, lon)
		filename = d_index['filename']
		ii = np.where((time >= start_time - GRACE_TIME) & (time <= end_time + GRACE_TIME))[0]
		for i in ii:
			t = time[i]
			i2 = np.argmin(np.abs(track['time'] - time[i]))
			lat0 = track['lat'][i2]
			lon0 = track['lon'][i2]
			j = np.argmin(np.abs(lat - lat0))
			k = np.argmin(np.abs(lon - lon0))
			d = ds.read(filename, variables=VARIABLES, sel={'time': i, 'lat': j, 'lon': k})
			clw = d['QL'][::-1]
			cli = d['QI'][::-1]
			clt = d['CLOUD'][::-1]*100.
			ps = d['PS']
			orog = d['PHIS']
			pfull = d['PL'][::-1]
			zg = d['H'][::-1]
			ta = d['T'][::-1]
			nlev = len(clw)
			newshape4 = (1,nlev)
			newshape3 = (1,)
			d_new = {
				'clw': clw.reshape(newshape4),
				'cli': cli.reshape(newshape4),
				'ta': ta.reshape(newshape4),
				'clt': clt.reshape(newshape4),
				'pfull': pfull.reshape(newshape4),
				'zg': zg.reshape(newshape4),
				'ps': ps.reshape(newshape3),
				'orog': orog.reshape(newshape3),
				'lat': np.array([lat[j]]),
				'lon': np.array([lon[k]]),
				'time': np.array([t]),
				'.': DESCR,
			}
			dd.append(d_new)
	d = ds.op.merge(dd, 'time')
	return d
