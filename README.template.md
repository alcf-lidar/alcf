Automatic Lidar and Ceilometer Framework (ALCF)
===============================================

**Development status:** in development

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
Installation on other operating systems may be possible, but is not detailed
here at the moment.

### Installation on Linux

Install the following required software:

- [PGI compiler](https://www.pgroup.com/products/community.htm)
- Python 2.7 (usually pre-installed on all Linux distributions)

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
pip install https://github.com/peterkuma/ds-python/archive/master.zip https://github.com/peterkuma/aquarius-time/archive/master.zip https://github.com/peterkuma/pst/archive/master.zip
python setup.py install
```

To install in user directories (make sure `~/.local/bin` is in the environmental variable `PATH`):

```sh
pip install --user https://github.com/peterkuma/ds-python/archive/master.zip https://github.com/peterkuma/aquarius-time/archive/master.zip https://github.com/peterkuma/pst/archive/master.zip
python setup.py install --user
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

# TODO:

# Plot lidar mask
alcf plot mask <input> <output> [<options>]

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

### convert

{{{cmd_convert}}}

### calibrate

TODO

{{{cmd_calibrate}}}

### model

{{{cmd_model}}}

### simulate

{{{cmd_simulate}}}

### lidar

{{{cmd_lidar}}}

### stats

{{{cmd_stats}}}

### plot

{{{cmd_plot}}}

### compare

TODO

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

Model guide
-----------

### AMPS

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

New Zealand Convective Scale Model (NZCSM) is a NWP model based on the
UK Met Office Unified Model. The following model output variables are needed
to run the lidar simulator: hybridt32, latitude, longitude, model_press,
model_qcf, model_qcl, theta_lev_temp, time0.

### CMIP5

TODO

CMIP5 model output can be downloaded from the [CMIP5 Earth System Grid (ESG) archive](https://esgf-node.llnl.gov/search/cmip5/). ALCF requires the following CMIP5
variables: cls, clc, clwc, clws, clic, clis, pfull, ps, ta, zfull, zhalf.

### JRA-55

TODO

License
-------

This software is available under the terms of the MIT license
(see [LICENSE.md](LICENSE.md)).

See also
--------

[ccplot](https://ccplot.org),
[cl2nc](https://github.com/peterkuma/cl2nc),
[mpl2nc](https://github.com/peterkuma/mpl2nc)
