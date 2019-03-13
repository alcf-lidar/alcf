import numpy as np
import ds_format as ds

wavelength = 1064
calibration_coeff = 1.0

def read(filename, vars):
	d = ds.from_netcdf(filename, vars)
	return d
