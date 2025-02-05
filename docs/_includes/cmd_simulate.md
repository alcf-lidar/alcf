
alcf-simulate -- Simulate lidar measurements from model data using COSP.
=============

Synopsis
--------

    alcf simulate <type> [<options>] [--] <input> <output>

Description
-----------

Arguments following `--` are treated as literal strings. Use this delimiter if the input or output file names might otherwise be interpreted as non-strings, e.g. purely numerical file names.

Arguments
---------

- `type`: Type of lidar to simulate.
- `input`: Input filename or directory (the output of "alcf model").
- `output`: Output filename or directory.
- `options`: See Options below.

Types
-----

- `caliop`: CALIPSO/CALIOP.
- `chm15k`: Lufft CHM 15k.
- `ct25k`: Vaisala CT25K. IMPORTANT: The simulator currently assumes wavelength of 910 nm instead of the actual instrument wavelength of 905 nm.
- `cl31`: Vaisala CL31.
- `cl51`: Vaisala CL51.
- `cl61`: Vaisala CL61.
- `minimpl`: Sigma Space MiniMPL.
- `mpl`: Sigma Space MPL.

Options
-------

- `keep_vars: { <var>... }`: Keep the listed input variables. The variables are expected to be prefixed with `input_` in the input. Default: `{ }`.
- `ncolumns: <ncolumns>`: Number of SCOPS subcolumns to generate. Default: `10`.
- `overlap: <overlap>`: Cloud overlap assumption in the SCOPS subcolumn generator. `maximum` for maximum overlap, `random` for random overlap, or `maximum-random` for maximum-random overlap. Default: `maximum-random`.

Examples
--------

Simulate a Vaisala CL51 instrument from model data in `alcf_merra2_model` previously extracted using `alcf model` and store the output in the direcctory `alcf_merra2_simulate`.

    alcf simulate cl51 alcf_merra2_model alcf_merra2_simulate
	