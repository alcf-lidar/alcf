---
title: Supported ALCs
layout: default
---

### [Documentation](../)
## Supported ALCs

The following ALCs are supported:

- Lufft CHM 15k
- Sigma Space MiniMPL
- Vaisala CL31, CL51

### Vaisala CL31, CL51

Vaisala CL31 and CL51 use near-infrared wavelength of 910 nm. The instruments
store backscatter in DAT files. These can be converted to NetCDF
with the `alcf convert cl51 <input> <output>` command, where `<input>`
and `<output>` are input and output directories, respectively. The NetCDF files
can then be used as input to the `alcf auto lidar` and `alcf lidar` commands.
Alternatively, you can use the tool [cl2nc](https://github.com/peterkuma/cl2nc)
to convert DAT files to NetCDF.

### Sigma Space MiniMPL

Sigma Space MiniMPL uses visible wavelength of 532 nm. The instrument
stores backscatter in MPL files. These can be converted to NetCDF using
the SigmaMPL software.  The NetCDF files can then be used as input to the
`alcf auto lidar` and `alcf lidar` commands. The tool
[mpl2nc](https://github.com/peterkuma/mpl2nc) can also convert MPL files
to NetCDF, however, these cannot be used as input to ALCF as they do not
contain all of the required variables.

### Lufft CHM 15k

Lufft CHM 15k uses near-infrared wavelength of 1064 nm. The instrument
stores backscatter in NetCDF files, which can be used directly with the ALCF
commands `alcf auto lidar` and `alcf lidar` without conversion.
