
alcf-stats -- Calculate cloud occurrence statistics.
==========

Synopsis
--------

    alcf stats [<options>] [--] <input> <output>

Description
-----------

Arguments following `--` are treated as literal strings. Use this delimiter if the input or output file names might otherwise be interpreted as non-strings, e.g. purely numerical file names.

Arguments
---------

- `input`: Input filename or directory.
- `output`: Output filename or directory.

Options
-------

- `blim: <value>`: Backscatter histogram limits (10^-6 m-1.sr-1). Default: `{ 5 200 }`.
- `bres: <value>`: Backscatter histogram resolution (10^-6 m-1.sr-1). Default: `10`.
- `bsd_lim: { <low> <high> }`: Backscatter standard deviation histogram limits (10^-6 m-1.sr-1). Default: `{ 0.001 10 }`.
- `bsd_log: <value>`: Enable/disable logarithmic scale of the backscatter standard deviation histogram (`true` or `false`). Default: `true`.
- `bsd_res: <value>`: Backscatter standard deviation histogram resolution (10^-6 m-1.sr-1). Default: `0.001`.
- `bsd_z: <value>`: Backscatter standard deviation histogram height (m). Default: `8000`.
- `filter: <value> | { <value> ... }`: Filter profiles by condition: `cloudy` for cloudy profiles only, `clear` for clear sky profiles only, `night` for nighttime profiles, `day` for daytime profiles, `none` for all profiles. If an array of values is supplied, all conditions must be true. For `night` and `day`, lidar profiles must contain valid longitude and latitude fields set via the `lon` and `lat` arguments of `alcf lidar` or read implicitly from raw lidar data files if available (mpl, mpl2nc). Default: `none`.
- `filter_exclude: <value> | { <value>... }`: Filter by a mask defined in a NetCDF file, described below under Filter file. If multiple files are supplied, they must all apply for a profile to be excluded.
- `filter_include: <value> | { <value>... }`: The same as `filter_exclude`, but with time intervals to be included in the result. If both are defined, `filter_include` takes precedence. If multiple files are supplied, they must all apply for a profile to be included.
- `interp: <value>`: Vertical interpolation method. `area_block` for area-weighting with block interpolation, `area_linear` for area-weighting with linear interpolation or `linear` for simple linear interpolation. Default: `area_block`.
- `tlim: { <start> <end> }`: Time limits (see Time format below). Default: `none`.
- `zlim: { <low> <high> }`: Height limits (m). Default: `{ 0 15000 }`.
- `zres: <value>`: Height resolution (m). Default: `50`.

Time format
-----------

`YYYY-MM-DD[THH:MM[:SS]]`, where `YYYY` is year, `MM` is month, `DD` is day, `HH` is hour, `MM` is minute, `SS` is second. Example: `2000-01-01T00:00:00`.

Filter file
----------

The NetCDF file must define a variable `time_bnds` (float64), which are time intervals to be excluded from or included in the result. `time_bnds` must have two dimensions `time` of an arbitrary size and `bnds` of size 2. The first and second column of the variable should contain the start and end of the interval, respectively. `time_bnds` must be valid time in accordance with the CF Conventions.

Examples
--------

Calculate statistics from processed lidar data in `alcf_cl51_lidar` and store the output in `alcf_cl51_stats.nc`.

    alcf stats alcf_cl51_lidar alcf_cl51_stats.nc
	