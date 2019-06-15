
alcf - Tool for processing of automatic lidar and ceilometer (ALC) data
and intercomparison with atmospheric models.

Usage:

    alcf <cmd> [<options>]
    alcf <cmd> --help

Arguments:

- `cmd`: command (see below)
- `options`: command options

Options:

`--help`: print help for command

Commands:

- `convert`: convert input instrument or model data to ALCF standard NetCDF
- `model`: extract model data at a point or along a track
- `cosp`: simulate lidar measurements from model data using COSP
- `lidar`: process lidar data
- `stats`: calculate cloud occurrence statistics
- `plot`: plot lidar data
- `plot_stats`: plot lidar statistics
	