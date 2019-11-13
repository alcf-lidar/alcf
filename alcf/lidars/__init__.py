META = {
	'time': {
		'.dims': ['time'],
		'long_name': 'time',
		'units': 'days since -4712-01-01T12:00',
	},
	'zfull': {
		'.dims': ['time', 'level'],
		'long_name': 'height_above_reference_ellipsoid',
		'units': 'm',
	},
	'backscatter': {
		'.dims': ['time', 'level'],
		'long_name': 'backscatter',
		'units': 'm-1 sr-1',
	},
}

from . import chm15k
from . import cl51
from . import mpl
from . import cosp
from . import caliop

LIDARS = {
	'chm15k': chm15k,
	'cl51': cl51,
	'cl31': cl51,
	'mpl': mpl,
	'minimpl': mpl,
	'cosp': cosp,
	'caliop': caliop,
}
