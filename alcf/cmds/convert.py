from subprocess import check_call, call
import sys
import os
import re

def dir_all(input_, output, inext, outext):
	files = sorted(os.listdir(input_))
	input2 = []
	output2 = []
	for file in files:
		if inext is not None:
			if not file.endswith('.' + inext):
				continue
			file2 = re.sub(r'\.' + inext + r'$', '.' + outext, file)
		else:
			file2 = file + '.nc'
		input2 += [os.path.join(input_, file)]
		output2 += [os.path.join(output, file2)]
	return input2, output2

def cl51(input_, output):
	if os.path.isdir(input_):
		input2, output2 = dir_all(input_, output, 'DAT', 'nc')
	else:
		input2, output2 = [input_], [output]
	for infile, outfile in zip(input2, output2):
		cmd = ['cl2nc', infile, outfile]
		print(' '.join(cmd))
		call(cmd, stdout=sys.stdout, stderr=sys.stderr)

def grib(input_, output):
	if os.path.isdir(input_):
		input2, output2 = dir_all(input_, output, None, 'nc')
	else:
		input2, output2 = [input_], [output]
	for infile, outfile in zip(input2, output2):
		cmd = ['grib_to_netcdf', '-o', outfile, infile]
		print(' '.join(cmd))
		call(cmd, stdout=sys.stdout, stderr=sys.stderr)

def mpl(input_, output):
	if os.path.isdir(input_):
		input2, output2 = dir_all(input_, output, 'mpl', 'nc')
	else:
		input2, output2 = [input_], [output]
	for infile, outfile in zip(input2, output2):
		cmd = ['mpl2nc', infile, outfile]
		print(' '.join(cmd))
		call(cmd, stdout=sys.stdout, stderr=sys.stderr)

TYPES = {
	'cl51': cl51,
	'jra55': grib,
	#'mpl': mpl,
}

def run(type_, input_, output, *args, **kwargs):
	"""
alcf convert - convert input instrument or model data to NetCDF

Usage: `alcf convert <type> <input> <output>`

- `type`: input data type (see Types below)
- `input`: input filename or dirname
- `output`: output filename or dirname

Types:

- `cl51`: Vaisala CL51 (converted with cl2nc)
- `jra55`: JRA-55 (converted with grib_to_netcdf)

If `input` is a directory, all data files in `input` are converted
to corresponding .nc files in `output`.

Examples:

Convert raw Vaisala CL51 data in `cl51_dat` to NetCDF and store the output in
the directory `cl51_nc`.

    alcf convert cl51 cl51_dat cl51_nc

Convert JRA-55 data in `jra55_grib` to NetCDF and store the output in the
directory `jra55_nc`.

    alcf convert jra55 jra55_grib jra55_nc
	"""

	func = TYPES.get(type_)
	if func is None:
		raise ValueError('Invalid type: %s' % type_)
	func(input_, output)
