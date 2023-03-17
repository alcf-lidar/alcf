---
title: About
layout: default
---

## About

The ALCF was developed at the <a href="https://www.canterbury.ac.nz">University
of Canterbury</a> with support from the <a
href="https://www.deepsouthchallenge.co.nz">New Zealand Deep South National
Science Challenge</a> and <a href="https://www.niwa.co.nz/">NIWA</a>, and at <a
href="https://www.su.se">Stockholm University</a> with support from the <a
href="https://nextgems-h2020.eu">NextGEMS</a> project, for the purpose of
evaluation of climate models based on automatic lidar and ceilometer (ALC)
observations.

### Abstract

Peter Kuma<sup>1</sup>, Adrian J. McDonald<sup>1</sup>, Olaf Morgenstern<sup>2</sup>, Richard Querel<sup>3</sup>, Israel Silber<sup>4</sup>, Connor J. Flynn<sup>5</sup>

<p style="font-size: 80%">
<sup>1</sup> University of Canterbury, Christchurch, New Zealand<br />
<sup>2</sup> NIWA, Wellington, New Zealand<br />
<sup>3</sup> NIWA, Lauder, New Zealand<br />
<sup>4</sup> Department of Meteorology and Atmospheric Science, Pennsylvania State University, University Park, PA, USA<br />
<sup>5</sup> Pacific Northwest National Laboratory, Richland, WA, USA
</p>

Automatic lidars and ceilometers (ALCs) provide valuable information on cloud
and aerosols but have not been systematically used in the evaluation of general
circulation models (GCMs) and numerical weather prediction (NWP) models.
Obstacles associated with the diversity of instruments, a lack of
standardisation of data products and open processing tools mean that the value
of large ALC networks worldwide is not being realised. We discuss a tool,
called the Automatic Lidar and Ceilometer Framework (ALCF), that overcomes
these problems and also includes a ground-based lidar simulator, which
calculates the radiative transfer of laser radiation and allows one-to-one
comparison with models. Our ground-based lidar simulator is based on the Cloud
Feedback Model Intercomparison Project (CFMIP) Observation Simulator Package
(COSP), which has been extensively used for spaceborne lidar intercomparisons.
The ALCF implements all steps needed to transform and calibrate raw ALC data
and create simulated attenuated volume backscattering coefficient profiles for
one-to-one comparison and complete statistical analysis of clouds. The
framework supports multiple common commercial ALCs (Vaisala CL31, CL51, Lufft
CHM 15k and Droplet Measurement Technologies MiniMPL), reanalyses (JRA-55, ERA5
and MERRA-2) and models (the Unified Model and AMPS – the Antarctic Mesoscale
Prediction System). To demonstrate its capabilities, we present case studies
evaluating cloud in the supported reanalyses and models using CL31, CL51, CHM
15k and MiniMPL observations at three sites in New Zealand. We show that the
reanalyses and models generally underestimate cloud fraction. If sufficiently
high-temporal-resolution model output is available (better than 6-hourly), a
direct comparison of individual clouds is also possible. We demonstrate that
the ALCF can be used as a generic evaluation tool to examine cloud occurrence
and cloud properties in reanalyses, NWP models, and GCMs, potentially utilising
the large amounts of ALC data already available. This tool is likely to be
particularly useful for the analysis and improvement of low-level cloud
simulations which are not well monitored from space. This has previously been
identified as a critical deficiency in contemporary models, limiting the
accuracy of weather forecasts and future climate projections. While the current
focus of the framework is on clouds, support for aerosol in the lidar simulator
is planned in the future.

### See also

[ccplot](https://ccplot.org),
[ccbrowse](https://github.com/peterkuma/ccbrowse),
[cl2nc](https://github.com/peterkuma/cl2nc),
[mpl2nc](https://github.com/peterkuma/mpl2nc),
[mrr2c](https://github.com/peterkuma/mrr2c)
