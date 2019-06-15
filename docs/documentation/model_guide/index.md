---
title: Model guide
layout: default
---

### [Documentation](../)
## Model guide

The following GCM, NWP models and reanalyses are supported:

- [AMPS](http://www2.mmm.ucar.edu/rt/amps/)
- [MERRA2](https://duckduckgo.com/?q=merra-2&t=ffab&ia=web)
- [NZCSM](https://www.nesi.org.nz/case-studies/improving-new-zealands-weather-forecasting-ability)

TODO:

- CMIP5
- JRA-55

Below is a description of the model output supported by ALCF. You might
have to modify the code for reading the model output depending on the
exact format of the model output, such as variable names and how they are
split among the output files.

### AMPS

**Source:** `alcf/models/amps.py`

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

**Source:** `alcf/models/merra2.py`

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

**Source:** `alcf/models/nzcsm.py`

New Zealand Convective Scale Model (NZCSM) is a NWP model based on the
UK Met Office Unified Model. The following model output variables are needed
to run the lidar simulator:

- hybridt32
- latitude
- longitude
- model_press,
- model_qcf
- model_qcl
- theta_lev_temp
- time0

### CMIP5

TODO

**Source:** `alcf/models/cmip5.py`

CMIP5 model output can be downloaded from the [CMIP5 Earth System Grid (ESG) archive](https://esgf-node.llnl.gov/search/cmip5/). ALCF requires the following CMIP5 variables:

- clc
- clic
- clis
- cls
- clwc
- clws
- pfull
- ps
- ta
- zfull
- zhalf

### JRA-55

TODO

### NZESM (experimental)

**Source:** `alcf/models/nzesm.py`

New Zealand Earth System Model output is a model based on HadGEM3. The
model output variables needed are:

- air_pressure
- air_temperature
- cloud_volume_fraction_in_atmosphere_layer
- latitude
- level_height
- longitude
- mass_fraction_of_cloud_ice_in_air
- mass_fraction_of_cloud_liquid_water_in_air
- time
