import numpy as np
import ds_format as ds
import datetime as dt
from alcf import misc
from alcf.lidars import META

VARS = {
	'backscatter': ['backscatter'],
}

DEFAULT_VARS1 = [
	'time',
	'detection_status',
]

DEFAULT_VARS2 = [
	'vertical_resolution',
	'range',
	'level',
]

def params(type_):
	return {
		'wavelength': {
			'ct25k': 910, # nm. This should be 905 nm, but for compatibility
			              # with the supported simulator wavelengths, we set it
			              # to 910 nm.
			'cl31': 910, # nm
			'cl51': 910, # nm
		}[type_],
		'calibration_coeff': {
			'ct25k': 1.45e-3,
			'cl31': 1.45e-3,
			'cl51': 1.2e-3,
		}[type_],
		'surface_lidar': True,
		'sc_lr': 18.8, # sr. Stratocumulus lidar ratio (O'Connor et al., 2004).
		'max_range': {
			'ct25k': 7680,
			'cl31': 7700,
			'cl51': 15400,
		}[type_], # m
	}

def read(type_, filename, vars,
	altitude=None,
	fix_cl_range=False,
	cl_crit_range=6000,
	tlim=None,
	keep_vars=[],
	**kwargs
):
	p = params(type_)
	sel = None
	if tlim is not None:
		d = ds.read(filename, 'time', jd=True)
		misc.require_vars(d, ['time'])
		d['time_bnds'] = misc.time_bnds(d['time'])
		mask = misc.time_mask(d['time_bnds'], tlim[0], tlim[1])
		if np.sum(mask) == 0: return None
		sel = {'time': mask}

	dep_vars = misc.dep_vars(VARS, vars)
	req_vars = dep_vars + DEFAULT_VARS1 + keep_vars
	vars_ = req_vars + DEFAULT_VARS2
	d = ds.read(filename, vars_, jd=True, sel=sel, full=True)
	misc.require_vars(d, req_vars)
	dx = {}
	misc.populate_meta(dx, META, set(vars) & set(VARS))
	n = ds.dim(d, 'time')
	if 'time' in vars:
		dx['time'] = d['time']
	if 'time_bnds' in vars:
		args = [] if tlim is None else [tlim[0], tlim[1]]
		dx['time_bnds'] = misc.time_bnds(d['time'], None, *args)
	if 'range' in d: # ARM CL51 format.
		range_ = d['range']
	elif 'vertical_resolution' in d: # Generic CL51 format.
		range_ = d['vertical_resolution'][0]*d['level']
	else:
		raise ValueError('Variable "range" or "level" and "vertical_resolution" is required')
	if 'zfull' in vars:
		zfull1 = range_
		dx['zfull'] = np.tile(zfull1, (n, 1))
		if altitude is not None:
			dx['zfull'] += altitude
	if 'backscatter' in vars:
		factor = 1e-4 if (d['.']['backscatter']['units'] == '1/(sr*km*10000)') \
			else 1 # Factor of 1e-4 if ARM CL51 format.
		dx['backscatter'] = d['backscatter']*p['calibration_coeff']*factor
		mask = range_ > 6000
		if fix_cl_range is True:
			for i in range(n):
				if d['detection_status'][i] == b'0':
					dx['backscatter'][i,mask] *= (range_[mask]/6000)**2
	for var in keep_vars:
		misc.keep_var(var, d, dx)
	return dx
