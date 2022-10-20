## ALCF output

The ALCF output is stored in NetCDF files. Below is a description of variables
contained in the data files. Variable names follow the
[CMIP5 standard output](https://pcmdi.llnl.gov/mips/cmip5/docs/standard_output.pdf).
Time is stored as [Julian date](https://en.wikipedia.org/wiki/Julian_day)
(fractional number of days since -4712-01-01 12:00 UTC, or -4713-11-24 12:00
UTC in the proleptic Gregorian calendar) and can be converted to Unix time (the
number of non-leap seconds since 1970-01-01 00:00 UTC) with the formula
`(time - 2440587.5)*86400`.

### model

`alcf model` output is a 2-dimensional "curtain" of model data at a given location
over a length of time or along a ship track.

Variable | Description | Dimensions | Units
--- | --- | --- | ---
cl | cloud area fraction | time, level | %
cli | mass fraction of cloud ice | time, level | 1
clw | mass fraction of cloud liquid water | time, level | 1
lat | latitude | time | degrees north
lon | longitude | time | degrees east
orog | surface altitude | time | m
pfull | pressure at model full-levels | time, level | Pa
ps | surface air pressure | time | Pa
ta | air temperature | time, level | K
time | time | time | days since -4713-11-24 12:00 UTC (`proleptic_gregorian` calendar)
zfull | altitude of model full-levels | time, level | m

### cosp

`alcf simulate` output is a 2-dimensional "curtain" of simulated backscatter
at a given location over a length of time or along a ship track.

Variable | Description | Dimensions | Units
--- | --- | --- | ---
backscatter | total attenuated volume backscattering coefficient | time, level, column | m<sup>-1</sup>.sr<sup>-1</sup>
backscatter_mol | total attenuated molecular volume backscattering coefficient | time, level | m<sup>-1</sup>.sr<sup>-1</sup>
lat | latitude | time | degrees north
lon | longitude | time | degrees east
pfull | air pressure | time, level | Pa
time | time | time | -4713-11-24 12:00 UTC (`proleptic_gregorian` calendar)
zfull | height above reference ellipsoid | time, level | m

### lidar

`alcf lidar` output  is a 2-dimensional "curtain" of observed or simulated
backscatter at a given location over a length of time or along a ship track.

Variable | Description | Dimensions | Units
--- | --- | --- | ---
backscatter | total attenuated volume backscattering coefficient | time, range | m<sup>-1</sup>.sr<sup>-1</sup>
backscatter_sd | total attenuated volume backscattering coefficient standard deviation | time, range | m<sup>-1</sup>.sr<sup>-1</sup>
cbh | cloud base height | time | m
cloud_mask | cloud mask | time, range | 1
lr | lidar ratio | time | sr
time | time | time | days since -4713-11-24 12:00 UTC (`proleptic_gregorian` calendar)
zfull | altitude of full-levels | time, level | m

### stats

`alcf stats` output contains histograms and summary statistics calculated
from a 2-dimensional "curtain" of observed or simulated backscatter.

Variable | Description | Dimensions | Units
--- | --- | --- | ---
backscatter_avg | total attenuated volume backscattering coefficient average | zfull | m<sup>-1</sup>.sr<sup>-1</sup>
backscatter_full | total attenuated volume backscattering coefficient | backscatter_full | m<sup>-1</sup>.sr<sup>-1</sup>
backscatter_hist | total attenuated volume backscattering coefficinet histogram | backscatter_full, zfull | %
backscatter_mol_avg | total attenuated molecular volume backscattering coefficient average | zfull | m<sup>-1</sup>.sr<sup>-1</sup>
backscatter_sd_full | total attenuated volume backscattering coefficient standard deviation | backscatter_sd_full | m<sup>-1</sup>.sr<sup>-1</sup>
backscatter_sd_hist | total attenuated volume backscattering coefficient standard deviation histogram | backscatter_sd_full | %
backscatter_sd_z | total attenuated volume backscattering coefficient standard deviation height above reference ellipsoid | m
cl | cloud area fraction | zfull | %
clt | total cloud fraction | | %
n | number of profiles | | 1
zfull | altitude of model full-levels | zfull | m
