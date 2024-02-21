META = {
	'clw': {
		'.dims': ['time', 'level'],
		'long_name': 'mass fraction of cloud liquid water',
		'standard_name': 'mass_fraction_of_cloud_liquid_water_in_air',
		'units': '1',
	},
	'cli': {
		'.dims': ['time', 'level'],
		'long_name': 'mass fraction of cloud ice',
		'standard_name': 'mass_fraction_of_cloud_ice_in_air',
		'units': '1',
	},
	'ps': {
		'.dims': ['time'],
		'long_name': 'surface air pressure',
		'standard_name': 'surface_air_pressure',
		'units': 'Pa',
	},
	'pfull': {
		'.dims': ['time', 'level'],
		'long_name': 'pressure at model full-levels',
		'standard_name': 'air_pressure',
		'units': 'Pa',
	},
	'zfull': {
		'.dims': ['time', 'level'],
		'long_name': 'altitude of model full-levels',
		'standard_name': 'height_above_reference_ellipsoid',
		'units': 'm',
	},
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
		'standard_name': 'time_bounds',
		'units': 'days since -4713-11-24 12:00 UTC',
		'calendar': 'proleptic_gregorian',
	},
	'lon': {
		'.dims': ['time'],
		'long_name': 'longitude',
		'standard_name': 'longitude',
		'units': 'degrees_east',
	},
	'lat': {
		'.dims': ['time'],
		'long_name': 'latitude',
		'standard_name': 'latitude',
		'units': 'degrees_north',
	},
	'ta': {
		'.dims': ['time', 'level'],
		'long_name': 'air temperature',
		'standard_name': 'air_temperature',
		'units': 'K',
	},
	'cl': {
		'.dims': ['time', 'level'],
		'long_name': 'cloud area fraction',
		'standard_name': 'cloud_area_fraction_in_atmosphere_layer',
		'units': '%',
	},
	'orog': {
		'.dims': ['time'],
		'long_name': 'surface altitude',
		'standard_name': 'surface_altitude',
		'units': 'm',
	},
}

from . import amps
#from . import cmip5
from . import era5
from . import jra55
from . import merra2
from . import nzcsm
from . import nzesm
from . import um
from . import icon
from . import icon_intake_healpix

MODELS = {
	'amps': amps,
	#'cmip5': cmip5,
	'era5': era5,
	'jra55': jra55,
	'merra2': merra2,
	'nzcsm': nzcsm,
	'nzesm': nzesm,
	'um': um,
	'icon': icon,
	'icon_intake_healpix': icon_intake_healpix,
}
