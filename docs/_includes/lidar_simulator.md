## Lidar simulator

### Introduction

The ALCF uses a modified version of COSPv1 for lidar simulation, which can
be found at [github.com/alcf-lidar/COSPv1](https://github.com/alcf-lidar/COSPv1).
The ACTSIM lidar simulator included in COSP has been modified to account
for the different viewing geometry and wavelength of a ground-based lidar.

If you want to add support for another lidar in the ALCF, you might have to
calculate Mie scattering parameters for the lidar wavelength, if it
is different from ones already implemented (532, 910, 1064 nm).
The code for calculating the parameters is located in
[github.com/alcf-lidar/alcf/mie_scattering](https://github.com/alcf-lidar/alcf/tree/master/mie_scattering).
Below is documentation on how to use this code.

### Mie scattering code

The `mie_scattering` directory in the ALCF contains code for calculation of Mie
scattering parameters required by the COSP/ACTSIM lidar simulator.
The code requires Python 3 and GNU Fortran (gfortran) for running.
The code is independent from the rest of the ALCF.

#### Overview

The code uses the Mie scattering code MIEV by Dr. Warren J. Wiscombe to
calculate extinction efficiency, scattering efficiency and the scattering phase
function
at 180 degrees as function of particule radius. The output of MIEV is then
used as input in `calc_k`, which calculates the backscatter-to-extinction
ratio k (the inverse of the lidar ratio) by integrating over a range
of radii, assuming a certain theoretical distribution of particle radii.
The calculated backscatter-to-extinction ratio is used as a lookup table
in the COSP/ACTSIM lidar simulator code (`actsim/mie_backscatter_*.F90` files
included from `actsim/lidar_simulator.F90`). The lidar ratio can be plotted by
`plot_lr`.

The code should be used in the following order:

- miev
- plot_size_dist
- calc_k
- plot_lr

The variable `k` in the NetCDF file produced by `calc_k` should be the content
of the lookup table `actsim/mie_backscatter_*.F90`, and the lookup table
should be included from `actsim/lidar_simulator.F90`.

#### MIEV

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

#### plot_size_dist

Plot theoretical particle size distribution (log-normal or Gamma).

Usage: `bin/plot_size_dist { <type> <reff> <sigmaeff> }... <output> [num: <num>]`

Arguments:

- `type` – distribution type: `lognorm` or `gamma`
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

#### calc_k

Calculate the backscatter-to-extinction ratio k (inverse of the lidar ratio)
by integrating Mie scattering parameters over a range of particle radii.

Usage: `bin/calc_k <input> <type> <output> [sigmaeff_ratio: <sigmaeff_ratio>]`

Arguments:

- `input` – file containing Mie scattering parameters calculated by
    MIEV (see above)
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

#### orig_cosp_poly

Calculate the backscatter-to-extinction ratio k based on the original COSP
polynnomials (Chepfer et al., 2007; Fig. 9).

Usage: `bin/orig_cosp_poly <type> <output>`

Arguments:

- `type` – see Types below
- `output` – output file (NetCDF)

Types:

- `liq` – liquid
- `ice` – ice
- `ice_ns` – ice (NS)

Example:

```sh
bin/orig_cosp_poly liq out/k_orig_cosp_poly_liq.nc
bin/orig_cosp_poly ice out/k_orig_cosp_poly_ice.nc
bin/orig_cosp_poly ice_ns out/k_orig_cosp_poly_ice_ns.nc
```

The original COSP polynomials are (`polpart` in `actsim/lidar_simulator.F90`):

- liquid: `2.6980e-8*x**4 + -3.7701e-6*x**3 + 1.6594e-4*x**2 + -0.0024*x + 0.0626`
- ice: `-1.0176e-8*x**4 + 1.7615e-6*x**3 + -1.0480e-4*x**2 + 0.0019*x + 0.0460`
- ice (NS): `1.3615e-8*x**4 + -2.04206e-6*x**3 + 7.51799e-5*x**2 + 0.00078213*x + 0.0182131`

where `x` is the effective radius.

#### plot_lr

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

Figure 1 shows the result of `plot_lr` for k calculated by
`calc_k` and `orig_cosp_poly`.

<figure><a href="lr.png"><img src="lr.png" width="500" /></a><figcaption><strong>Figure 1: </strong>Lidar ratio as a function of the effective radius.</figcaption></figure>
