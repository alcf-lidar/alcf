#!/usr/bin/env python

import sys
import numpy as np
from alcf import misc

def cloud_base_detection(d, **options):
	cloud_mask = d['cloud_mask']
	if len(cloud_mask.shape) == 3:
		n, m, l = d['cloud_mask'].shape
		dims = (n,l)
		dimnames = ('time', 'column')
	else:
		n, m = d['cloud_mask'].shape
		l = 1
		dims = (n,)
		dimnames = ('time',)
	cbh = np.zeros(dims, dtype=np.float64)
	for i in range(n):
		for j in range(l):
			x = cloud_mask[i,:,j] if len(dims) == 2 \
				else cloud_mask[i,:]
			kk = np.where(x == 1)[0]
			if np.any(np.isnan(x)):
				v = np.nan
			elif len(kk) > 0:
				v = d['zfull'][kk[0]]
			else:
				v = np.inf
			if len(dims) == 2:
				cbh[i,j] = v
			else:
				cbh[i] = v
	d['cbh'] = cbh
	d['.']['cbh'] = {
		'.dims': dimnames,
		'long_name': 'cloud base height',
		'units': 'm',
	}

def stream(dd, state, **options):
	return misc.stream(dd, state, cloud_base_detection, **options)
