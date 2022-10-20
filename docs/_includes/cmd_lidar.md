
alcf-lidar -- Process lidar data.
==========

Synopsis
--------

    alcf lidar <type> <lidar> <output> [<options>] [<algorithm_options>]

Description
-----------

The processing is done in the following order:

- noise removal
- calibration
- time resampling
- height resampling
- cloud detection
- cloud base detection

Arguments
---------

- `type`: Lidar type (see Types below).
- `lidar`: Input lidar data directory or filename.
- `output`: Output filename or directory.
- `options`: See Options below.
- `algorithm_options`: See Algorithm options below.

Types
-----

- `blview`: Vaisala BL-VIEW L2 product.
- `chm15k`: Lufft CHM 15k.
- `cl31`: Vaisala CL31.
- `cl51`: Vaisala CL51.
- `cl61`: Vaisala CL61.
- `cosp`: COSP simulated lidar.
- `default`: The same format as the output of `alcf lidar`.
- `minimpl`: Sigma Space MiniMPL.
- `mpl`: Sigma Space MPL (converted via SigmaMPL).
- `mpl2nc`: Sigma Space MPL (converted via mpl2nc).

Options
-------

- `altitude: <altitude>`: Altitude of the instrument (m). Default: Taken from lidar data or `0` if not available.
- `calibration: <algorithm>`: Backscatter calibration algorithm. Available algorithms: `default`, `none`. Default: `default`.
- `couple: <directory>`: Couple to other lidar data. Default: `none`.
- `cl_crit_range: <range>`: Critical range for the `fix_cl_range` option (m). Default: 6000.
- `cloud_detection: <algorithm>`: Cloud detection algorithm. Available algorithms: `default`, `none`. Default: `default`.
- `cloud_base_detection: <algorithm>`: Cloud base detection algorithm. Available algorithms: `default`, `none`. Default: `default`.
- `--fix_cl_range`: Fix CL31/CL51 range correction (if `noise_h2` firmware option if off). The critical range is taken from `cl_crit_range`.
- `lat: <lat>`: Latitude of the instrument (degrees North). Default: Taken from lidar data or `none` if not available.
- `lon: <lon>`: Longitude of the instrument (degrees East). Default: Taken from lidar data or `none` if not available.
- `noise_removal: <algorithm>`: Noise removal algorithm. Available algorithms: `default`, `none`.  Default: `default`.
- `output_sampling: <period>`: Output sampling period (seconds). Default: `86400` (24 hours).
- `tlim: { <low> <high> }`: Time limits (see Time format below). Default: `none`.
- `tres: <tres>`: Time resolution (seconds). Default: `300` (5 min).
- `tshift: <tshift>`: Time shift (seconds). Default: `0`.
- `zlim: { <low> <high> }`: Height limits (m). Default: `{ 0 15000 }`.
- `zres: <zres>`: Height resolution (m). Default: `50`.

Cloud detection options
-----------------------

- `default`: Cloud detection based on backscatter threshold.
- `none`: Disable cloud detection.

Cloud detection default options
-------------------------------

- `cloud_nsd: <n>`: Number of noise standard deviations to subtract. Default: `5`.
- `cloud_threshold: <threshold>`: Cloud detection threshold (sr^-1.m^-1). Default: `2e-6`.

Cloud base detection options
----------------------------

- `default`: Cloud base detection based cloud mask produced by the cloud detection algorithm.
- `none`: Disable cloud base detection.

Calibration options
-------------------

- `default`: Multiply backscatter by a calibration coefficient.
- `none`: Disable calibration.

Calibration default options
---------------------------

- `calibration_file: <file>`: Calibration file.

Noise removal options
---------------------

- `default`: Noise removal based on noise distribution on the highest level.
- `none`: Disable noise removal.

Noise removal default options
-----------------------------

- `noise_removal_sampling: <period>`: Sampling period for noise removal (seconds). Default: 300.

Time format
-----------

`YYYY-MM-DD[THH:MM[:SS]]`, where `YYYY` is year, `MM` is month, `DD` is day, `HH` is hour, `MM` is minute, `SS` is second. Example: `2000-01-01T00:00:00`.

Examples
--------

Process Vaisala CL51 data in `cl51_nc` and store the output in `cl51_alcf_lidar`, assuming instrument altitude of 100 m above sea level.

    alcf lidar cl51 cl51_nc cl51_alcf_lidar altitude: 100
	