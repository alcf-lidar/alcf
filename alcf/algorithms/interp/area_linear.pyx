cimport cython
cimport numpy as np
import numpy as np
from libc.math cimport isnan

def interp(
	np.ndarray[double, ndim=1] x not None,
	np.ndarray[double, ndim=1] xhalf not None,
	np.ndarray[double, ndim=1] y not None,
	np.ndarray[double, ndim=1] x2 not None,
	np.ndarray[double, ndim=1] xhalf2 not None
):
	cdef long n = len(x)
	cdef long n2 = len(x2)
	cdef np.ndarray[double, ndim=1] y2 = np.full(n2, np.nan, dtype=np.float64)
	cdef long i = 0
	cdef long i2 = 0
	cdef double dxa = 0
	cdef double dxb = 0
	cdef double dxtot = 0
	cdef double a = 0
	cdef double b = 0
	cdef double atmp = 0
	cdef double btmp = 0
	cdef double fa = 0
	cdef double fb = 0
	cdef double ya = 0
	cdef double yb = 0
	while i < n and xhalf[i+1] < xhalf2[0]:
		i += 1
	if i == n:
		return y2
	while i2 < n2 and xhalf2[i2] < xhalf[-1]:
		dxtot = 0
		while i < n and xhalf[i] < xhalf2[i2+1]:
			a = max(xhalf[i], xhalf2[i2])
			b = min(xhalf[i+1], xhalf2[i2+1])
			# Left arm.
			atmp = min(a, x[i])
			btmp = min(b, x[i])
			dx = btmp - atmp
			if dx > 0:
				dxa = x[i] - atmp
				dxb = x[i] - btmp
				assert(dxa >= 0)
				assert(dxb >= 0)
				if i > 0:
					fa = dxa/(x[i] - x[i-1])
					ya = y[i-1]*fa + y[i]*(1 - fa)
					fb = dxb/(x[i] - x[i-1])
					yb = y[i-1]*fb + y[i]*(1 - fb)
				else:
					ya = y[i]
					yb = y[i]
				if isnan(y2[i2]):
					y2[i2] = 0
				y2[i2] += 0.5*(ya + yb)*dx
				dxtot += dx
			# Right arm.
			atmp = max(a, x[i])
			btmp = max(b, x[i])
			dx = btmp - atmp
			if dx > 0:
				dxa = atmp - x[i]
				dxb = btmp - x[i]
				assert(dxa >= 0)
				assert(dxb >= 0)
				if i < n - 1:
					fa = dxa/(x[i+1] - x[i])
					ya = y[i]*(1 - fa) + y[i+1]*fa
					fb = dxb/(x[i+1] - x[i])
					yb = y[i]*(1 - fb) + y[i+1]*fb
				else:
					ya = y[i]
					yb = y[i]
				if isnan(y2[i2]):
					y2[i2] = 0
				y2[i2] += 0.5*(ya + yb)*dx
				dxtot += dx
			i += 1
		if i > 0:
			i -= 1
		if dxtot > 0:
			y2[i2] /= dxtot
		i2 += 1
	return y2
