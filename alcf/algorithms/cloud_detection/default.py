#!/usr/bin/env python

import sys
import ds_format as ds
import numpy as np
from scipy.stats import norm
from scipy.optimize import minimize_scalar
from alcf import misc

def cloud_detection(d,
	cloud_threshold=2e-6,
	cloud_threshold_exp=None,
	cloud_nsd=5,
	bsd=None,
	bsd_z=8000,
	**options
):
	b = d['backscatter']
	if b.ndim == 3:
		n, m, l = b.shape
	else:
		n, m = b.shape

	if bsd is None:
		bsd2 = d.get('backscatter_sd')
	else:
		bsd2 = np.full(b.shape, bsd, np.float64)
		f = (d['zfull']/bsd_z)**2
		if b.ndim == 3:
			for i in range(b.shape[2]):
				bsd2[:,:,i] *= f
		else:
			bsd2 *= f
	bmol = d.get('backscatter_mol')
	x = np.copy(b)
	if bsd2 is not None:
		x -= cloud_nsd*bsd2
	if bmol is not None:
		if len(x.shape) == 3:
			for i in range(x.shape[2]):
				x[:,:,i] -= bmol
		else:
			x -= bmol

	cloud_mask = np.zeros(x.shape, np.byte)
	if cloud_threshold_exp is not None:
		ct_x, ct_y, ct_h = cloud_threshold_exp
		for i in range(n):
			alt = 0 if np.isnan(d['altitude'][i]) else d['altitude'][i]
			height = d['zfull'] - alt
			height[height < 0] = 0
			ct = ct_y + (ct_x - ct_y)*0.5**(height/ct_h)
			if x.ndim == 3:
				for k in range(l):
					cloud_mask[i,:,k] = x[i,:,k] >= ct
			else:
				cloud_mask[i,:] = x[i,:] >= ct
	else:
		cloud_mask[::] = x >= cloud_threshold

	d['cloud_mask'] = cloud_mask
	d['.']['cloud_mask'] = {
		'.dims': d['.']['backscatter']['.dims'],
		'long_name': 'cloud mask',
		'units': '1',
	}

def stream(dd, state, **options):
	return misc.stream(dd, state, cloud_detection, **options)
