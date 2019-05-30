#!/usr/bin/env python

import sys
import ds_format as ds
import numpy as np
from scipy.stats import norm
from scipy.optimize import minimize_scalar
from alcf import misc

def cloud_detection(d, cloud_threshold=10e-6, cloud_nsd=3, **options):
	b = d['backscatter']
	b_sd = d.get('backscatter_sd')
	if b_sd is not None:
		cloud_mask = (b - cloud_nsd*b_sd >= cloud_threshold).astype(np.byte)
	else:
		cloud_mask = (b >= cloud_threshold).astype(np.byte)
	d['cloud_mask'] = cloud_mask
	d['.']['cloud_mask'] = {
		'.dims': d['.']['backscatter']['.dims'],
		'long_name': 'cloud_mask',
		'units': '1',
	}

def stream(dd, state, **options):
	return misc.stream(dd, state, cloud_detection, **options)
