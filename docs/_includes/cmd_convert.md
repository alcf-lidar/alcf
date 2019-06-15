
alcf convert - convert input instrument or model data to ALCF standard NetCDF

Usage: `alcf convert <type> <input> <output>`

- `type`: input data type (see Types below)
- `input`: input filename or dirname
- `output`: output filename or dirname

Types:

- `cl51`: Vaisala CL51

If `input` is a directory, all .DAT files in `input` are converted
to corresponding .nc files in `output`.
	