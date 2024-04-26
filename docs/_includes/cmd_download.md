
alcf-download -- Download model data.
=============

Synopsis
--------

    alcf download <type> [login_options] --login
    alcf download <type> point: { <lon> <lat> } time: { <start> <end> } [<options>] [--] <output>
    alcf download <type> track: <track> [<options>] [--] <output>

Description
-----------

This command downloads model data required by the lidar simulator for a given geographical point or ship track. Not all models supported by the other ALCF commands are supported by `alcf download` - these have to be acquired manually. Before downloading data, you have register an account on Copernicus CDS (ERA5; https://cds.climate.copernicus.eu) or NASA Earthdata (MERRA-2; https://earthdata.nasa.gov) and run `alcf download <type> --login`. This prompts for credentials interactively. For non-interactive use, use the `--overwrite` option and credential options (see the login options below). Only geographical subsets necessary to cover the point or track are downloaded.

Arguments following `--` are treated as literal strings. Use this delimiter if the output file name might otherwise be interpreted as non-strings, e.g. purely numerical file names.

Arguments
---------

- `type`: Model type (see Model types below).
- `lon`: Point longitude (degrees East).
- `lat`: Point latitutde (degrees North).
- `start`: Start time (see Time format below).
- `end`: End time (see Time format below).
- `track: <file>`, `track: { <file>... }`: One or more track NetCDF files (see Files below). If multiple files are supplied and `time_bnds` is not present in the files, they are assumed to be multiple segments of a discontinous track unless the last and first time of adjacent tracks are the same.
- `output`: Output directory.
- `login_options`: See login options below.
- `options`: See Options below.

Options
-------

- `--nocache`: Disable server-side caching of requests, when applicable.
- `--overwrite`: Overwrite existing files.
- `track_gap: <interval>`: If the interval is not 0, a track file is supplied, the `time_bnds` variable is not defined in the file and any two adjacent points are separated by more than the specified time interval (seconds), then a gap is assumed to be present between the two data points, instead of interpolating location between the two points. Default: `21600` (6 hours).

Login options
-------------

- `--overwrite`: Overwrite existing files.

MERRA-2 login options
---------------------

- `user: <value>`: Supply non-interactive user instead of prompting.
- `password: <value>`: Supply non-interactive password instead of prompting.

ERA5 login options
------------------

- `uid: <value>`: Supply non-interactive UID instead of prompting.
- `key: <value>`: Supply non-interactive API key instead of prompting.

Model types
-----------

- `era5`: ERA5.
- `merra2`: MERRA-2.

Files
-----

The track file is a NetCDF file containing 1D variables `lon`, `lat`, `time`, and optionally `time_bnds`. `time` and `time_bnds` are time in format conforming with the CF Conventions (has a valid `units` attribute and optional `calendar` attribute), `lon` is longitude between 0 and 360 degrees and `lat` is latitude between -90 and 90 degrees. If `time_bnds` is provided, discontinous track segments can be specified if adjacent time bounds are not coincident. The variables `lon`, `lat` and `time` have a single dimension `time`. The variable `time_bnds` has dimensions (`time`, `bnds`).

Time format
-----------

`YYYY-MM-DD[THH:MM[:SS]]`, where `YYYY` is year, `MM` is month, `DD` is day, `HH` is hour, `MM` is minute, `SS` is second. Example: `2000-01-01T00:00:00`.

Examples
--------

Log in to the Copernicus CDS (ERA5) service:

    alcf download era5 --login

Download ERA5 data at 45 S, 170 E between 1 and 2 January 2020 and store the output in the directory `era5`.

    alcf download era5 point: { 170.0 -45.0 } time: { 2020-01-01 2020-01-02 } era5

Log in to the NASA Earthdata (MERRA-2) service:

    alcf download merra2 --login

Download MERRA-2 data for a ship track `track.nc` and store the output in the directory `merra2`.

    alcf download merra2 track: track.nc merra2
	