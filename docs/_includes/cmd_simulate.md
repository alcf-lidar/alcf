
alcf simulate - simulate lidar measurements from model data using COSP

Usage: `alcf simulate <type> <input> <output> [<options>]`

Arguments:

- `type`: type of lidar to simulate
- `input`: input filename or directory (the output of "alcf model")
- `output`: output filename or directory
- `options`: see Options below

Types:

- `chm15k`: Lufft CHM 15k
- `cl51`: Vaisala CL51
- `mpl`: Sigma Space MiniMPL

Options:

- `ncolumns: <ncolumns>`: Number of SCOPS subcolumns to generate. Default: `10`.
- `overlap: <overlap>`: Cloud overlap assumption in the SCOPS subcolumn
   generator. `maximum` for maximum overlap, `random` for random overlap, or
  `maximum-random` for maximum-random overlap. Default: `maximum-random`.
	