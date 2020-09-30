#!/usr/bin/env python

import sys
import ds_format as ds
import numpy as np
from scipy.stats import norm
from scipy.optimize import minimize_scalar
from alcf import misc

def cloud_detection(d, cloud_threshold=2e-6, cloud_nsd=5, **options):
	b = d['backscatter']
	bsd = d.get('backscatter_sd')
	bmol = d.get('backscatter_mol')
	x = np.copy(b)
	if bsd is not None:
		x -= cloud_nsd*bsd
	if bmol is not None:
		if len(x.shape) == 3:
			for i in range(x.shape[2]):
				x[:,:,i] -= bmol
		else:
			x -= bmol
	cloud_mask = (x >= cloud_threshold).astype(np.byte)
	d['cloud_mask'] = cloud_mask
	d['.']['cloud_mask'] = {
		'.dims': d['.']['backscatter']['.dims'],
		'long_name': 'cloud mask',
		'units': '1',
	}

def stream(dd, state, **options):
	return misc.stream(dd, state, cloud_detection, **options)
