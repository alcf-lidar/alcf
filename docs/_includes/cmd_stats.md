
alcf-stats -- Calculate cloud occurrence statistics.
==========

Synopsis
--------

    alcf stats <input> <output> [<options>]

Arguments
---------

- `input`: Input filename or directory.
- `output`: Output filename or directory.

Options
-------

- `blim: <value>`: Backscatter histogram limits (1e-6 m-1.sr-1). Default: `{ 5 200 }`.
- `bres: <value>`: Backscatter histogram resolution (1e-6 m-1.sr-1). Default: `10`.
- `bsd_lim: { <low> <high> }`: Backscatter standard deviation histogram limits (1e-6 m-1.sr-1). Default: `{ 0.001 10 }`.
- `bsd_log: <value>`: Enable/disable logarithmic scale of the backscatter standard deviation histogram (`true` or `false`). Default: `true`.
- `bsd_res: <value>`: Backscatter standard deviation histogram resolution (1e-6 m-1.sr-1). Default: `0.001`.
- `bsd_z: <value>`: Backscatter standard deviation histogram height (m). Default: `8000`.
- `filter: <value> | { <value> ... }`: Filter profiles by condition: `cloudy` for cloudy profiles only, `clear` for clear sky profiles only, `night` for nighttime profiles, `day` for daytime profiles, `none` for all profiles. If an array of values is supplied, all conditions must be true. For `night` and `day`, lidar profiles must contain valid longitude and latitude fields set via the `lon` and `lat` arguments of `alcf lidar` or read implicitly from raw lidar data files if available (mpl, mpl2nc). Default: `none`.
- `tlim: { <start> <end> }`: Time limits (see Time format below). Default: `none`.
- `zlim: { <low> <high> }`: Height limits (m). Default: `{ 0 15000 }`.
- `zres: <value>`: Height resolution (m). Default: `50`.

Time format
-----------

`YYYY-MM-DD[THH:MM[:SS]]`, where `YYYY` is year, `MM` is month, `DD` is day, `HH` is hour, `MM` is minute, `SS` is second. Example: `2000-01-01T00:00:00`.

Examples
--------

Calculate statistics from processed lidar data in `alcf_cl51_lidar` and store the output in `alcf_cl51_stats.nc`.

    alcf stats alcf_cl51_lidar alcf_cl51_stats.nc
	