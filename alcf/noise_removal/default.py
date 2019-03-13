def noise_removal(d):
	b = d['backscatter']
	z = d['zfull']
	b_top = b[:,-1]
	z_top = z[-1]
	p = np.percentile(b_top, p)
	n, m = b.shape
	bp = np.zeros((n, m), np.float64)
	f = (1.0*z/zt)**2
	noise_mean = np.mean(bt)
	noise_sd = np.std(bt)
	if sd:
		for i in range(b.shape[0]):
			bp[i] = b[i] - noise_mean*f
		return bp, noise_sd*f
	else:
		for i in range(b.shape[0]):
			bp[i] = b[i] - p*f
		bp[bp < 0] = 0
		return bp
