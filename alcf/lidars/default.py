import numpy as np
import ds_format as ds
from alcf import misc
from alcf.lidars import META

WAVELENGTH = 1064 # nm
CALIBRATION_COEFF = 1.0
SURFACE_LIDAR = None
SC_LR = None

def read(filename, vars,
	altitude=None,
	time=None,
	keep_vars=[],
	**kwargs
):
	sel = None
	if time is not None:
		d = ds.read(filename, 'time_bnds', jd=True)
		mask = misc.time_mask(d['time_bnds'], time[0], time[1])
		if np.sum(mask) == 0: return None
		sel = {'time': mask}

	d = ds.read(filename, vars, sel=sel)
	n = d['backscatter'].shape[0]
	return d
