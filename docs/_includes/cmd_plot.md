
alcf-plot -- Plot lidar data.
=========

Synopsis
--------

    alcf plot <plot_type> <input> <output> [<options>] [<plot_options>]

Arguments
---------

- `plot_type`: Plot type (see Plot types below).
- `input`: Input filename or directory.
- `output`: Output filename or directory.
- `options`: See Options below.
- `plot_options`: Plot type specific options. See Plot options below.

Plot types
----------

- `backscatter`: Plot backscatter from `alcf lidar` output.
- `backscatter_hist`: Plot backscatter histogram from `alcf stats` output.
- `backscatter_sd_hist`: Plot backscatter standard deviation histogram from `alcf stats` output.
- `cl`: Plot model cloud area fraction from `alcf lidar` output.
- `cli`: Plot model mass fraction of cloud ice from `alcf lidar` output.
- `cloud_occurrence`: Plot cloud occurrence from `alcf stats` output.
- `clw`: Plot model mass fraction of cloud liquid water from `alcf lidar` output.
- `clw+cli`: Plot model mass fraction of cloud liquid water and ice from `alcf lidar` output.

General options
---------------

- `dpi: <value>`: Resolution in dots per inch (DPI). Default: `300`.
- `--grid`: Plot grid.
- `height: <value>`: Plot height (inches). Default: `5` if `plot_type` is `cloud_occurrence` or `backscatter_hist` else `4`.
- `subcolumn: <value>`: Model subcolumn to plot. Default: `0`.
- `title: <value>`: Plot title.
- `width: <value>`: Plot width (inches). Default: `5` if `plot_type` is `cloud_occurrence` or `backscatter_hist` else `10`.

backscatter options
-------------------

- `lr: <value>`: Plot effective lidar ratio. Default: `true`.
- `cloud_mask: <value>`: Plot cloud mask. Default: `true`.
- `remove_bmol: <value>`: Remove molecular backscatter (observed data have to be coupled with model data via the `couple` option of `alcf lidar`). Default: `true`.
- `sigma: <value>`: Remove of number of standard deviations of backscatter from the mean backscatter (real). Default: `5`.
- `vlim: { <min> <max }`: Value limits (10^6 m-1.sr-1). Default: `{ 0.1 200 }`.
- `vlog: <value>`: Plot values on logarithmic scale: `true` of `false`. Default: `true`.

backscatter_hist options
------------------------

- `vlim: { <min> <max> }`: Value limits (%) or `none` for auto. If `none` and `vlog` is `none`, `min` is set to 1e-3 if less or equal to zero. Default: `none`.
- `--vlog`: Use logarithmic scale for values.
- `xlim: { <min> <max> }`: x axis limits (10^6 m-1.sr-1) or `none` for automatic. Default: `none`.
- `zlim: { <min> <max> }`: z axis limits (m) or `none` for automatic. Default: `none`.

backscatter_sd_hist options
---------------------------

- `xlim: { <min> <max> }`: x axis limits (10^6 m-1.sr-1) or `none` for automatic. Default: `none`.
- `zlim: { <min> <max> }`: z axis limits (%) or `none` for automatic. Default: `none`.

cl options
----------

- `vlim: { <min> <max> }`: Value limits (%). Default: `{ 0 100 }`.
- `vlog: <value>`: Plot values on logarithmic scale: `true` of `false`. Default: `false`.
- `zres: <zres>`: Height resolution (m). Default: `50`.

cli, clw, and clw+cli options
-----------------------------

- `vlim: { <min> <max> }`: Value limits (g/kg). Default: `{ 1e-3 1 }`.
- `vlog: <value>`: Plot values on logarithmic scale: `true` of `false`. Default: `true`.
- `zres: <zres>`: Height resolution (m). Default: `50`.

cloud_occurrence options
------------------------

- `colors: { <value>... }`: Line colors. Default: `{ #0084c8 #dc0000 #009100 #ffc022 #ba00ff }`
- `linestyle: { <value> ... }`: Line style (`solid`, `dashed`, `dotted`). Default: `solid`.
- `labels: { <value>... }`: Line labels. Default: `none`.
- `lw: <value>`: Line width. Default: `1`.
- `xlim: { <min> <max> }`: x axis limits (%). Default: `{ 0 100 }`.
- `zlim: { <min> <max> }`: z axis limits (m). Default: `{ 0 15 }`.

Examples
--------

Plot backscatter from processed Vaisala CL51 data in `alcf_cl51_lidar`
and store the output in the directory `alcf_cl51_backscatter`.

    alcf plot backscatter alcf_cl51_lidar alcf_cl51_backscatter
	