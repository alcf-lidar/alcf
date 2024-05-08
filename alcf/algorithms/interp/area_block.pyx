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
	cdef double dx = 0
	cdef double dxtot = 0
	cdef double a = 0
	cdef double b = 0
	while i < n and xhalf[i+1] < xhalf2[0]:
		i += 1
	if i == n:
		return y2
	while i2 < n2 and xhalf2[i2] < xhalf[-1]:
		dxtot = 0
		while i < n and xhalf[i] < xhalf2[i2+1]:
			a = max(xhalf[i], xhalf2[i2])
			b = min(xhalf[i+1], xhalf2[i2+1])
			dx = b - a
			if dx > 0:
				if isnan(y2[i2]):
					y2[i2] = 0
				y2[i2] += y[i]*dx
				dxtot += dx
			i += 1
		if i > 0:
			i -= 1
		if dxtot > 0:
			y2[i2] /= dxtot
		i2 += 1
	return y2
