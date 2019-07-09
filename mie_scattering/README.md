Mie scattering
==============

## Contents

### plot_size_dist

Plot theoretical particle size distribution (log-normal or Gamma).

Usage: `bin/plot_size_dist <type> <output> [<mean>] [<sd>]`

Arguments:

- `type` – Distribution type: `log-norm` or `gamma`.
- `output` – Output plot filename (PNG or PDF).
- `mean` – Distribution mean (effective radius). Default: 20 um.
- `sd` – Standard deviation.

### calc_k (TODO)

Calculate the scattering-to-extinction ratio k by integrating Mie scattering
parameters over a range of particle radii.

Usage: `bin/calc_k <mie_parameters>`

Arguments:

- `mie_parameters` – file containing Mie scattering parameters calculated by
    MIEV (see below)

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

- `r` – particle radius (um)
- `qext` – extinction efficiency (1)
- `qsca` – scattering efficiency (1)
- `p180` – scattering phase function at 180 degrees (1)

The particle radii range from 0.1 um to 100 um by 0.1 um, and radii
identified as "spikes" by MIEV are ignored (not printed).

Example:

```sh
miev/miev 532 > out/miev_532
miev/miev 910 > out/miev_910
miev/miev 1064 > out/miev_1064
```
