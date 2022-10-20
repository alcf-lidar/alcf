## Supported ALCs

The following ALCs are supported:

- [Lufft CHM 15k](https://www.lufft.com/products/cloud-height-snow-depth-sensors-288/ceilometer-chm-15k-nimbus-2300/)
- [Sigma Space MiniMPL](https://www.micropulselidar.com/)
- [Vaisala CL31](https://www.vaisala.com/en/products/instruments-sensors-and-other-measurement-devices/weather-stations-and-sensors/cl31)
- [Vaisala CL51](https://www.vaisala.com/en/products/instruments-sensors-and-other-measurement-devices/weather-stations-and-sensors/cl51)
- [Vaisala CL61](https://www.vaisala.com/en/products/weather-environmental-sensors/ceilometer-CL61)
- [CALIPSO/CALIOP](https://www-calipso.larc.nasa.gov/) (lidar simulation only)

### Vaisala CL31, CL51, CL61

**Type:** `blview`, `cl31`, `cl51`, `cl61`

Vaisala CL31, CL51 and CL61 are ceilometers which use near-infrared wavelength
of 910 nm. CL31 and CL51 store backscatter in DAT files. These can be converted
to NetCDF with the `alcf convert cl51 <input> <output>` command, where
`<input>` and `<output>` are input and output directories, respectively. CL61
produces native NetCDF files. The converted and native "L2" NetCDF files can be
used as input to the `alcf auto lidar` and `alcf lidar` commands.
Alternatively, you can use the tool [cl2nc](https://github.com/peterkuma/cl2nc)
to convert the CL31 and CL51 DAT files to NetCDF.

The types `cl31`, `cl51` read NetCDF files produced by cl2nc
(or `alcf convert cl51 <input> <output>`). The type `cl61` reads native NetCDF
files produced by the CL61 instrument. The type `blview` reads L2 NetCDF produced
by the vendor software BL-VIEW.

The 910-nm wavelength band used by CL31, CL51 and CL61 is affected by water
vapour absorption lines ([Wiegner et al.,
2019](https://www.atmos-meas-tech.net/12/471/2019/)). The ALCF currently does
not support simulating water vapour absorption, and it is not taken into
account in the calibration process.

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

Lufft CHM 15k is a ceilometer which uses near-infrared wavelength of 1064 nm. The instrument
stores backscatter in NetCDF files, which can be used directly with the ALCF
commands `alcf auto lidar` and `alcf lidar` without conversion.

### CALIPSO/CALIOP

**Type:** `caliop`

CALIOP is a spaceborne lidar on board of the CNES-NASA satellite CALIPSO.
The ALCF supports lidar simulation of a spaceborne lidar at 532 nm, i.e. it can
produce simulated backscatter profiles from atmospheric model data. Therefore,
this lidar type can be used with `alcf simulate` and `alcf auto model`,
but not with `alcf lidar` or `alcf auto lidar`.
