---
title: Home
layout: default
---

<p class="abstract">
ALCF is an open source command line tool for processing of automatic lidar and ceilometer (ALC) data and intercomparison with atmospheric models such as general circulation models (GCMs), numerical weather prediction (NWP) models and reanalyses with a lidar simulator using the COPS instrument simulator framework. ALCs are vertically pointing atmospheric lidars, measuring cloud and aerosol backscatter. The primary focus of ALCF are atmospheric studies of cloud using ALC observations and model cloud validation.
</p>

### Features

#### Multiple instruments and models

ALCF can process data from multiple ceilometers and lidars:
Vaisala CL31, CL51, Lufft CHM 15k, Sigma Space MiniMPL. Multiple models
and reanalyses are supported by the lidar simulator: MERRA-2, AMPS, NZCSM,
NZESM.

<div class="img-flex">
<a href="{% "/img/chm15k_512x.jpg" | relative_url }}"><img src="{{ "/img/chm15k_512x.jpg" | relative_url }}" height="200" /></a>
<a href="{% "/img/cl51_512x.jpg" | relative_url }}"><img src="{{ "/img/cl51_512x.jpg" | relative_url }}" height="200" /></a>
</div>

#### Resampling and noise removal

ALCF resamples lidar backscatter to chosen temporal and vertical sampling
to increase signal-to-noise ratio, calculates noise standard deviation from
the highest level and removes noise.

<div class="img-flex nospace">
<a href="{{ "/img/rutherford14_2014-03-30T00:00:00.png" | relative_url |}"><img src="{{ "/img/rutherford14_2014-03-30T00:00:00.png" | relative_url }}" width="600" /></a>
</div>

#### Lidar simulator

Embedded lidar simulator based on COSP can be applied on model data
to produce virtual backscatter measurements comparable with ALC observations
for the purpose of model evaluation.

#### Cloud detection

Cloud detection is done by applying a threshold on absolute backscatter.
More sophisticated algorithms may be added in the future.

#### Calibration

Lidar ratio can calculated and plotted along the backscatter for absolute
calibration of lidar backscatter using fully-opaque stratocumulus scenes
(O'Connor et al., 2004).

#### Plotting

#### Cloud occurrence

#### Backscatter histogram

#### Open source

<img src="{{ "/img/osi_mit.png" | relative_url }}" height="100" style="float: left; margin-right: 16px" />

ALCF is available under the terms of the MIT license, which allows free
use, copying, modification and redistribution.
