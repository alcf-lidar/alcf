import numpy as np
from alcf import misc

def noise_removal(d, **options):
	pass
	# b = d['backscatter']
	# z = d['zfull']
	# b_top = b[:,-1]
	# z_top = z[-1]
	# # p = np.percentile(b_top, percentile)
	# n, m = b.shape
	# bp = np.zeros((n, m), np.float64)
	# scaling_factor = (1.0*z/z_top)**2
	# noise_mean = np.mean(b_top)
	# noise_sd = np.std(b_top)
	# if sd:
	# 	for i in range(b.shape[0]):
	# 		bp[i] = b[i] - noise_mean*scaling_factor
	# 	# return bp, noise_sd*scaling_factor
	# 	return bp
	# else:
	# 	for i in range(b.shape[0]):
	# 		bp[i] = b[i] - p*scaling_factor
	# 	bp[bp < 0] = 0
	# 	# return bp
	# 	return bp

def stream(dd, state, noise_removal_sampling=300, **options):
	aggregate_state = state.get('aggregate_state', {})
	dd = misc.aggregate(dd, aggregate_state, noise_removal_sampling/60./60./24.)
	return misc.stream(dd, state, noise_removal, **options)
