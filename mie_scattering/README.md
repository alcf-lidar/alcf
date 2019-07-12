Mie scattering
==============

This directory contains code for calculation of Mie scattering parameters
required by the COSP/ACTSIM lidar simulator.

## Contents

### plot_size_dist

Plot theoretical particle size distribution (log-normal or Gamma).

Usage: `bin/plot_size_dist { <type> <reff> <sigmaeff> }... <output> [num: <num>]`

Arguments:

- `type` – distribution type: `log-norm` or `gamma`
- `reff` – effective radius (μm)
- `sigmaeff` – effective standard deviation (μm)
- `output` – output plot filename (PDF)

Options:

- `num` – Number of `reff` bins. Default: 100000.

Example:

```sh
bin/plot_size_dist { lognorm 20 10 } { lognorm 20 5 } { lognorm 10 5 } plot/size_dist_lognorm.pdf
bin/plot_size_dist { gamma 20 10 } { gamma 20 5 } { gamma 10 5 } plot/size_dist_gamma.pdf
```

### calc_k

Calculate the scattering-to-extinction ratio k (inverse of the lidar ratio)
by integrating Mie scattering parameters over a range of particle radii.

Usage: `bin/calc_k <input> <type> <output> [sigmaeff_ratio: <sigmaeff_ratio>]`

Arguments:

- `input` – file containing Mie scattering parameters calculated by
    MIEV (see below)
- `type` – type of particle size distribution: `lognorm` or `gamma`
- `output` – output file (NetCDF)
- `sigmaeff_ratio` – Ratio of effective standard deviation to effective radius.
    Default: 0.25.

Example:

```sh
bin/calc_k out/miev_532 lognorm out/k_lognorm_532.nc
bin/calc_k out/miev_910 lognorm out/k_lognorm_910.nc
bin/calc_k out/miev_1064 lognorm out/k_lognorm_1064.nc
bin/calc_k out/miev_532 gamma out/k_gamma_532.nc
bin/calc_k out/miev_910 gamma out/k_gamma_910.nc
bin/calc_k out/miev_1064 gamma out/k_gamma_1064.nc
```

### plot_lr

Plot lidar ratio calculated by calc_k.

Usage: `bin/plot_lr <input>... <output> [xlim: { <xmin> <xmax> }] [ylim: { <ymin> <ymax> }]`

Arguments:

- `input` – output of calc_k (NetCDF)
- `output` – output plot filename (PDF)
- `xmin` – x axis minimum (μm). Default: 5.
- `xmax` – x axis maximum (μm). Default: 50.
- `ymin` – y axis minimum (sr). Default: 10.
- `ymax` – y axis maximum (sr). Default: 25.

Example:

```sh
bin/plot_lr out/k_*.nc plot/lr.pdf
```

## MIEV

`miev` contains the MIEV Mie scattering code by Dr. Warren J. Wiscombe
(see `miev/MIEV.doc` for documentation). We use MIEV to calculate the
extinction efficiency, scattering efficiency and the scattering phase function
at 180 degrees for a range of spherical particle radii. `main.f90` contains code
to calculate and print these parameters.

Build (requires gfortran):

```sh
cd miev
make
```

Usage:

```sh
./miev <wavelength_nm>
```

Arguments:

- `wavelength_nm` – laser wavelength (nm)

The output contains a line with metadata:

- `wavelength_nm` – the same as above
- `crefin` – complex refractive index

followed by a header line (`r qext qsca p180`), followed by lines containing
four space separated columns:

- `r` – particle radius (μm)
- `qext` – extinction efficiency (1)
- `qsca` – scattering efficiency (1)
- `p180` – scattering phase function at 180 degrees (1)

The particle radii range from 0.1 μm to 100 μm by 0.1 μm, and radii
identified as "spikes" by MIEV are ignored (not printed).

Example:

```sh
miev/miev 532 > out/miev_532
miev/miev 910 > out/miev_910
miev/miev 1064 > out/miev_1064
```
