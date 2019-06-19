---
title: About
layout: default
---

## About

ALCF was developed at the <a href="https://www.canterbury.ac.nz">University of Canterbury</a>
with support from the <a href="https://www.deepsouthchallenge.co.nz">New Zealand Deep South National Science Challenge</a> and <a href="https://www.niwa.co.nz/">NIWA</a> for the purpose of evaluation of climate models based on automatic lidar and ceilometer (ALC) observations. ALCF has not yet been peer-reviewed. The current release
is a beta release.

### Abstract

Peter Kuma<sup>1</sup>, Adrian McDonald<sup>1</sup>, Olaf Morgenstern<sup>2</sup>

<p style="font-size: 80%">
<sup>1</sup> University of Canterbury, Christchurch, New Zealand<br>
<sup>2</sup> NIWA, Wellington, New Zealand
</p>

Atmospheric lidar measurements are a well-established tool for remote sensing of clouds. For over a decade, spaceborne lidar measurements produced by the CALIOP instrument on the CALIPSO satellite and CATS on the International Space Station have proven invaluable for model cloud evaluation in general circulation and numerical weather forecasting models. They have revealed the vertical structure of clouds, particularly in combination with radar instruments, which is impossible to obtain with passive remote sensing instruments. However, the measurements are limited by rapid attenuation of the lidar signal in thick clouds. Ground-based lidar measurements are becoming more common due to greater availability of instruments such as ceilometers installed on a wide scale globally. They can provide much needed lidar measurements of clouds "from below", but processing of lidar data and model evaluation using this data is not well-developed compared to satellite measurements. We present an open source tool called the Automatic Lidar and Ceilometer Framework (ALCF) which implements common lidar processing steps such as resampling, noise removal, cloud detection, calculation of statistics, as well as model—observation intercomparison by bundling the COSP/ACTSIM lidar simulator and allowing it to produce corresponding "curtain" lidar pseudo-measurements from model output of various models (MERRA-2, AMPS, CMIP5) for ground-based and shipborne instruments (Vaisala CL31, CL51, Lufft CHM 15k, Sigma Space MiniMPL). These pseudo-measurements can be compared in an ‘apples to apples’ comparison with observations. We hope this tool will enable ground-based lidars to be used more commonly for model evaluation and improvement efforts.

### See also

[ccplot](https://ccplot.org),
[cl2nc](https://github.com/peterkuma/cl2nc),
[mpl2nc](https://github.com/peterkuma/mpl2nc)
