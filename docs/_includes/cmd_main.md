alcf -- Tool for processing of automatic lidar and ceilometer (ALC) data and intercomparison with atmospheric models.
====

Synopsis
--------

    alcf <cmd> [<options>]
    alcf <cmd> --help

Arguments
---------

- `cmd`: See Commands below.
- `options`: Command options.

Commands
--------

- `auto`: Peform automatic processing of model or lidar data.
- `calibrate`: Calibrate lidar backscatter.
- `convert`: Convert input instrument or model data to the ALCF standard NetCDF.
- `lidar`: Process lidar data.
- `model`: Extract model data at a point or along a track.
- `plot`: Plot lidar data.
- `simulate`: Simulate lidar measurements from model data using COSP.
- `stats`: Calculate cloud occurrence statistics.

Options
-------

- `--help`: Print help for command.
- `--debug`: Enable debugging information.
