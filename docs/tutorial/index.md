---
title: Tutorial
layout: default
---

## Tutorial

TODO

This tutorial shows how to use ALCF to process ceilometer observations,
simulate a lidar from model output and compare the two. As an example,
we will use a month of Lufft CHM 15k ceilometer observations
at a site in Christchurch, New Zealand in October 2014 and the corresponding
MERRA-2 renalaysis output. To start, download the archive
[example.zip](example.zip) with source files.

Processing using ALCF can be done in two modes: automatic and manual.
Automatic is easier and will be convered here first. Both automatic
and manual processing are equivalent, but manual processing gives you a better
understanding of the processing steps and can be more useful if anything
goes wrong during the processing.

### Preparation

First, make sure that you have installed ALCF following the [installation
instructions](/installation), and the you can run `alcf` in the terminal.
Extract the archive `example.zip` in your working directory.

### Automatic processing

#### Observations

To process the observations use the following command:

```sh
alcf auto lidar chm15k raw/rutherford16/ obs
```

This command will resample the lidar data, remove noise, detect clouds,
calculate statistics, and plot the lidar backscatter, backscatter histogram
and cloud occurrence as a function of height.

#### Model

To process model data use the following command:

```sh
alcf auto model merra2 chm15k raw/merra2/ merra2 point: { } time: { }
```

This command will extract a "curtain" of data along the give point and time
period, run the lidar simulator on this data, simulating the Lufft CHM 15k
instrumnet, and then run the same processing as the observational data above.

### Manual processing

TODO

### Observations

Processing of observations is done in the following steps:

1. Convert raw Vaisala CL51 data to NetCDF.
2. Re-process the data to a common NetCDF format. Apply noise removal, resampling
and cloud detection.
3. Plot the backscatter.
4. Calculate summary statistics.
5. Plot the statistics.

#### Model

Processing of model data is done in the following steps:

### Conclusion

This tutorial introduced how to use ALCF to process one month of data
collected by the Lufft CHM 15k ceilometer and the corresponding data in the
MERRA-2 reanalysis. ALCF supports more advanced options described in the
[documentation](/documentation).
For support please see the [support](/support) page.
