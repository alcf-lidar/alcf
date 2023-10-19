import numpy as np
import ds_format as ds
from alcf import misc
from alcf.lidars import META

WAVELENGTH = 1064 # nm
CALIBRATION_COEFF = 1.0
SURFACE_LIDAR = None
SC_LR = None

def read(filename, vars, altitude=None, lon=None, lat=None, time=None, **kwargs):
	sel = None
	if time is not None:
		d = ds.read(filename, 'time_bnds', jd=True)
		mask = misc.time_mask(d['time_bnds'], time[0], time[1])
		if np.sum(mask) == 0: return None
		sel = {'time': mask}

	d = ds.read(filename, vars, sel=sel)
	n = d['backscatter'].shape[0]
	d['altitude'] = d['altitude'] if altitude is None and 'altitude' in d else \
		np.full(n, altitude, np.float64)
	d['lon'] = d['lon'] if lon is None and 'lon' in d else \
		np.full(n, lon, np.float64)
	d['lat'] = d['lat'] if lat is None and 'lat' in d else \
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

