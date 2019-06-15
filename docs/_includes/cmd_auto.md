
alcf auto - peform automatic processing of model or lidar data

`alcf auto model` is equivalent to:

1. `alcf model`
2. `alcf simulate`
3. `alcf lidar`
4. `alcf stats`
5. `alcf plot backscatter`
6. `alcf plot backscatter_hist`
7. `alcf plot cloud_occurrence`

`alcf auto lidar` is equivalent to:

1. `alcf lidar`
2. `alcf stats`
3. `alcf plot backscatter`
4. `alcf plot backscatter_hist`
5. `alcf plot cloud_occurrence`

`alcf auto compare` is equivalent to:

1. `alcf plot cloud_occurrence`

Usage:

    alcf auto model <model_type> <lidar_type> <input> <output>
        point: { <lon> <lat> } time: { <start> <end> }
        [<options>] [<model_options>] [<lidar_options>]
    alcf auto model <model_type> <lidar_type> <input> <output>
        track: <track> [<options>] [<model_options>] [<lidar_options>]
    alcf auto lidar <lidar_type> <input> <output> [<options>] [<lidar_options>]
    alcf auto compare <input>... <output> [<options>] [<plot_options>]

Arguments:

- `end`: end time (see Time format below)
- `input`: input directory containing model or lidar data, or,
    in case of `alcf auto compare`, the output of `alcf auto model` or
    `alcf auto lidar`
- `lat`: point latitutde
- `lidar_options`: see `alcf lidar` options
- `lidar_type`: lidar type (see Lidar types below)
- `lon`: point longitude
- `model_options`: see `alcf model` options
- `model_type`: model type (see Model types below)
- `options`: see Options below
- `plot_options`: see `alcf plot` options
- `start`: start time (see Time format below)
- `track`: track NetCDF file (see Track below)

Options:

- `skip: <step>`: Skip all processing steps before `step`.
    `step` is one of: `model`, `simulate`, `lidar`, `stats`, `plot`.
    Default: `none`.

Model types:

- `amps`: Antarctic Mesoscale Prediction System (AMPS)
- `merra2`: Modern-Era Retrospective Analysis for Research and Applications,
	Version 2 (MERRA-2)
- `nzcsm`: New Zealand Convection Scale Model (NZCSM)
- `nzesm`: New Zealand Earth System Model (NZESM) (experimental)

Lidar types:

- `chm15k`: Lufft CHM 15k
- `cl31`: Vaisala CL31
- `cl51`: Vaisala CL51
- `cosp`: COSP simulated lidar
- `minimpl`: Sigma Space MiniMPL
- `mpl`: Sigma Space MPL
	