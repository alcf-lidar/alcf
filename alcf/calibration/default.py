def stream(dd, state, calibration_coeff=1.0):
	for d in dd:
		if 'backscatter' in d:
			d['backscatter'] *= calibration_coeff
		if 'backscatter_sd' in d:
			d['backscatter_sd'] *= calibration_coeff
