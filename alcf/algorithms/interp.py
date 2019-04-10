import numpy as np

def interp(xhalf, y, xhalf2):
	"""Interpolate y(x) on x2"""
	n = len(xhalf)
	n2 = len(xhalf2)
	y2 = np.zeros(n2-1, dtype=np.float64)
	i = 0
	i2 = 0
	while i < n-1 and xhalf[i] < xhalf2[0]:
		i += 1
	if xhalf[i] < xhalf2[0]:
		return y2
	if i > 0:
		i -= 1
	while i2 < n2-1 and xhalf2[i2] < xhalf[-1]:
		dx2 = 0
		while i < n-1 and xhalf[i+1] < xhalf2[i2+1]:
			dx = xhalf[i+1] - max(xhalf2[i2], xhalf[i])
			if dx < 0:
				raise ValueError(xhalf[i+1], xhalf2[i2], xhalf[i])
			y2[i2] += y[i]*dx
			dx2 += dx
			i += 1
		if i < n-1 and xhalf[i] < xhalf2[i2+1]:
			dx = xhalf2[i2+1] - max(xhalf2[i2], xhalf[i])
			if dx < 0:
				raise ValueError(i, i2)
			y2[i2] += y[i]*dx
			dx2 += dx
		if dx2 > 0:
			y2[i2] /= dx2
		i2 += 1
	return y2
