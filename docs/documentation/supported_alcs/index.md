---
title: Supported ALCs
layout: default
---

### [Documentation]({{ "/documentation/" | relative_url }})

## Supported ALCs

The following ALCs are supported:

- [Lufft CHM 15k](https://www.lufft.com/products/cloud-height-snow-depth-sensors-288/ceilometer-chm-15k-nimbus-2300/)
- [Sigma Space MiniMPL](https://www.dropletmeasurement.com/micro-pulse-lidar/)
- [Vaisala CL31 and CL51](https://www.vaisala.com/en/products/weather-environmental-sensors/ceilometers-CL31-CL51-meteorology)
- [Vaisala CL61](https://www.vaisala.com/en/products/weather-environmental-sensors/ceilometer-CL61)
- [Cloudnet](https://cloudnet.fmi.fi) project data format (various instruments)
- [CALIPSO/CALIOP](https://www-calipso.larc.nasa.gov/) (lidar simulation only)

### Vaisala CT25K, CL31, CL51, CL61

**Type:** `blview`, `ct25k`, `cl31`, `cl51`, `cl61`

Vaisala CT25K, CL31, CL51 and CL61 are ceilometers which use near-infrared
wavelength of 905 nm (CT25k) and 910 nm (CL). CT25K, CL31 and CL51 store
backscatter in DAT files. These can be converted to NetCDF with the `alcf
convert cl51 <input> <output>` command, where `<input>` and `<output>` are
input and output directories, respectively. CL61 produces native NetCDF files.
The converted and native "L2" NetCDF files can be used as input to the `alcf
auto lidar` and `alcf lidar` commands.  Alternatively, you can use the tool
[cl2nc](https://github.com/peterkuma/cl2nc) to convert the CT25K, CL31 and CL51
DAT files to NetCDF.

The types `ct25k`, `cl31` and `cl51` read NetCDF files produced by cl2nc (or
`alcf convert cl51 <input> <output>`). The type `cl61` reads native NetCDF
files produced by the CL61 instrument. The type `blview` reads L2 NetCDF
produced by the vendor software BL-VIEW.

The 905-nm and 910-nm wavelength bands used by CT25K, CL31, CL51 and CL61 are
affected by water vapour absorption lines ([Wiegner et al.,
2019](https://www.atmos-meas-tech.net/12/471/2019/)). The ALCF currently does
not support simulating water vapour absorption, and it is not taken into
account in the calibration process.

The types `ct25k`, `cl31` and `cl51` also support reading a format of CL51
NetCDF files (`ceil`) produced by the Atmospheric Radiation Measurement (ARM)
campaigns.

### Sigma Space MiniMPL

**Type:** `mpl` (`mpl2nc`)

Sigma Space MiniMPL is a lidar which use visible wavelength of 532 nm. The instrument
stores backscatter in MPL files. These can be converted to NetCDF using
the SigmaMPL software. The NetCDF files can then be used as input to the
`alcf auto lidar` and `alcf lidar` commands. The tool
[mpl2nc](https://github.com/peterkuma/mpl2nc) can also convert MPL files
to NetCDF. Use the lidar type `mpl2nc` with `alcf auto lidar` and `alcf lidar`
to process data from mpl2nc.

### Lufft CHM 15k

**Type:** `chm15k`

Lufft CHM 15k is a ceilometer which uses near-infrared wavelength of 1064 nm.
The instrument stores backscatter in NetCDF files, which can be used directly
with the ALCF commands `alcf auto lidar` and `alcf lidar` without conversion.

### Cloudnet

**Type:** `cn_ct25k`, `cn_cl31`, `cn_cl51`, `cn_chm15k`, `cn_minimpl`

Data format produced by the Cloudnet project. Various instruments are supported:
Vaisala CT25K (`cn_ct25k`), CL31 (`cn_cl31`), CL51 (`cn_cl51`), CL61 (`cn_cl61`)
Lufft CHM 15k (`cn_chm15k`) and Sigma Space MiniMPL (`cn_minimpl`).

### CALIPSO/CALIOP

**Type:** `caliop`

CALIOP is a spaceborne lidar on board of the CNES-NASA satellite CALIPSO.
The ALCF supports lidar simulation of a spaceborne lidar at 532 nm, i.e. it can
produce simulated backscatter profiles from atmospheric model data. Therefore,
this lidar type can be used with `alcf simulate` and `alcf auto model`,
but not with `alcf lidar` or `alcf auto lidar`.
