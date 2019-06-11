from alcf import misc

def calibration(d, calibration_coeff=1.0, **options):
	if 'backscatter' in d:
		d['backscatter'] *= calibration_coeff
	if 'backscatter_mol' in d:
		d['backscatter_mol'] *= calibration_coeff
	if 'backscatter_sd' in d:
		d['backscatter_sd'] *= calibration_coeff

def stream(dd, state, **options):
	return misc.stream(dd, state, calibration, **options)
