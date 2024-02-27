from subprocess import check_call, call
import sys
import os
import re
import glob
import tempfile
import shutil

TYPES = {
	'amps': {
		'ext': ['grb'],
		'outfile_is_directory': True,
		'cmdf': lambda infile, outfile: ['ncl_convert2nc', infile, '-o', outfile],
	},
	'cl31': {
		'ext': ['dat', 'DAT', 'asc', 'ASC'],
		'cmdf': lambda infile, outfile: ['cl2nc', infile, outfile],
	},
	'cl51': {
		'ext': ['dat', 'DAT', 'asc', 'ASC'],
		'cmdf': lambda infile, outfile: ['cl2nc', infile, outfile],
	},
	'jra55': {
		'ext': [None],
		'cmdf': lambda infile, outfile: ['grib_to_netcdf', '-o', outfile, infile],
	},
	'mpl': {
		'ext': ['mpl', 'MPL'],
		'cmdf': lambda infile, outfile: ['mpl2nc', infile, outfile],
	},
}

def find(input_, output, inext, outext, recursive=False):
	if not input_.endswith('/'):
		input_ += '/'
	if recursive:
		path = '**' if inext is None else '**/*.' + glob.escape(inext)
	else:
		path = '*' if inext is None else '*.' + glob.escape(inext)
	pattern = os.path.join(glob.escape(input_), path)
	files = sorted(glob.glob(pattern, recursive=recursive))
	input2 = []
	output2 = []
	for file_ in files:
		if not os.path.isfile(file_):
			continue
		if not file_.startswith(input_):
			continue
		infile = file_[len(input_):]
		if inext is not None and infile.endswith('.' + inext):
			outfile = infile[:-len(inext)] + outext
		else:
			outfile = infile + '.' + outext
		input2 += [os.path.join(input_, infile)]
		output2 += [os.path.join(output, outfile)]
	return input2, output2

def run(type_, input_, output, *args, **kwargs):
	"""
alcf-convert -- Convert input instrument or model data to NetCDF.
============

Synopsis
--------

    alcf convert [options] <type> [--] <input> <output>

Description
-----------

Arguments following `--` are treated as literal strings. Use this delimiter if the input or output file names might otherwise be interpreted as non-strings, e.g. purely numerical file names.

Arguments
---------

- `type`: Input data type (see Types below).
- `input`: Input filename or dirname. If `input` is a directory, all data files ending with the correct file extension (see Types below) in `input` are converted to corresponding `.nc` files in the directory `output`. If the option `-r` is supplied, the directory is processed recursively.
- `output`: Output filename or dirname.

Options
-------

- `-r`: Process the input directory recursively. The same directory structure is created under `output`.

Types
-----

- `amps`: Antarctic Mesoscale Prediction System (AMPS) GRIB files. Input file extension `.grb`.
- `cl31`: Vaisala CL31. Input file extension `.dat`, `.DAT`, `.asc` or `.ASC`.
- `cl51`: Vaisala CL51. Input file extension `.dat`, `.DAT`, `.asc` or `.ASC`.
- `jra55`: JRA-55 reanalysis. No input file extension.
- `mpl`: MiniMPL or MPL. Input file extension `.mpl` or `.MPL`.

Examples
--------

Convert raw Vaisala CL51 data in `cl51_dat` to NetCDF and store the output in the directory `cl51_nc`.

    alcf convert cl51 cl51_dat cl51_nc

Convert JRA-55 data in `jra55_grib` to NetCDF and store the output in the directory `jra55_nc`.

    alcf convert jra55 jra55_grib jra55_nc
	"""
	recursive = kwargs.get('r', False)

	if type_ not in TYPES:
		raise ValueError('Invalid type: %s' % type_)
	desc = TYPES[type_]

	if os.path.isdir(input_) and not os.path.isdir(output):
		raise IOError('%s: the output path does not exist or is not a directory' % output)

	if os.path.isfile(input_) and os.path.isdir(output):
		basename = os.path.basename(input_)
		for ext in desc['ext']:
			if ext is not None and basename.endswith('.' + ext):
				basename = basename[:-(len(ext) + 1)]
				break
		output = os.path.join(output, basename + '.nc')

	if os.path.isdir(input_):
		input2 = []
		output2 = []
		for ext in desc['ext']:
			in_, out = find(input_, output, ext, 'nc',
				recursive=recursive)
			input2 += in_
			output2 += out
	else:
		input2, output2 = [input_], [output]

	for infile, outfile in zip(input2, output2):
		if recursive:
			os.makedirs(os.path.dirname(outfile), exist_ok=True)
		if desc.get('outfile_is_directory'):
			with tempfile.TemporaryDirectory() as tmpdir:
				cmd = desc['cmdf'](infile, tmpdir)
				print(' '.join(cmd))
				call(cmd, stdout=sys.stdout, stderr=sys.stderr)
				name = os.path.splitext(os.path.basename(infile))[0]
				filename = os.path.join(tmpdir, name + '.nc')
				shutil.move(filename, outfile)
		else:
			cmd = desc['cmdf'](infile, outfile)
			print(' '.join(cmd))
			call(cmd, stdout=sys.stdout, stderr=sys.stderr)
