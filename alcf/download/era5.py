import os
from getpass import getpass

LOGIN_URL = b'https://cds.climate.copernicus.eu/api/v2'

PRODUCTS = ['surf', 'plev']

VARS_SURF = [
	'geopotential',
	'surface_pressure',
]

VARS_PLEV = [
	'fraction_of_cloud_cover',
	'geopotential',
	'specific_cloud_ice_water_content',
	'specific_cloud_liquid_water_content',
	'temperature',
]

TYPE_SURF = 'reanalysis-era5-single-levels'
TYPE_PLEV = 'reanalysis-era5-pressure-levels'

TIME = [
	'00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00',
	'08:00', '09:00', '10:00', '11:00',	'12:00', '13:00', '14:00', '15:00',
	'16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'
]

PRESSURE_LEVEL = [
	'1', '2', '3', '5', '7', '10', '20', '30', '50', '70', '100', '125', '150',
	'175', '200', '225', '250', '300', '350', '400', '450', '500', '550', '600',
	'650', '700', '750', '775', '800', '825', '850', '875', '900', '925', '950',
	'975', '1000'
]

def login(uid=None, key=None, overwrite=False):
	if uid is None:
		uid = input('Copernicus CDS UID: ')
	if key is None:
		key = getpass(prompt='Copernicus CDS API key: ')
	if type(uid) is not str:
		uid = str(uid)
	if type(key) is not str:
		key = str(key)

	home = os.path.expanduser("~")
	cdsapirc = os.path.join(home, '.cdsapirc')

	if os.path.exists(cdsapirc) and overwrite is False:
		print('The following files have to be overwritten:')
		print('    ' + cdsapirc)
		res = input('Continue [y/n]? ')
		if res != 'y':
			return

	with open(cdsapirc, 'wb',
		opener=lambda p, f: os.open(p, f, mode=0o600)) as f:
		os.chmod(f.fileno(), 0o600)
		f.write(b'url: %s\n' % LOGIN_URL)
		f.write(b'key: %s:%s\n' % (uid.encode('utf-8'), key.encode('utf-8')))
	print('-> %s' % cdsapirc)

def download(filename, product, year, month, day, lon1, lon2, lat1, lat2,
	nocache=False
):
	import cdsapi
	type_ = {
		'surf': TYPE_SURF,
		'plev': TYPE_PLEV,
	}[product]
	vars_ = {
		'surf': VARS_SURF,
		'plev': VARS_PLEV,
	}[product]
	lon1_180 = lon1 if lon1 < 180 else lon1 - 360
	lon2_180 = lon2 if lon2 < 180 else lon2 - 360
	req = {
			'product_type': 'reanalysis',
			'format': 'netcdf',
			'variable': vars_,
			'time': TIME,
			'area': [lat2, lon1_180, lat1, lon2_180],
			'year': '%d' % year,
			'month': '%d' % month,
			'day': '%d' % day,
	}
	if type_ == 'surf':
		req['pressure_level'] = PRESSURE_LEVEL
	if nocache:
		req['nocache'] = str(random.randint(0, 2147483647))
	c = cdsapi.Client()
	c.retrieve(type_, req, filename)
