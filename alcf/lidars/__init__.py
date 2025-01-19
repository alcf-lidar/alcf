import alcf

META = {
	'time': {
		'.dims': ['time'],
		'long_name': 'time',
		'standard_name': 'time',
		'units': 'days since -4713-11-24 12:00 UTC',
		'calendar': 'proleptic_gregorian',
	},
	'time_bnds': {
		'.dims': ['time', 'bnds'],
		'long_name': 'time bounds',
		'standard_name': 'time',
		'units': 'days since -4713-11-24 12:00 UTC',
		'calendar': 'proleptic_gregorian',
	},
	'zfull': {
		'.dims': ['time', 'level'],
		'long_name': 'altitude of full-levels',
		'standard_name': 'altitude',
		'units': 'm',
	},
	'backscatter': {
		'.dims': ['time', 'level'],
		'long_name': 'total attenuated volume backscattering coefficient',
		'units': 'm-1 sr-1',
	},
	'altitude': {
		'.dims': ['time'],
		'long_name': 'instrument altitude',
		'standard_name': 'altitude',
		'units': 'm',
	},
	'lon': {
		'.dims': ['time'],
		'long_name': 'instrument longitude',
		'standard_name': 'longitude',
		'units': 'degrees_east',
	},
	'lat': {
		'.dims': ['time'],
		'long_name': 'instrument latitude',
		'standard_name': 'latitude',
		'units': 'degrees_north',
	},
	'.': alcf.META,
}

from . import \
	blview, \
	caliop, \
	chm15k, \
	vaisala, \
	cl61, \
	cloudnet, \
	default, \
	mpl, \
	mpl2nc

LIDARS = {
	'blview': blview,
	'caliop': caliop,
	'chm15k': chm15k,
	'cl31': vaisala,
	'cl51': vaisala,
	'cl61': cl61,
	'cn_cl31': cloudnet,
	'cn_cl51': cloudnet,
	'cn_ct25k': cloudnet,
	'cn_minimpl': cloudnet,
	'cosp': default,
	'ct25k': vaisala,
	'default': default,
	'minimpl': mpl,
	'mpl2nc': mpl2nc,
	'mpl': mpl,
}
