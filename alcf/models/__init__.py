META = {
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
	'zfull': {
		'.dims': ['time', 'level'],
		'standard_name': 'height_above_reference_ellipsoid',
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
	'cl': {
		'.dims': ['time', 'level'],
		'standard_name': 'cloud_area_fraction_in_atmosphere_layer',
		'units': '%',
	},
	'orog': {
		'.dims': ['time'],
		'standard_name': 'surface_altitude',
		'units': 'm',
	},
}

from . import cmip5
from . import merra2
from . import amps
from . import nzcsm
from . import nzesm

MODELS = {
	'amps': amps,
	#'cmip5': cmip5,
	#'jra55': jra55,
	'merra2': merra2,
	'nzcsm': nzcsm,
	'nzesm': nzesm,
}
