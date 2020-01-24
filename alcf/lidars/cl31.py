import numpy as np
import ds_format as ds
import datetime as dt
from alcf.lidars import META
from alcf.lidars import cl51

WAVELENGTH = 910 # nm
CALIBRATION_COEFF = 1.45e-3
SURFACE_LIDAR = True
SC_LR = 18.8 # sr. Stratocumulus lidar ratio (O'Connor et al., 2004).
MAX_RANGE = 7700 # m

def read(filename, vars, **kwargs):
	return cl51.read(filename, vars,
		calibration_coeff=CALIBRATION_COEFF,
		**kwargs
	)

