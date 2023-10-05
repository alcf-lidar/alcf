import numpy as np
import ds_format as ds
from alcf import misc
from alcf.algorithms import interp

def zsample(d, zres=None, zlim=None):
	n = ds.dim(d, 'time')
	m = ds.dim(d, 'level')
	l = ds.dim(d, 'column')
	if m == 0:
		return

	zfull = d['zfull']
	zhalf = np.zeros((n, m+1), dtype=np.float64)
	for i in range(n):
		zhalf[i,:] = misc.half(zfull[i,:]) \
			if zfull.ndim == 2 \
			else misc.half(zfull)
	zhalf2 = np.arange(zlim[0], zlim[-1] + zres, zres, np.float64)
	zfull2 = (zhalf2[1:] + zhalf2[:-1])*0.5
	m2 = len(zfull2)

	for var in ds.vars(d):
		dims = ds.dims(d, var)
		if var == 'zfull' or 'level' not in dims:
			continue
		x = ds.var(d, var)
		i = dims.index('time')
		j = dims.index('level')
		x = np.moveaxis(x, [i, j], [0, 1])
		shape = list(x.shape)
		x = x.reshape(n, m, -1)
		shape2 = list(x.shape)
		shape2[1] = m2
		l = shape2[2]
		x2 = np.zeros(shape2, dtype=x.dtype)
		if var == 'backscatter_sd':
			x = x**2
		for i2 in range(n):
			for j2 in range(l):
				x2[i2,:,j2] = interp(zhalf[i2,:], x[i2,:,j2], zhalf2)
		if var == 'backscatter_sd':
			x2 = np.sqrt(x2)
		x2 = x2.reshape([n, m2] + shape[2:])
		x2 = np.moveaxis(x2, [0, 1], [i, j])
		ds.var(d, var, x2)

	ds.var(d, 'zfull', zfull2)
	ds.dims(d, 'zfull', ['level'])

def stream(dd, state, zres=None, zlim=None, **options):
	return misc.stream(dd, state, zsample, zres=zres, zlim=zlim)
