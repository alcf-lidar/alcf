Automatic Lidar and Ceilometer Processing Framework (ALCF)
==========================================================

**Development status:** In development

ALCF is an open source command line tool for processing of automatic
lidar and ceilometer (ALC) data and intercomparison with atmospheric models
such as general circulation models (GCMs), numerical weather prediction models
(NWP) and reanalyses with a lidar simulator using the [COPS](https://github.com/CFMIP/COSPv2.0)
instrument simulator framework. ALCs are vertically pointing atmospheric
lidars, measuring cloud and aerosol backscatter.
The primary focus of ALCF are atmospheric studies of cloud using ALC
observations and model cloud validation.

ALCF can read input data from multiple ceilometers and atmopsheric lidars
(such as Vaisala CL51, Lufft CHM 15k, Sigma Space MiniMPL), convert them
to NetCDF, resample, calibrate, remove noise, detect cloud layers and cloud
base height. Atmospheric model data can be processed with the lidar simulator
to get backscatter profiles at the same location as the observations,
which can then be compared directly with the observations. The same
cloud detection algorithm is used on both observed lidar profiles and simulated
lidar profiles, so that cloud statistics such as cloud occurrence can be
compared between the model and observations.

A number of common ALCs and model formats (CMIP5, AMPS) are supported and
support for a new format can be added by writing a short read function in
Python or converting the ALC and model data to the ALCF NetCDF format
(described below).

<!--
The scientific part of ALCF is documented in the following paper:

Kuma et al. (2019): Ground-based lidar simulator framework for comparing models
and observations
-->

Requirements
------------

ALCF is written in Python and Fortran. Installation on Linux is recommended.

Installation
------------

<!--
Installation with PIP (Linux):

```sh
pip install alcf
```
-->

### Installation from source (optional)

<!-- A pre-compiled binary package is provided via PIP. -->
If you want to compile
ACLF yourself, you will need to install the
[PGI Fortran compiler](https://www.pgroup.com/products/community.htm).

Once you have install PGI, make sure the command `pgf95` works in the console.

To install in system directories:

```sh
python setup.py install
```

To install in user directories (make sure `~/.local/bin` is in the environmental variable `PATH`):

```sh
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
alcf simulate <config> <model> <output>

# Process lidar data
alcf process <lidar> <output>

# Plot lidar data
alcf plot lidar <lidar> <output>

# Calculate statistics
alcf stats <lidar> <output>

# Plot statistics
alcf plot stats <stats>
```

Commands
--------

### convert

### model

### simulate

### process

### plot

### stats

Supported models
----------------

The following GCM, NWP models and reanalyses are supported:

- CMIP5
- MERRA2
- AMPS

Supported ALCs
--------------

The following ALCs are supported:

- Vaisala CL31, CL51
- Lufft CHM 15k
- Sigma Space MiniMPL

License
-------

This software is available under the terms of the MIT license
(see [LICENSE.md](LICENSE.md)).
