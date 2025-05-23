
alcf-auto -- Peform automatic processing of model or lidar data.
=========

Synopsis
--------

    alcf auto model <model_type> <lidar_type> point: { <lon> <lat> } time: { <start> <end> } [<options>] [<model_options>] [<lidar_options>] [--] <input> <output>

    alcf auto model <model_type> <lidar_type> track: <track> [<options>] [<model_options>] [<lidar_options>] [--] <input> <output>

    alcf auto lidar <lidar_type> [<options>] [<lidar_options>] [--] <input> <output>

Description
-----------

`alcf auto model` is equivalent to the sequence of commands:

    alcf model
    alcf simulate
    alcf lidar
    alcf stats
    alcf stats (fine-scale)
    alcf stats (clear-sky fine-scale)
    alcf plot backscatter
    alcf plot backscatter_hist
    alcf plot backscatter_hist (fine-scale)
    alcf plot backscatter_hist (clear-sky fine-scale)
    alcf plot cloud_occurrence
    alcf plot cbh

`alcf auto lidar` is equivalent to the sequence of commands:

    alcf lidar
    alcf stats
    alcf stats (fine-scale)
    alcf stats (clear-sky fine-scale)
    alcf plot backscatter
    alcf plot backscatter_hist
    alcf plot backscatter_hist (fine-scale)
    alcf plot backscatter_hist (clear-sky fine-scale)
    alcf plot cloud_occurrence
    alcf plot cbh

Arguments following `--` are treated as literal strings. Use this delimiter if the input or output file names might otherwise be interpreted as non-strings, e.g. purely numerical file names.

Arguments
---------

- `end`: End time (see Time format below).
- `input`: Input directory containing model or lidar data, or, in case of `alcf auto compare`, the output of `alcf auto model` or `alcf auto lidar`.
- `lat`: Point latitutde.
- `lidar_options`: See `alcf lidar` options.
- `lidar_type`: Lidar type (see Lidar types below).
- `lon`: Point longitude.
- `model_options`: See `alcf model` options.
- `model_type`: Model type (see Model types below).
- `options`: See Options below.
- `plot_options`: See `alcf plot` options.
- `start`: Start time (see Time format below).
- `track`: Track NetCDF file (see Track below).

Options
-------

- `skip: <step>`: Skip all processing steps before `<step>`. `<step>` is one of: `model`, `simulate`, `lidar`, `stats`, `plot`. Default: `none`.

Model types
-----------

- `amps`: Antarctic Mesoscale Prediction System (AMPS).
- `era5`: ERA5.
- `icon`: ICON.
- `icon_intake_healpix`: ICON through Intake-ESM on HEALPix grid.
- `jra55`: JRA-55.
- `merra2`: Modern-Era Retrospective Analysis for Research and Applications, Version 2 (MERRA-2).
- `nzcsm`: New Zealand Convection Scale Model (NZCSM).
- `nzesm`: New Zealand Earth System Model (NZESM) (experimental).
- `um`: UK Met Office Unified Model (UM).

Lidar types
-----------

- `blview`: Vaisala BL-VIEW L2 product.
- `caliop`: CALIPSO/CALIOP (`alcf auto model` only).
- `chm15k`: Lufft CHM 15k.
- `ct25k`: Vaisala CT25K. IMPORTANT: The simulator currently assumes wavelength of 910 nm instead of the actual instrument wavelength of 905 nm.
- `cl31`: Vaisala CL31.
- `cl51`: Vaisala CL51.
- `cl61`: Vaisala CL61.
- `cn_chm15k`: Cloudnet Lufft CHM 15k.
- `cn_ct25k`: Cloudnet Vaisala CT25K.
- `cn_cl31`: Cloudnet Vaisala CL31.
- `cn_cl51`: Cloudnet Vaisala CL51.
- `cn_cl61`: Cloudnet Vaisala CL61.
- `cn_minimpl`: Cloudnet Sigma Space MiniMPL.
- `cosp`: COSP simulated lidar.
- `default`: The same format as the output of `alcf lidar`.
- `minimpl`: Sigma Space MiniMPL (converted via SigmaMPL).
- `mpl`: Sigma Space MPL (converted via SigmaMPL).
- `mpl2nc`: Sigma Space MPL and MiniMPL (converted via mpl2nc).

Time format
-----------

`YYYY-MM-DD[THH:MM[:SS]]`, where `YYYY` is year, `MM` is month, `DD` is day,
`HH` is hour, `MM` is minute, `SS` is second. Example: 2000-01-01T00:00:00.

Examples
--------

Simulate a Vaisala CL51 instrument from MERRA-2 data in `M2I3NVASM.5.12.4`
at 45 S, 170 E between 1 and 2 January 2020 and store the output in
`alcf_merra2`.

    alcf auto model merra2 cl51 point: { -45.0 170.0 } time: { 2020-01-01 2020-01-02 } M2I3NVASM.5.12.4 alcf_merra2

Process Lufft CHM 15k data in `chm15k` and store the output in `alcf_chm15k`.

    alcf auto lidar chm15k chm15k_data alcf_chm15k
	