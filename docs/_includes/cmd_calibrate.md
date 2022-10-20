
alcf-calibrate -- Calibrate ALC backscatter.
==============

Synopsis
--------

    alcf calibrate <type> <time_periods> <input> <output>

Description
-----------

Calibration based the O'Connor et al. (2004) method of lidar ratio (LR) in fully opaque stratocumulus clouds.

Arguments
---------

- `type`: Lidar type (see Types below).
- `time_periods`: File containing calibration time periods of stratocumulus clouds in the backscatter profiles (see Time periods below).
- `input`: Input directory containing NetCDF files (the output of `alcf lidar`).
- `output`: Output calibration file.

Types
-----

- `chm15k`: Lufft CHM 15k.
- `cl31`: Vaisala CL31.
- `cl51`: Vaisala CL51.
- `minimpl`: Sigma Space MiniMPL.
- `mpl`: Sigma Space MPL.

Files
-----

Time periods file is a text file containting start and end time (see Time format below) of a time period separated by whitespace, one time period per line:

```
<start> <end>
<start> <end>
...
```

where `start` is the start time and `end` is the end time.

Time format
-----------

`YYYY-MM-DD[THH:MM[:SS]]`, where `YYYY` is year, `MM` is month, `DD` is day, `HH` is hour, `MM` is minute, `SS` is second. Example: `2000-01-01T00:00:00`.

Examples
--------

Read time periods from `time_periods.txt`, lidar profiles from the directory `lidar` and write the calibration coefficient to `calibration.txt`.

    alcf calibrate time_periods.txt lidar calibration.txt
	