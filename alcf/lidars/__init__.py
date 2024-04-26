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

from . import chm15k
from . import cl61
from . import blview
from . import cl51
from . import cl31
from . import mpl
from . import mpl2nc
from . import default
from . import caliop

LIDARS = {
	'default': default,
	'chm15k': chm15k,
	'cl61': cl61,
	'blview': blview,
	'cl51': cl51,
	'cl31': cl31,
	'mpl': mpl,
	'mpl2nc': mpl2nc,
	'minimpl': mpl,
	'cosp': default,
	'caliop': caliop,
}
