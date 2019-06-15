Automatic Lidar and Ceilometer Framework (ALCF)
===============================================

**Development status:** beta

ALCF is an open source command line tool for processing of automatic
lidar and ceilometer (ALC) data and intercomparison with atmospheric models
such as general circulation models (GCMs), numerical weather prediction models
(NWP) and reanalyses with a lidar simulator using the
[COPS](https://github.com/CFMIP/COSPv2.0)
instrument simulator framework running offline on model output.
ALCs are vertically pointing atmospheric
lidars, measuring cloud and aerosol backscatter.
The primary focus of ALCF are atmospheric studies of cloud using ALC
observations and model cloud validation.

ALCF can read input data from multiple ceilometers and atmopsheric lidars
(such as [Vaisala CL51](https://www.vaisala.com/en/products/instruments-sensors-and-other-measurement-devices/weather-stations-and-sensors/cl51), [Lufft CHM 15k](https://www.lufft.com/products/cloud-height-snow-depth-sensors-288/ceilometer-chm-15k-nimbus-2300/), [Sigma Space MiniMPL](http://www.sigmaspace.com/blog-post/new-lidar-product-minimpl-launched-sigma-space)), convert them
to NetCDF, resample, calibrate, remove noise, detect cloud layers and cloud
base height. Atmospheric model data can be processed with the lidar simulator
to get backscatter profiles at the same location as the observations,
which can then be compared directly with the observations. The same
cloud detection algorithm is used on both observed lidar profiles and simulated
lidar profiles, so that cloud statistics such as cloud occurrence can be
compared between the model and observations.

A number of common ALCs and model formats (CMIP5, MERRA2, AMPS) are supported and
support for a new format can be added by writing a short read function in
Python or converting the ALC and model data to the CMIP5 standard.

<!--
The scientific part of ALCF is documented in the following paper:

Kuma et al. (2019): Ground-based lidar simulator framework for comparing models
and observations
-->


Installation
------------

### Requirements

ALCF is written in Python and Fortran. Installation on Linux is recommended.
Installation on other operating systems may be possible and planned in the
future, but is not detailed here at the moment.

### Installation on Linux

Install the following required software:

- [PGI compiler](https://www.pgroup.com/products/community.htm)
- Python 3 (usually pre-installed on Linux distributions)

Once you have installed PGI, make sure the command `pgf95` works in the console.

Download and unpack the [latest ALCF version](https://github.com/peterkuma/alcf/archive/master.zip),
and run commands below in the unpacked directory.

To download and build dependencies
([UDUNITS](https://www.unidata.ucar.edu/software/udunits/),
[NetCDF](https://www.unidata.ucar.edu/software/netcdf/),
[NetCDF-Fortran](https://www.unidata.ucar.edu/software/netcdf/docs-fortran/),
[OSSP uuid](http://www.ossp.org/pkg/lib/uuid/),
[HDF5](https://www.hdfgroup.org/solutions/hdf5),
[CMOR](https://pcmdi.github.io/cmor-site/),
[COSP](https://github.com/peterkuma/COSPv1)):

```sh
./download_dep
./build_dep
make
```

To install in system directories:

```sh
pip3 install https://github.com/peterkuma/ds-python/archive/master.zip https://github.com/peterkuma/aquarius-time/archive/master.zip https://github.com/peterkuma/pst/archive/master.zip
python3 setup.py install
```

To install in user directories (make sure `~/.local/bin` is in the environmental variable `PATH`):

```sh
pip3 install --user https://github.com/peterkuma/ds-python/archive/master.zip https://github.com/peterkuma/aquarius-time/archive/master.zip https://github.com/peterkuma/pst/archive/master.zip
python3 setup.py install --user
```


Usage
-----

```sh
# Convert raw lidar data to NetCDF
alcf convert <type> <input> <output>

# Convert model data to ALCF model format - single point
alcf model <type> point: { <lon> <lat> } time: { <start> <end> } <input> <output>

# Convert model data to ALCF model format - along a track
alcf model <type> track: <track> <input> <output>

# Simulate lidar
alcf simulate <type> <input> <output> [<options>]

# Process lidar data
alcf lidar <input> <output> [<options>] [<algorithm_options>]

# Calculate statistics from lidar time series
alcf stats <input> <output> [<options>]

# Plot lidar backscatter
alcf plot backscatter <input> <output> [<options>]

# Calculate statistics
alcf stats <input> <output>

# Plot statistics
alcf plot stats <input>... <output> [options]

# Peform automatic processing of model data
alcf auto model <model_type> <lidar_type> <input> <output>
    point: { <lon> <lat> } { time: <start> <end> }
    [<options>] [<model_options>] [<lidar_options>]

# Peform automatic processing of model data - along a track
alcf auto model <model_type> <lidar_type> <input> <output>
    track: <track>  [<options>] [<model_options>] [<lidar_options>]

# Perform automatic processing of lidar data
alcf auto lidar <lidar_type> <input> <output> [<options>] [<lidar_options>]

# Perform automatic comparison of model and lidar data
alcf auto compare <input>... <output> [<options>] [<compare_options>]

# TODO:

# Calculate comparison statistics from multiple lidar time series
alcf compare <input-1> <input-2> [<input-n>...] <output>
```


Commands
--------

| Command | Description |
| --- | --- |
| [convert](#convert) | Convert input instrument or model data to ALCF standard NetCDF. |
| [calibrate](#calibrate) | Calibrate ALC. (TODO) |
| [model](#model) | Extract model data at a point or along a track. |
| [simulate](#simulate) | Simulate lidar measurements from model data using COSP. |
| [lidar](#lidar) | Process lidar data. |
| [stats](#stats) | Calculate cloud occurrence statistics. |
| [plot](#plot) | Plot lidar data. |
| [compare](#compare) | TODO |
| [auto](#auto) | Peform automatic processing of model or lidar data |

The commands can be either used in a manual processing mode or automatic
processing mode (described below).

#### Manual processing

The commands are usually run in the following order.

ALC observations processing:

1. `alcf convert` – convert raw ALC data to NetCDF (only if not in NetCDF
    already),
2. `alcf lidar` – produce uncalibrated resampled data,
3. `alcf plot lidar` – plot uncalibrated backscatter profiles,
4. `alcf calibrate` (TODO) – calculate calibration coefficient based on opaque
    stratocumulus intervals identified in step 3.,
5. `alcf lidar` – produce calibrated resampled data,
6. `alcf plot lidar` – plot calibrated backscatter profiles
7. `alcf stats` – calculate summary statistics from calibrated resampled
    lidar data from step 5.
8. `alcf plot stats` – plot statistics from step 7.

Model output processing:

1. `alcf model` – extract model data at a geographical point or along a
    ship track,
2. `alcf simulate` – simulate backscatter based on data from step 1.,
3. `alcf lidar` – resample simulated backscatter data from step 2.,
4. `alcf plot lidar` – plot simulated backscatter profiles from step 3.,
5. `alcf stats` – calculate summary statistics from resampled simulated
    backscatter data from step 3.,
6. `alcf plot stats` – plot statistics from step 5.

NetCDF data files generated in each step can be previewed in
[Panoply](https://www.giss.nasa.gov/tools/panoply/).

#### Automatic processing

TODO

### convert


alcf convert - convert input instrument or model data to ALCF standard NetCDF

Usage: `alcf convert <type> <input> <output>`

- `type`: input data type (see Types below)
- `input`: input filename or dirname
- `output`: output filename or dirname

Types:

- `cl51`: Vaisala CL51

If `input` is a directory, all .DAT files in `input` are converted
to corresponding .nc files in `output`.
	

### calibrate

TODO


alcf calibrate - calibrate ALC backscatter

Supported methods:

- O'Connor et al. (2004) - calibrate based on lidar ratio (LR) of fully
opaque stratocumulus clouds.

Usage: `alcf calibrate { <start> <end> }... <input>`

- `start`: interval start (see Time format below)
- `end`: interval end (see Time format below)
- `input`: input directory (output of uncalibrated alcf lidar)

Time format:

"YYYY-MM-DD[THH:MM[:SS]]", where YYYY is year, MM is month, DD is day,
HH is hour, MM is minute, SS is second. Example: 2000-01-01T00:00:00.
	

### model


alcf model - extract model data at a point or along a track

Usage:

    alcf model <type> point: { <lon> <lat> } time: { <start> <end> } <input>
    	<output> [options]
    alcf model <type> track: <track> <input> <output>

Arguments:

- `type`: input data type (see Types below)
- `input`: input directory
- `output`: output directory
- `lon`: point longitude
- `lat`: point latitutde
- `start`: start time (see Time format below)
- `end`: end time (see Time format below)
- `track`: track NetCDF file (see Track below)
- `options`: see Options below

Options:

- `track_override_year`: Override year in track. Use if comparing observations
    with a model statistically. Default: none.
- `track_lon_180`: Expect track longitude between -180 and 180 degrees.
    Default: false.

Types:

- `amps`: Antarctic Mesoscale Prediction System (AMPS)
- `merra2`: Modern-Era Retrospective Analysis for Research and Applications,
	Version 2 (MERRA-2)
- `nzcsm`: New Zealand Convection Scale Model (NZCSM)
- `nzesm`: New Zealand Earth System Model (NZESM) (experimental)

Time format:

"YYYY-MM-DD[THH:MM[:SS]]", where YYYY is year, MM is month, DD is day,
HH is hour, MM is minute, SS is second. Example: 2000-01-01T00:00:00.

Track:

Track file is a NetCDF file containing 1D variables `lon`, `lat`, and `time`.
`time` is time in format conforming with the NetCDF standard,
`lon` is longitude between 0 and 360 degrees and `lat` is latitude between
-90 and 90 degrees.
	

### simulate


alcf simulate - simulate lidar measurements from model data using COSP

Usage: `alcf simulate <type> <input> <output> [<options>]`

Arguments:

- `type`: type of lidar to simulate
- `input`: input filename or directory (the output of "alcf model")
- `output`: output filename or directory
- `options`: see Options below

Types:

- `chm15k`: Lufft CHM 15k
- `cl51`: Vaisala CL51
- `mpl`: Sigma Space MiniMPL

Options:

- `ncolumns`: Number of SCOPS subcolumns to generate. Default: `10`.
- `overlap`: Cloud overlap assumption in the SCOPS subcolumn generator.
  `maximum` for maximum overlap, `random` for random overlap, or
  `maximum-random` for maximum-random overlap. Default: `maximum-random`.
	

### lidar


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
	

### stats


alcf stats - calculate cloud occurrence statistics

Usage: `alcf stats <input> <output> [<options>]`

Arguments:

- `input`: input filename or directory
- `output`: output filename or directory

Options:

- `blim`: backscatter histogram limits (1e-6 m-1.sr-1). Default: `{ 5 200 }`.
- `bres`: backscatter histogram resolution (1e-6 m-1.sr-1). Default: `10`.
- `filter`: filter profiles by condition: `cloudy` for cloudy profiles only,
    `clear` for clear sky profiles only, `none` for all profiles.
    Default: `none`.
- `tlim`: Time limits `{<start> <end> }` (see Time format below).
    Default: `none`.
- `zlim`: `{ <low> <high> }`: Height limits (m). Default: `{ 0 15000 }`.
- `zres`: Height resolution (m). Default: `50`.
- `bsd_lim`: backscatter standard deviation histogram limits (1e-6 m-1.sr-1).
    Default: `{0 10}`.
- `bsd_log`: enable/disable logarithmic scale of the backscatter standard
    deviation histogram (`true` or `false`). Default: `true`.
- `bsd_res`: backscatter standard deviation histogram resolution
    (1e-6 m-1.sr-1). Default: `0.1`.
- `bsd_z`: backscatter standard deviation histogram height (m). Default: `8000`.

Time format:

"YYYY-MM-DD[THH:MM[:SS]]", where YYYY is year, MM is month, DD is day,
HH is hour, MM is minute, SS is second. Example: 2000-01-01T00:00:00.
	

### plot


alcf plot - plot lidar data

Usage: `alcf plot <plot_type> <input> <output> [<options>] [<plot_options>]`

Arguments:

- `plot_type`: plot type (see Plot types below)
- `input`: input filename or directory
- `output`: output filename or directory
- `options`: see Options below
- `plot_options`: Plot type specific options. See Plot options below.

Plot types:

- `backscatter`: plot backscatter
- `backscatter_hist`: plot backscatter histogram
- `backscatter_sd_hist`: plot backscatter standard deviation histogram
- `cloud_occurrence`: plot cloud occurrence

Options:

- `dpi`: Resolution in dots per inch (DPI). Default: `300`.
- `grid`: Plot grid (`true` or `false`). Default: `false`.
- `height`: Plot height (inches).
    Default: `5` if `plot_type` is `cloud_occurrence` or `backscatter_hist`
    else `4`.
- `subcolumn`: Model subcolumn to plot. Default: `0`.
- `title`: Plot title.
- `width`: Plot width (inches).
    Default: `5` if `plot_type` is `cloud_occurrence` or `backscatter_hist`
    else `10`.

Plot options:

- `backscatter`:
	- `lr`: Plot lidar ratio (LR), Default: `false`.
	- `plot_cloud_mask`: Plot cloud mask. Default: `false`.
	- `sigma`: Suppress backscatter less than a number of standard deviations
		from the mean backscatter (real). Default: `3`.
	- `vlim`: `{ <min> <max }`. Value limits (10^6 m-1.sr-1).
        Default: `{ 5 200 }`.
- `backscatter_hist`:
    - `vlim`: `{ <min> <max }`. Value limits (%) or `none` for auto. If `none`
        and `vlog` is `none`, `min` is set to 1e-3 if less or equal to zero.
        Default: `none`.
    - `vlog`: use logarithmic scale for values. Default: `false`.
    - `xlim`: `{ <min> <max> }`. x axis limits (10^6 m-1.sr-1) or non for auto.
        Default: `none`.
    - `zlim`: `{ <min> <max> }`. y axis limits (m) or none for auto.
        Default: `none`.
- `cloud_occurrence`:
    - `colors`: Line colors. Default: `{ #0084c8 #dc0000 #009100 #ffc022 #ba00ff }`
    - `labels`: Line labels. Default: `none`.
    - `lw`: Line width. Default: `1`.
    - `xlim`: x axis limits `{ <min> <max> }` (%). Default: `{ 0 100 }`.
    - `zlim`: y axis limits `{ <min> <max> }` (m). Default: `{ 0 15 }`.
	

### compare

TODO

### auto


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
	

Supported models
----------------

The following GCM, NWP models and reanalyses are supported:

- [AMPS](http://www2.mmm.ucar.edu/rt/amps/)
- [MERRA2](https://duckduckgo.com/?q=merra-2&t=ffab&ia=web)
- [NZCSM](https://www.nesi.org.nz/case-studies/improving-new-zealands-weather-forecasting-ability)

TODO:

- CMIP5
- JRA-55

Supported ALCs
--------------

The following ALCs are supported:

- Vaisala CL31, CL51
- Lufft CHM 15k
- Sigma Space MiniMPL

Calibration
-----------

Depending on the instrument, calibration in ALCF may be an essential part of
processing ALC data. Ceilometers often report backscatter values in
"arbitrary units" which need to be converted to m^-1.sr^-1 for a reliable
comparison with the COSP simulator. The recommended calibration method of
calibration in ALCF is [O'Connor et al. (2004)](https://journals.ametsoc.org/doi/abs/10.1175/1520-0426(2004)021%3C0777%3AATFAOC%3E2.0.CO%3B2) for its universality.
The method is based on the fact that the lidar ratio of fully opaque
stratocumulus scenes tends to a constant.

1. Plot daily uncalibrated ALC data by:

        alcf lidar <type> <raw-dir> <lidar-dir>
        alcf plot lidar --lr <lidar-dir> <plot-dir>

2. Identify visually sections of the plots which contain fully attenuating
stratocumulus clouds, and note their time intervals.

TODO:

3. Supply the time intervals to alcf calibrate:

        alcf calibrate { <start> <end> }...

    where `<start>` and `<end>` are the start time and end time of each interval
    in the ISO format (`<year>-<month>-<day>T<hour>:<minute>`). The command
    will output the calibration coefficient to be used with the `alcf lidar`
    command:

        alcf lidar <type> --calibration_coeff: <coeff> <input> <output>

    where `<coeff>` is the calibration coefficient.

ALCF output
-----------

The ALCF output is stored in NetCDF files. Below is description of variables
contained in the data files.

### model

`alcf model` output is a 2-dimensional "curtain" of model data at a given location
over a length of time or along a ship track.

Variable | Description | Dimensions | Units
--- | --- | --- | ---
cli | mass fraction of cloud ice in air | time, level | 1
clt | cloud area fraction | time, level | %
clw | mass fraction of cloud liquid water in air | time, level | 1
lat | latitude | time | degrees north
lon | longitude | time | degrees east
orog | surface altitude | time | m
pfull | air pressure | time, level | Pa
ps | surface air pressure | time | Pa
ta | air temperature | time, level | K
time | time | time | days since -4712-01-01 12:00
zg | geopotential height | time, level | m

### cosp

`alcf simulate` output is a 2-dimensional "curtain" of simulated backscatter
at a given location over a length of time or along a ship track.

Variable | Description | Dimensions | Units
--- | --- | --- | ---
backscatter | total attenuated backscatter coefficient | time, level, column | m<sup>-1</sup>.sr<sup>-1</sup>
backscatter_mol | total attenuated molecular backscatter coefficient | time, level | m<sup>-1</sup>.sr<sup>-1</sup>
lat | latitude | time | degrees north
lon | longitude | time | degrees east
pfull | air pressure | time, level | Pa
time | time | time | days since -4712-01-01 12:00
zfull | height above reference ellipsoid | time, level | m

### lidar

`alcf lidar` output  is a 2-dimensional "curtain" of observed or simulated
backscatter at a given location over a length of time or along a ship track.

Variable | Description | Dimensions | Units
--- | --- | --- | ---
backscatter | total attenuated backscatter coefficient | time, range | m<sup>-1</sup>.sr<sup>-1</sup>
backscatter_sd | total attenuated backscatter coefficient standard deviation | time, range | m<sup>-1</sup>.sr<sup>-1</sup>
cbh | cloud base height | time | m
cloud_mask | cloud mask | time, range | 1
lr | lidar ratio | time | sr
time | time | time | days since -4712-01-01 12:00
zfull | height above reference ellipsoid | time, level | m

### stats

`alcf stats` output contains histograms and summary statistics calculated
from a 2-dimensional "curtain" of observed or simulated backscatter.

Variable | Description | Dimensions | Units
--- | --- | --- | ---
backscatter_avg | total attenuated backscatter coefficient average | zfull | m<sup>-1</sup>.sr<sup>-1</sup>
backscatter_full | total attenuated backscatter coefficient | backscatter_full | m<sup>-1</sup>.sr<sup>-1</sup>
backscatter_hist | backscatter histogram | backscatter_full, zfull | %
backscatter_mol_avg | total attenuated molecular backscatter coefficient average | zfull | m<sup>-1</sup>.sr<sup>-1</sup>
backscatter_sd_full | total attenuated backscatter coefficient standard deviation | backscatter_sd_full | m<sup>-1</sup>.sr<sup>-1</sup>
backscatter_sd_hist | total attenuated backscatter coefficient standard deviation histogram | backscatter_sd_full | %
backscatter_sd_z | total attenuated backscatter coefficient standard deviation height above reference ellipsoid | m
cloud_occurrence | cloud occurrence | zfull | %
n | number of profiles | | 1
zfull | height above reference ellipsoid | zfull | m

Model guide
-----------

Below is a description of the model output supported by ALCF. You might
have to modify the code for reading the model output depending on the
exact format of the model output, such as variable names and how they are
split among the output files.

### AMPS

**Source:** `alcf/models/amps.py`

ALCF is compatible with the NetCDF AMPS output. You can find the
[AMPS archive](https://www.earthsystemgrid.org/project/amps.html) on the
Earth System Grid (ESG) website. The following files conver 24 hours of model
output:

    wrfout_dxx_YYYYmmdd00_f003.nc
    wrfout_dxx_YYYYmmdd00_f006.nc
    wrfout_dxx_YYYYmmdd00_f009.nc
    wrfout_dxx_YYYYmmdd00_f012.nc
    wrfout_dxx_YYYYmmdd12_f003.nc
    wrfout_dxx_YYYYmmdd12_f006.nc
    wrfout_dxx_YYYYmmdd12_f009.nc
    wrfout_dxx_YYYYmmdd12_f012.nc

where xx is the [AMPS grid](http://www2.mmm.ucar.edu/rt/amps/information/configuration/maps_2017101012/maps.html), YYYYmmdd is the year (YYYY), month (mm) and day (dd). The "*_f000.nc"
files are not suitable for use with ALCF as they do not contain all required
variables.

### MERRA-2

**Source:** `alcf/models/merra2.py`

MERRA-2 reanalysis files can be found via the
[NASA EarthData](https://earthdata.nasa.gov/) portal.
Description of the MERRA-2 products can be found in the [MERRA-2: File Specification](https://gmao.gsfc.nasa.gov/pubs/docs/Bosilovich785.pdf) document. The model-level products are recommended due to
their higher resolution. Only the "Assimilated Meteorological Fields" contain
the required variables. The recommended product is the
"inst3_3d_asm_Nv (M2I3NVASM): Assimilated Meteorological Fields", i.e.
the 3-hourly instantaneous 3D assimilated fields on model levels. You can
find the product files by searching for "M2I3NVASM" on NASA EarthData,
or directly on the [NASA EOSDIS FTP server](https://goldsmr5.gesdisc.eosdis.nasa.gov/data/MERRA2/M2I3NVASM.5.12.4/).

### NZCSM

**Source:** `alcf/models/nzcsm.py`

New Zealand Convective Scale Model (NZCSM) is a NWP model based on the
UK Met Office Unified Model. The following model output variables are needed
to run the lidar simulator:

- hybridt32
- latitude
- longitude
- model_press,
- model_qcf
- model_qcl
- theta_lev_temp
- time0

### CMIP5

TODO

**Source:** `alcf/models/cmip5.py`

CMIP5 model output can be downloaded from the [CMIP5 Earth System Grid (ESG) archive](https://esgf-node.llnl.gov/search/cmip5/). ALCF requires the following CMIP5 variables:

- clc
- clic
- clis
- cls
- clwc
- clws
- pfull
- ps
- ta
- zfull
- zhalf

### JRA-55

TODO

### NZESM (experimental)

**Source:** `alcf/models/nzesm.py`

New Zealand Earth System Model output is a model based on HadGEM3. The
model output variables needed are:

- air_pressure
- air_temperature
- cloud_volume_fraction_in_atmosphere_layer
- latitude
- level_height
- longitude
- mass_fraction_of_cloud_ice_in_air
- mass_fraction_of_cloud_liquid_water_in_air
- time

License
-------

This software is available under the terms of the MIT license
(see [LICENSE.md](LICENSE.md)).

See also
--------

[ccplot](https://ccplot.org),
[cl2nc](https://github.com/peterkuma/cl2nc),
[mpl2nc](https://github.com/peterkuma/mpl2nc)
