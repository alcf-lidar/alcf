import numpy as np
import ds_format as ds
from alcf.lidars import META

WAVELENGTH = 1064 # nm
CALIBRATION_COEFF = 1.0
SURFACE_LIDAR = None
SC_LR = None

def read(filename, vars, altitude=None, lon=None, lat=None, **kwargs):
	d = ds.from_netcdf(filename, vars)
	n = d['backscatter'].shape[0]
	d['altitude'] = d['altitude'] if altitude is None and 'altitude' in d else \
		np.full(n, altitude, np.float64)
	d['lon'] = d['lon'] if lon is None and 'longitude' in d else \
		np.full(n, lon, np.float64)
	d['lat'] = d['lat'] if lat is None and 'latitude' in d else \
		np.full(n, lat, np.float64)
	d['.']['altitude'] = META['altitude']
	d['.']['lon'] = META['lon']
	d['.']['lat'] = META['lat']
	d['.'] = {
		x: d['.'][x]
		for x in vars
		if x in d['.']
	}
	return d

