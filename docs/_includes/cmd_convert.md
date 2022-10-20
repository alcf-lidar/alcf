
alcf-convert -- Convert input instrument or model data to NetCDF.
============

Synopsis
--------

    alcf convert <type> <input> <output>

Arguments
---------

- `type`: Input data type (see Types below).
- `input`: Input filename or dirname. If `input` is a directory, all data files in `input` are converted to corresponding .nc files in the directory `output`.
- `output`: Output filename or dirname.

Types
-----

- `cl51`: Vaisala CL51 (converted with cl2nc).
- `jra55`: JRA-55 (converted with grib_to_netcdf).

Examples
--------

Convert raw Vaisala CL51 data in `cl51_dat` to NetCDF and store the output in
the directory `cl51_nc`.

    alcf convert cl51 cl51_dat cl51_nc

Convert JRA-55 data in `jra55_grib` to NetCDF and store the output in the
directory `jra55_nc`.

    alcf convert jra55 jra55_grib jra55_nc
	