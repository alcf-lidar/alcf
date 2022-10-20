
alcf-model -- Extract model data at a point or along a track.
==========

Synopsis
--------

    alcf model <type> point: { <lon> <lat> } time: { <start> <end> } <input> <output> [options]

    alcf model <type> track: <track> <input> <output>

Arguments
---------

- `type`: Input data type (see Types below).
- `input`: Input directory.
- `output`: Output directory.
- `lon`: Point longitude.
- `lat`: Point latitutde.
- `start`: Start time (see Time format below).
- `end`: End time (see Time format below).
- `track`: Track NetCDF file (see Files below).
- `options`: See Options below.

Options
-------

- `--track_lon_180`: Expect track longitude between -180 and 180 degrees.
- `track_override_year: <year>`: Override year in track. Use if comparing observations with a model statistically. Default: `none`.

Types
-----

- `amps`: Antarctic Mesoscale Prediction System (AMPS).
- `era5`: ERA5.
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

The track file is a NetCDF file containing 1D variables `lon`, `lat`, and `time`. `time` is time in format conforming with the NetCDF standard, `lon` is longitude between 0 and 360 degrees and `lat` is latitude between -90 and 90 degrees.

Examples
--------

Extract MERRA-2 model data in `M2I3NVASM.5.12.4` at 45 S, 170 E between 1 and 2 January 2020 and store the output in the directory `alcf_merra2_model`.

    alcf model merra2 point: { -45.0 170.0 } time: { 2020-01-01 2020-01-02 } M2I3NVASM.5.12.4 alcf_merra2_model
	