import sys
import os
from alcf.cmds.auto_cmds import CMDS

def run(cmd, *args, **kwargs):
	"""
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
- `era5`: ERA5
- `jra55`: JRA-55
- `merra2`: Modern-Era Retrospective Analysis for Research and Applications,
	Version 2 (MERRA-2)
- `nzcsm`: New Zealand Convection Scale Model (NZCSM)
- `nzesm`: New Zealand Earth System Model (NZESM) (experimental)
- `um`: UK Met Office Unified Model (UM)

Lidar types:

- `blview`: Vaisala BL-VIEW L2 product
- `caliop`: CALIPSO/CALIOP (`alcf auto model` only)
- `chm15k`: Lufft CHM 15k
- `cl31`: Vaisala CL31
- `cl51`: Vaisala CL51
- `cl61`: Vaisala CL61
- `cosp`: COSP simulated lidar
- `minimpl`: Sigma Space MiniMPL
- `mpl`: Sigma Space MPL (converted via SigmaMPL)
- `mpl2nc`: Sigma Space MPL (converted via mpl2nc)

Time format:

"YYYY-MM-DD[THH:MM[:SS]]", where YYYY is year, MM is month, DD is day,
HH is hour, MM is minute, SS is second. Example: 2000-01-01T00:00:00.

Examples:

Simulate a Vaisala CL51 instrument from MERRA-2 data in `M2I3NVASM.5.12.4`
at 45 S, 170 E between 1 and 2 January 2020 and store the output in
`alcf_merra2`.

    alcf auto model merra2 cl51 M2I3NVASM.5.12.4 alcf_merra2 \\
    point: { -45.0 170.0 } time: { 2020-01-01 2020-01-02 }

Process Lufft CHM 15k data in `chm15k` and store the output in `alcf_chm15k`.

    alcf auto lidar chm15k chm15k_data alcf_chm15k
	"""
	if cmd is None:
		sys.stderr.write(main.__doc__.strip() + '\n')
		return 1

	func = CMDS.get(cmd)
	if func is None:
		raise ValueError('Invalid command: %s' % cmd)
	func(*args, **kwargs)
