
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
	