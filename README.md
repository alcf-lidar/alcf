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

A number of common ALCs and model formats (AMPS, MERRA2, ...) are supported and
support for a new format can be added by writing a read function in
Python.

<!--
The scientific part of ALCF is documented in the following paper:

Kuma et al. (2019): Ground-based lidar simulator framework for comparing models
and observations
-->

Please see [alcf-lidar.github.io](https://alcf-lidar.github.io) for more information.
