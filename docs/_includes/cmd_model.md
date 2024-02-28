
alcf-model -- Extract model data at a point or along a track.
==========

Synopsis
--------

    alcf model <type> point: { <lon> <lat> } time: { <start> <end> } [options] [--] <input> <output>

    alcf model <type> track: <track> [--] <input> <output>

Description
-----------

Arguments following `--` are treated as literal strings. Use this delimiter if the input or output file names might otherwise be interpreted as non-strings, e.g. purely numerical file names.

Arguments
---------

- `type`: Input data type (see Types below).
- `input`: Input directory.
- `output`: Output directory.
- `lon`: Point longitude.
- `lat`: Point latitutde.
- `start`: Start time (see Time format below).
- `end`: End time (see Time format below).
- `track: <file>`, `track: { <file>... }`: One or more track NetCDF files (see Files below). If multiple files are supplied and `time_bnds` is not present in the files, they are assumed to be multiple segments of a discontinous track unless the last and first time of adjacent tracks are the same.
- `options`: See Options below.

Options
-------

- `njobs: <n>`: Number of parallel jobs. Default: number of CPU cores.
- `-r`: Process the input directory recursively.
- `--track_lon_180`: Expect track longitude between -180 and 180 degrees.
- `override_year: <year>`: Override year in the track. Use if comparing observations with a model statistically and the model output does not have a corresponding year available. The observation time is converted to the same time relative to the start of the year in the specified year. Note that if the original year is a leap year and the override year is not, as a consequence of the above 31 December is mapped to 1 January. The output retains the original year as in the track, even though the model data come from the override year. Default: `none`.

Types
-----

- `amps`: Antarctic Mesoscale Prediction System (AMPS).
- `era5`: ERA5.
- `icon`: ICON.
- `icon_intake_healpix`: ICON through Intake-ESM on HEALPix grid.
- `jra55`: JRA-55.
- `merra2`: Modern-Era Retrospective Analysis for Research and Applications, Version 2 (MERRA-2).
- `nzcsm`: New Zealand Convection Scale Model (NZCSM).
- `nzesm`: New Zealand Earth System Model (NZESM). [Experimental]
- `um`: UK Met Office Unified Model (UM).

Time format
-----------

`YYYY-MM-DD[THH:MM[:SS]]`, where `YYYY` is year, `MM` is month, `DD` is day, `HH` is hour, `MM` is minute, `SS` is second. Example: `2000-01-01T00:00:00`.

Files
-----

The track file is a NetCDF file containing 1D variables `lon`, `lat`, `time`, and optionally `time_bnds`. `time` and `time_bnds` are time in format conforming with the CF Conventions (has a valid `units` attribute and optional `calendar` attribute), `lon` is longitude between 0 and 360 degrees and `lat` is latitude between -90 and 90 degrees. If `time_bnds` is provided, discontinous track segments can be specified if adjacent time bounds are not coincident. The variables `lon`, `lat` and `time` have a single dimension `time`. The variable `time_bnds` has dimensions (`time`, `bnds`).

Examples
--------

Extract MERRA-2 model data in `M2I3NVASM.5.12.4` at 45 S, 170 E between 1 and 2 January 2020 and store the output in the directory `alcf_merra2_model`.

    alcf model merra2 point: { -45.0 170.0 } time: { 2020-01-01 2020-01-02 } M2I3NVASM.5.12.4 alcf_merra2_model
	