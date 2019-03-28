import numpy as np
from alcf import misc

def zsampling(d, zres=None, zlim=None):
	b = d['backscatter']
	b_sd = d['backscatter_sd']
	zfull = d['zfull']
	r = d['range']
	n, m = b.shape
	if m == 0:
		return
	if zlim is None:
		zlim = zfull[0], zfull[-1]
	if zres is None:
		mask = (zfull >= zlim[0]) & (zfull <= zlim[1])
		r2 = r[mask]
		zfull2 = zfull[mask]
		b2 = b[:,mask]
		b_sd2 = b_sd[:,mask]
	else:
		zhalf2 = np.arange(zlim[0], zlim[-1] + zres, zres)
		zfull2 = (zhalf2[1:] + zhalf2[:-1])*0.5
		m2 = len(zfull2)
		b2 = np.zeros((n, m2), dtype=np.float64)
		b_sd2 = np.zeros((n, m2), dtype=np.float64)
		r2 = np.zeros(m2, dtype=np.float64)
		for i in range(m2):
			mask = (zfull >= zhalf2[i]) & (zfull < zhalf2[i+1])
			b2[:,i] = np.mean(b[:,mask], axis=1)
			b_sd2[:,i] = np.sqrt(np.mean(b_sd[:,mask]**2, axis=1))
			r2[i] = np.mean(r[mask])
	d['range'] = r2
	d['zfull'] = zfull2
	d['backscatter'] = b2
	d['backscatter_sd'] = b_sd2

def stream(dd, state, zres=None, zlim=None, **options):
	return misc.stream(dd, state, zsampling, zres=zres, zlim=zlim)
