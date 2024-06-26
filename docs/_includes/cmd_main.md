alcf -- Tool for processing of automatic lidar and ceilometer (ALC) data and intercomparison with atmospheric models.
====

Synopsis
--------

    alcf <cmd> [<options>] [<arguments>]
    alcf [<cmd>] --help
    alcf --version

Arguments
---------

- `cmd`: See Commands below.
- `arguments`: Command arguments. Use `alcf <cmd> --help` for more information.
- `options`: Command options (see Options below).

Commands
--------

- `auto`: Peform automatic processing of model or lidar data.
- `calibrate`: Calibrate lidar backscatter.
- `convert`: Convert input instrument or model data to the ALCF standard NetCDF.
- `download`: Download model data.
- `lidar`: Process lidar data.
- `model`: Extract model data at a point or along a track.
- `plot`: Plot lidar data.
- `simulate`: Simulate lidar measurements from model data using COSP.
- `stats`: Calculate cloud occurrence statistics.

Options
-------

- `--debug`: Enable debugging information.
- `--help`: Print general help or help for a command and exit.
- `--version`: Print version and exit.
