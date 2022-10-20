## Model guide

The following GCM, NWP models and reanalyses are supported:

- [AMPS](http://www2.mmm.ucar.edu/rt/amps/)
- [ERA5](https://www.ecmwf.int/en/forecasts/datasets/reanalysis-datasets/era5)
- [JRA-55](https://jra.kishou.go.jp/JRA-55/index_en.html)
- [MERRA2](https://gmao.gsfc.nasa.gov/reanalysis/MERRA-2/)
- [NZCSM](https://www.nesi.org.nz/case-studies/improving-new-zealands-weather-forecasting-ability)
- [UM](https://www.metoffice.gov.uk/research/approach/modelling-systems/unified-model/index)

**Note:** The ERA-Interim reanalysis is not supported due to the required fields
(mass fraction of cloud liquid water and ice in air) not available in the
dataset.

Below is a description of the model output supported by the ALCF. You might
have to modify the code for reading the model output depending on the
exact format of the model output, such as variable names and how they are
split among the output files.

### AMPS

**Source:** `alcf/models/amps.py`

The ALCF is compatible with the NetCDF AMPS output. You can find the
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

where `xx` is the [AMPS grid](http://www2.mmm.ucar.edu/rt/amps/information/configuration/maps_2017101012/maps.html), `YYYYmmdd` is the year (`YYYY`), month (`mm`) and day (`dd`). The `*_f000.nc`
files are not suitable for use with the ALCF as they do not contain all required
variables.

### ERA5

**Source:** `alcf/models/era5.py`

ERA5 reanalysis data can be downloaded from [Copernicus](https://cds.climate.copernicus.eu/#!/search?text=ERA5&type=dataset). Download the following datasets:

**ERA5 hourly data on pressure levels from 1979 to present**

- Product type: `reanalysis`
- Variable: `Geopotential`, `Specific cloud ice water content`, `Fraction of cloud cover`, `Specific cloud liquid water content`, `Temperature`
- Pressure level: *all*
- Time: *all* (preferred)
- Format: `NetCDF`

**ERA5 hourly data on single levels from 1979 to present**

- Product type: `reanalysis`
- Variable: `Surface pressure`, `Orography`
- Time: *the same as above*
- Format: `NetCDF`

Save the pressure-level files in a directory named `plev` and the surface-level
files in a directory named `surf`. Pass the path to the parent directory
to `alcf model` or `alcf auto model`.

### JRA-55

**Source:** `alcf/models/jra55.py`

The JRA-55 reanalysis data can be downloaded from the
[JRA-55 project website](https://jra.kishou.go.jp/JRA-55/index_en.html).
The following fields are required by the ALCF:

- `Const/LL25.grib` (Constant fields)
- `anl_p125/anl_p125_hgt` (Geopotential height @ Isobaric Surface)
- `anl_p125/anl_p125_tmp` (Temperature @ Isobaric Surface)
- `anl_surf125` (Surface analysis fields)
- `fcst_p125/fcst_p125_ciwc` (Cloud ice @ Isobaric Surface)
- `fcst_p125/fcst_p125_clwc` (Cloud liquid water @ Isobaric Surface)
- `fcst_p125/fcst_p125_tcdc` (Total cloud cover @ Isobaric Surface)

Download files for the period of interest all into the same directory.
The JRA-55 GRIB files have to be converted to NetCDF before they can be
used with the ALCF. Use [grib_to_netcdf](https://confluence.ecmwf.int/display/ECC/grib_to_netcdf)
to convert the data. All data files should reside in the same directory.

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

- `hybridt32`
- `latitude`
- `longitude`
- `model_press,`
- `model_qcf`
- `model_qcl`
- `theta_lev_temp`
- `time0`

<!--

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

-->

### NZESM (experimental)

**Source:** `alcf/models/nzesm.py`

New Zealand Earth System Model output is a model based on HadGEM3. The
model output variables needed are:

- `air_pressure`
- `air_temperature`
- `cloud_volume_fraction_in_atmosphere_layer`
- `latitude`
- `level_height`
- `longitude`
- `mass_fraction_of_cloud_ice_in_air`
- `mass_fraction_of_cloud_liquid_water_in_air`
- `time`

### UM

**Source:** `alcf/models/um.py`

The NetCDF output (configuration option `l_netcdf`) of the UK Met Office
Unified Model (UM) is supported. The following variables are required:

- `TALLTS` (time)
- `latitude_t` (latitude)
- `longitude_t` (longitude)
- `DALLTH_zsea_theta` (Height above mean sea level)
- `STASH_m01s00i265` (AREA CLOUD FRACTION IN EACH LAYER)
- `STASH_m01s00i408` (PRESSURE AT THETA LEVELS AFTER TS)
- `STASH_m01s00i409` (SURFACE PRESSURE AFTER TIMESTEP)
- `STASH_m01s16i004` (TEMPERATURE ON THETA LEVELS)

**ALCF <= 1.0.0-beta.2:**

- `STASH_m01s04i205` (CLOUD LIQUID WATER AFTER LS PRECIP)
- `STASH_m01s04i206` (CLOUD ICE CONTENT AFTER LS PRECIP)

**ALCF > 1.0.0-beta.2:**

- `STASH_m01s00i254` (QCL AFTER TIMESTEP)
- `STASH_m01s00i012` (QCF AFTER TIMESTEP)

The variables should be provided on all theta levels and as high temporal
sampling as possible (instantaneous). All variables should be dumped together
to the same NetCDF file, split by time into arbitrary number of files.

In addition, a file containing model orography is required. Convert the
model grid `qrparam.orog` file distributed with the UM to NetCDF with iris:

```sh
python -c "import iris;c=iris.load('qrparm.orog');iris.save(c,'qrparm.orog.nc')"
```

and put `qrparm.orog.nc` in the same directory as the model output files.
