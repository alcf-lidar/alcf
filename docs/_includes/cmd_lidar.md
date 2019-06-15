
alcf lidar - process lidar data

The processing is done in the following order:

- noise removal
- calibration
- time resampling
- height resampling
- cloud detection
- cloud base detection

Usage: `alcf lidar <type> <lidar> <output> [<options>] [<algorithm_options>]`

Arguments:

- `type`: lidar type (see Types below)
- `lidar`: input lidar data directory or filename
- `output`: output filename or directory
- `options`: see Options below
- `algorithm_options`: see Algorithm options below

Types:

- `chm15k`: Lufft CHM 15k
- `cl31`: Vaisala CL31
- `cl51`: Vaisala CL51
- `cosp`: COSP simulated lidar
- `minimpl`: Sigma Space MiniMPL
- `mpl`: Sigma Space MPL

Options:

- `calibration`: Backscatter calibration algorithm.
    Available algorithms: `default`, `none`. Default: `default`.
- `cloud_detection`: Cloud detection algorithm.
    Available algorithms: `default`, `none`. Default: `default`.
- `cloud_base_detection`: Cloud base detection algorithm.
    Available algorithms: `default`, `none`. Default: `default`.
- `eta`: Multiple-scattering factor to assume in lidar ratio calculation.
    Default: `0.7`.
- `noise_removal`: Noise removal algorithm.
    Available algorithms: `default`, `none`.  Default: `default`.
- `output_sampling`: Output sampling period (seconds).
    Default: `86400` (24 hours).
- `tlim`: `{ <low> <high> }`: Time limits (see Time format below).
    Default: `none`.
- `tres`: Time resolution (seconds). Default: `300` (5 min).
- `zlim`: `{ <low> <high> }`: Height limits (m). Default: `{ 0 15000 }`.
- `zres`: Height resolution (m). Default: `50`.

Algorithm options:

- Cloud detection:
    - `default`: cloud detection based on backscatter threshold
        - `cloud_nsd`: Number of noise standard deviations to subtract.
        	Default: `3`.
        - `cloud_threshold`: Cloud detection threshold (sr^-1.m^-1).
            Default: `10e-6`.
	- `none`: disable cloud detection

- Cloud base detection:
	- `default`: cloud base detection based cloud mask produced by the cloud
		detection algorithm
	- `none`: disable cloud base detection

- Calibration:
    - `default`: multiply backscatter by calibration coefficient
        - `calibration_coeff`: Calibration coefficient. Default: ?.
	- `none`: disable calibration

- Noise removal:
    - `default`:
        - `noise_removal_sampling`: Sampling period for noise removal (seconds).
        	Default: 300.
    - `none`: disable noise removal
	