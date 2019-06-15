
alcf plot - plot lidar data

Usage: `alcf plot <plot_type> <input> <output> [<options>] [<plot_options>]`

Arguments:

- `plot_type`: plot type (see Plot types below)
- `input`: input filename or directory
- `output`: output filename or directory
- `options`: see Options below
- `plot_options`: Plot type specific options. See Plot options below.

Plot types:

- `backscatter`: plot backscatter
- `backscatter_hist`: plot backscatter histogram
- `backscatter_sd_hist`: plot backscatter standard deviation histogram
- `cloud_occurrence`: plot cloud occurrence

Options:

- `dpi`: Resolution in dots per inch (DPI). Default: `300`.
- `grid`: Plot grid (`true` or `false`). Default: `false`.
- `height`: Plot height (inches).
    Default: `5` if `plot_type` is `cloud_occurrence` or `backscatter_hist`
    else `4`.
- `subcolumn`: Model subcolumn to plot. Default: `0`.
- `title`: Plot title.
- `width`: Plot width (inches).
    Default: `5` if `plot_type` is `cloud_occurrence` or `backscatter_hist`
    else `10`.

Plot options:

- `backscatter`:
	- `lr`: Plot lidar ratio (LR), Default: `false`.
	- `plot_cloud_mask`: Plot cloud mask. Default: `false`.
	- `sigma`: Suppress backscatter less than a number of standard deviations
		from the mean backscatter (real). Default: `3`.
	- `vlim`: `{ <min> <max }`. Value limits (10^6 m-1.sr-1).
        Default: `{ 5 200 }`.
- `backscatter_hist`:
    - `vlim`: `{ <min> <max }`. Value limits (%) or `none` for auto. If `none`
        and `vlog` is `none`, `min` is set to 1e-3 if less or equal to zero.
        Default: `none`.
    - `vlog`: use logarithmic scale for values. Default: `false`.
    - `xlim`: `{ <min> <max> }`. x axis limits (10^6 m-1.sr-1) or non for auto.
        Default: `none`.
    - `zlim`: `{ <min> <max> }`. y axis limits (m) or none for auto.
        Default: `none`.
- `cloud_occurrence`:
    - `colors`: Line colors. Default: `{ #0084c8 #dc0000 #009100 #ffc022 #ba00ff }`
    - `labels`: Line labels. Default: `none`.
    - `lw`: Line width. Default: `1`.
    - `xlim`: x axis limits `{ <min> <max> }` (%). Default: `{ 0 100 }`.
    - `zlim`: y axis limits `{ <min> <max> }` (m). Default: `{ 0 15 }`.
	