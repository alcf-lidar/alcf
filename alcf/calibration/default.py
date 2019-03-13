def calibration(d, calibration_coeff=1.0):
	if 'backscatter' in d:
		d['backscatter'] *= calibration_coeff
	if 'backscatter_sd' in d:
		d['backscatter_sd'] *= calibration_coeff
