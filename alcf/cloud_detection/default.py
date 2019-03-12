#!/usr/bin/env python

import sys
import ds_format as ds
import numpy as np
from scipy.stats import norm
from scipy.optimize import minimize_scalar

def cloud_detection(d, cloud_threshold=20e-6):
	backscatter = d['backscatter']
	backscatter_sd = d.get('backscatter_sd')
	zfull = d['zfull']
	cloud_mask = (backscatter >= cloud_threshold).astype(np.byte)

	d['cloud_mask'] = cloud_mask
	d['.']['cloud_mask'] = {
		'.dims': d['.']['backscatter']['.dims'],
		'long_name': 'cloud_mask',
		'units': '1',
	}
