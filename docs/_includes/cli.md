## Command line interface

After completing the [installation]({{ "/installation/" | relative_url }}), the
ALCF commands can be run in the terminal with the `alcf` program. The program
uses the command line argument format [PST](https://github.com/peterkuma/pst)
for passing complex command line arguments.

### Commands

| Command | Description |
| --- | --- |
| [alcf](cmd_main.html) | the main command |
| [alcf auto](cmd_auto.html) | peform automatic processing of model or lidar data |
| [alcf calibrate](cmd_calibrate.html) | calibrate lidar backscatter |
| [alcf convert](cmd_convert.html) | convert input instrument or model data to the ALCF standard NetCDF |
| [alcf lidar](cmd_lidar.html) | process lidar data |
| [alcf model](cmd_model.html) | extract model data at a point or along a track |
| [alcf plot](cmd_plot.html) | plot lidar data |
| [alcf simulate](cmd_simulate.html) | simulate lidar measurements from model data using COSP |
| [alcf stats](cmd_stats.html) | calculate cloud occurrence statistics |

<!-- | [compare](cmd_compare.html) | TODO | -->

### Automatic processing

Automatic processing of lidar measurements can be done with the
`alcf auto lidar` command and performs resampling, noise removal,
cloud detection, calculates cloud occurrence and backscatter histograms and
plots backscatter profiles, cloud occurrence and the backscatter histogram.
`alcf auto lidar` does not perform initial data conversion from raw instrument
data to NetCDF, and this needs to be done manually by running `alcf convert`
for instruments which do not produce NetCDF output.

Automatic processing of model data can be done with the `alcf auto model`
command and performs extraction of model data, runs the lidar simulator,
and processes the simulated backscatter in the same way as `alcf lidar`.


<!--
Automatic comparison of processed lidar or model data (the output of
`alcf lidar` or `alcf model`, respectively) can be done with
`alcf auto compare`.
-->

### Manual processing

The commands are usually run in the following order.

ALC observations processing:

1. `alcf convert` – convert raw ALC data to NetCDF (only if not in NetCDF
    already),
2. `alcf lidar` – produce resampled data,
3. `alcf plot backscatter` – plot backscatter profiles,
4. `alcf stats` – calculate summary statistics from resampled
    lidar data from step 2.,
5. `alcf plot cloud_occurrence` – plot cloud occurrence calculated in step 4.,
6. `alcf plot backscatter_hist` – plot backscatter histogram calculated in
    step 4.

<!--
4. `alcf calibrate` (TODO) – calculate calibration coefficient based on opaque
    stratocumulus intervals identified in step 3.,
5. `alcf lidar` – produce calibrated resampled data,
6. `alcf plot backscatter` – plot calibrated backscatter profiles
7. `alcf stats` – calculate summary statistics from calibrated resampled
    lidar data from step 5.
8. `alcf plot cloud_occurrence` – plot cloud occurrence calculated in step 7.
9. `alcf plot backscatter_hist` – plot backscatter histogram calculated in
    step 7.
-->

Model output processing:

1. `alcf model` – extract model data at a geographical point or along a
    ship track,
2. `alcf simulate` – simulate backscatter based on data from step 1.,
3. `alcf lidar` – resample simulated backscatter data from step 2.,
4. `alcf plot backscatter` – plot simulated backscatter profiles from step 3.,
5. `alcf stats` – calculate summary statistics from resampled simulated
    backscatter data from step 3.,
6. `alcf plot cloud_occurrence` – plot cloud occurrence calculated in step 5.,
7. `alcf plot backscatter_hist` – plot backscatter histogram calculated in
    step 5.

NetCDF data files generated in each step are described in the
[ALCF output]({{ "/documentation/alcf_output/" | relative_url }}) and can be previewed in
[Panoply](https://www.giss.nasa.gov/tools/panoply/).
