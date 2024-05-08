import numpy as np

def interp(x, xhalf, y, x2, xhalf2):
	xext = np.concatenate(([xhalf[0]], x, [xhalf[-1]])) if len(x) > 0 else x
	yext = np.concatenate(([y[0]], y, [y[-1]])) if len(x) > 0 else y
	return np.interp(x2, xext, yext, left=np.nan, right=np.nan)
