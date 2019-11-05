import numpy as np
import ds_format as ds

WAVELENGTH = 1064
CALIBRATION_COEFF = 1.0
SURFACE_LIDAR = None

def read(filename, vars):
	d = ds.from_netcdf(filename, vars)
	return d
