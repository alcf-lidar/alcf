
alcf-simulate -- Simulate lidar measurements from model data using COSP.
=============

Synopsis
--------

    alcf simulate <type> <input> <output> [<options>]

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
- `cl31`: Vaisala CL31.
- `cl51`: Vaisala CL51.
- `cl61`: Vaisala CL61.
- `mpl`: Sigma Space MiniMPL.

Options
-------

- `ncolumns: <ncolumns>`: Number of SCOPS subcolumns to generate. Default: `10`.
- `overlap: <overlap>`: Cloud overlap assumption in the SCOPS subcolumn generator. `maximum` for maximum overlap, `random` for random overlap, or `maximum-random` for maximum-random overlap. Default: `maximum-random`.

Examples
--------

Simulate a Vaisala CL51 instrument from model data in `alcf_merra2_model` previously extracted using `alcf model` and store the output in the direcctory `alcf_merra2_simulate`.

    alcf simulate cl51 alcf_merra2_model alcf_merra2_simulate
	