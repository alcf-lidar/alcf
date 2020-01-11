# -*- coding: utf-8 -*-

import os
import sys
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.dates import date2num, AutoDateFormatter, AutoDateLocator
from matplotlib.colors import ListedColormap, Normalize, BoundaryNorm, LogNorm
import matplotlib.lines as mlines
import aquarius_time as aq
import ds_format as ds
from alcf import misc
from alcf.lidars import LIDARS

COLORS = [
	'#0084c8',
	'#dc0000',
	'#009100',
	'#ffc022',
	'#ba00ff',
]

LINESTYLE = 'solid'

VARIABLES = [
	'time',
	'time_bnds',
	'backscatter',
	'backscatter_sd',
	'backscatter_sd_full',
	'backscatter_sd_hist',
	'zfull',
	'lr',
	'cl',
	'clt',
	'n',
	'cloud_mask',
	'backscatter_hist',
	'backscatter_full',
	'altitude',
]

def plot_legend(*args, theme='light', **kwargs):
	legend = plt.legend(*args, fontsize=8, **kwargs)
	f = legend.get_frame()
	f.set_facecolor('k' if theme == 'light' else 'white')
	f.set_linewidth(0)
	f.set_alpha(0.1 if theme == 'light' else 0.9)

def plot_profile(plot_type, d, cax,
	subcolumn=0,
	sigma=0.,
	zlim=None,
	vlim=[2, 200],
	vlog=True,
	**opts
):
	cmap = 'viridis'
	if vlog:
		norm = LogNorm(vlim[0], vlim[1])
	else:
		norm = Normalize(vlim[0], vlim[1])
	under = '#222222'
	#over = '#990000'
	if len(d['backscatter'].shape) == 3:
		b = d['backscatter'][:,:,subcolumn]
		cloud_mask = d['cloud_mask'][:,:,subcolumn]
		b_sd = d['backscatter_sd'][:,:,subcolumn] if 'backscatter_sd' in d \
			else np.zeros(b.shape, dtype=np.float64)
	else:
		b = d['backscatter']
		cloud_mask = d['cloud_mask']
		b_sd = d['backscatter_sd'] if 'backscatter_sd' in d \
			else np.zeros(b.shape, dtype=np.float64)
	t1 = d['time'][0] - 0.5*(d['time'][1] - d['time'][0])
	t2 = d['time'][-1] + 0.5*(d['time'][-1] - d['time'][-2])
	z1 = d['zfull'][0] - 0.5*(d['zfull'][1] - d['zfull'][0])
	z2 = d['zfull'][-1] + 0.5*(d['zfull'][-1] - d['zfull'][-2])

	if sigma > 0.:
		b[b - sigma*b_sd < vlim[0]*1e-6] = 0.
	im = plt.imshow(b.T*1e6,
		extent=(t1, t2, z1*1e-3, z2*1e-3),
		aspect='auto',
		origin='bottom',
		norm=norm,
		cmap=cmap,
	)
	plt.gca().set_facecolor(under)
	im.cmap.set_under(under)
	cb = plt.colorbar(
		cax=cax,
		label=u'Backscatter (×10$^{-6}$ m$^{-1}$sr$^{-1}$)',
		pad=0.03,
		fraction=0.05,
		aspect='auto',
		extend='both',
	)
	if opts.get('cloud_mask'):
		cf = plt.contour(d['time'], d['zfull']*1e-3, cloud_mask.T,
			colors='red',
			linewidths=1,
			linestyles='dashed',
			levels=[-1., 0.5, 2.],
		)
		plot_legend(
			handles=[mlines.Line2D([], [],
				color='red', linestyle='dashed', label='Cloud mask'
			)],
			theme='dark'
		)
	if 'altitude' in d:
		plt.plot(d['time'], d['altitude']*1e-3, color='red', lw=0.5)
	plt.xlabel('Time (UTC)')
	plt.ylabel('Height (km)')

	if zlim is not None:
		plt.ylim(zlim[0]*1e-3, zlim[1]*1e-3)

	def formatter_f(t, pos):
		return aq.to_datetime(t).strftime('%d/%m\n%H:%M')

	formatter = plt.FuncFormatter(formatter_f)
	locator = AutoDateLocator()
	plt.gca().xaxis.set_major_formatter(formatter)
	plt.gca().xaxis.set_major_locator(locator)

def plot_lr(d, subcolumn=0, **opts):
	lr = d['lr'][:,subcolumn] if d['lr'].ndim == 2 else d['lr'][:]
	plt.plot(d['time'], lr, lw=0.7, color='#0087ed')
	locator = AutoDateLocator()
	plt.gca().xaxis.set_major_locator(locator)
	plt.grid(lw=0.1, color='black')
	def f(x, pos):
		return aq.to_datetime(x).strftime('%d/%m\n%H:%M')
	formatter = plt.FuncFormatter(f)
	plt.gca().xaxis.set_major_formatter(formatter)
	plt.xlim(np.min(d['time']), np.max(d['time']))
	plt.ylim(0, 50)
	plt.ylabel('Lidar ratio (sr)')
	plt.xlabel('Time (UTC)')

def plot_cloud_occurrence(dd,
	colors=COLORS,
	linestyle=LINESTYLE,
	lw=None,
	labels=None,
	subcolumn=0,
	xlim=[0., 100.],
	zlim=[0., 15000],
	**kwargs
):
	for i, d in enumerate(dd):
		zfull = d['zfull']
		cl = d['cl'][:,subcolumn] \
			if len(d['cl'].shape) == 2 \
			else d['cl']
		clt = d['clt'][subcolumn] \
			if len(d['clt'].shape) == 1 \
			else d['clt']
		n = d['n']
		label = (labels[i] if labels is not None else '')
		label += ' | CF: %d%%' % clt
		plt.plot(cl, 1e-3*zfull,
			color=colors[i],
			linestyle=(linestyle[i] if type(linestyle) is list else linestyle),
			lw=lw,
			label=label,
		)
	plt.xlim(xlim[0], xlim[1])
	plt.ylim(zlim[0]*1e-3, zlim[1]*1e-3)
	plt.xlabel('Cloud occurrence (%)')
	plt.ylabel('Height (km)')

	if labels is not None:
		plot_legend()

def plot_backscatter_hist(d,
	subcolumn=0,
	xlim=None,
	zlim=None,
	vlim=None,
	vlog=False,
	**kwargs
):
	if vlim is None:
		vlim = [
			np.min(d['backscatter_hist'])*1e2,
			np.max(d['backscatter_hist'])*1e2
		]

	if vlog is False:
		norm = Normalize(vlim[0], vlim[1])
	else:
		if vlim[0] <= 0: vlim[0] = 1e-3
		norm = LogNorm(vlim[0], vlim[1])

	if xlim is None:
		xlim = [
			(1.5*d['backscatter_full'][0] - 0.5*d['backscatter_full'][1])*1e6,
			(1.5*d['backscatter_full'][-1] - 0.5*d['backscatter_full'][-2])*1e6,
		]

	under = '#222222'
	im = plt.imshow(
		d['backscatter_hist'].T*1e2
			if len(d['backscatter_hist'].shape) == 2
			else d['backscatter_hist'][:,:,subcolumn].T*1e2,
		origin='lower',
		aspect='auto',
		extent=(
			(1.5*d['backscatter_full'][0] - 0.5*d['backscatter_full'][1])*1e6,
			(1.5*d['backscatter_full'][-1] - 0.5*d['backscatter_full'][-2])*1e6,
			(1.5*d['zfull'][0] - 0.5*d['zfull'][1])*1e-3,
			(1.5*d['zfull'][-1] - 0.5*d['zfull'][-2])*1e-3,
		),
		norm=norm,
	)
	im.cmap.set_under(under)
	plt.gca().set_facecolor(under)
	plt.colorbar(
		label='Occurrence (%)',
		pad=0.03,
		fraction=0.03,
		aspect='auto',
		extend='both',
	)
	if xlim is not None:
		plt.xlim(xlim)
	if zlim is not None:
		plt.ylim(zlim[0]*1e-3, zlim[1]*1e-3)
	plt.xlabel('Total attenuated backscatter coefficient (×10$^{-6}$ m$^{-1}$sr$^{-1}$)')
	plt.ylabel('Height (km)')
	plt.axvline(0, lw=0.3, linestyle='dashed', color='k')

def plot_backscatter_sd_hist(dd,
	labels=None,
	xlim=None,
	zlim=None,
	colors=COLORS,
	linestyle=LINESTYLE,
	**kwargs
):
	for i, d in enumerate(dd):
		plt.plot(d['backscatter_sd_full']*1e6, d['backscatter_sd_hist'],
			lw=1,
			color=colors[i],
			linestyle=(linestyle[i] if type(linestyle) is list else linestyle),
			label=(labels[i] if labels is not None else None),
		)
	plt.gca().set_yscale('log')
	plt.gca().set_xscale('log')
	if xlim is not None:
		plt.xlim(xlim)
	if zlim is not None:
		plt.ylim(zlim)
	plt.xlabel('Total attenuated backscatter coefficient (×10$^{-6}$ m$^{-1}$sr$^{-1}$)')
	plt.ylabel('Occurrence (%)')
	if labels is not None:
		plot_legend()

def plot(plot_type, d, output,
	width=None,
	height=None,
	lr=False,
	grid=False,
	dpi=300,
	title=None,
	**kwargs
):
	mpl.rcParams['font.family'] = 'Public Sans'
	mpl.rcParams['axes.linewidth'] = 0.5
	mpl.rcParams['xtick.major.size'] = 3
	mpl.rcParams['xtick.major.width'] = 0.5
	mpl.rcParams['ytick.major.size'] = 3
	mpl.rcParams['ytick.major.width'] = 0.5

	if width is not None and height is not None:
		fig = plt.figure(figsize=[width, height])

	if plot_type == 'backscatter':
		if lr:
			gs = GridSpec(2, 2,
				width_ratios=[0.985, 0.015],
				height_ratios=[0.7, 0.3],
				hspace=0.4,
				wspace=0.05,
			)
			cax = plt.subplot(gs[1])
			ax = plt.subplot(gs[0])
		else:
			gs = GridSpec(1, 2,
				width_ratios=[0.985, 0.015],
				wspace=0.05,
			)
			cax = plt.subplot(gs[1])
			ax = plt.subplot(gs[0])
		plot_profile(plot_type, d, cax, **kwargs)
		if lr:
			plt.subplot(gs[2])
			plot_lr(d, **kwargs)
	elif plot_type == 'cloud_occurrence':
		plot_cloud_occurrence(d, **kwargs)
	elif plot_type == 'backscatter_hist':
		plot_backscatter_hist(d, **kwargs)
	elif plot_type == 'backscatter_sd_hist':
		plot_backscatter_sd_hist(d, **kwargs)
	else:
		raise ValueError('Invalid plot type "%s"' % plot_type)

	if grid:
		plt.grid(lw=0.1, color='k', alpha=1)

	if title is not None:
		plt.title(title)

	plt.savefig(output, bbox_inches='tight', dpi=dpi)

def run(plot_type, *args,
	lr=False,
	subcolumn=0,
	width=None,
	height=None,
	dpi=300,
	grid=False,
	colors=COLORS,
	linestyle=LINESTYLE,
	lw=1,
	labels=None,
	xlim=None,
	zlim=None,
	vlim=None,
	vlog=None,
	sigma=3.,
	cloud_mask=False,
	title=None,
	**kwargs
):
	"""
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

- `dpi: <value>`: Resolution in dots per inch (DPI). Default: `300`.
- `--grid`: plot grid
- `height: <value>`: Plot height (inches).
    Default: `5` if `plot_type` is `cloud_occurrence` or `backscatter_hist`
    else `4`.
- `subcolumn: <value>`: Model subcolumn to plot. Default: `0`.
- `title: <value>`: Plot title.
- `width: <value>`: Plot width (inches).
    Default: `5` if `plot_type` is `cloud_occurrence` or `backscatter_hist`
    else `10`.

Plot command options:

- `backscatter`:
    - `--lr`: plot lidar ratio (LR)
    - `--plot_cloud_mask`: plot cloud mask
    - `sigma: <value>`: Suppress backscatter less than a number of standard deviations
        from the mean backscatter (real). Default: `3`.
    - `vlim: { <min> <max }`. Value limits (10^6 m-1.sr-1).
        Default: `{ 10 2000 }`.
    - `vlog: <value>`: Plot values on logarithmic scale: `true` of `false`.
        Default: `true`.
- `backscatter_hist`:
    - `vlim: { <min> <max }`. Value limits (%) or `none` for auto. If `none`
        and `vlog` is `none`, `min` is set to 1e-3 if less or equal to zero.
        Default: `none`.
    - `--vlog`: use logarithmic scale for values
    - `xlim: { <min> <max> }`. x axis limits (10^6 m-1.sr-1) or `none` for
        automatic. Default: `none`.
    - `zlim: { <min> <max> }`. z axis limits (m) or `none` for automatic.
        Default: `none`.
- `backscatter_sd_hist`:
    - `xlim: { <min> <max> }`. x axis limits (10^6 m-1.sr-1) or `none` for
        automatic. Default: `none`.
    - `zlim: { <min> <max> }`. z axis limits (%) or `none` for
        automatic. Default: `none`.
- `cloud_occurrence`:
    - `colors: { <value>... }`: Line colors.
        Default: `{ #0084c8 #dc0000 #009100 #ffc022 #ba00ff }`
    - `linestyle`: { <value> ... }`: Line style (`solid`, `dashed`, `dotted`).
        Default: `solid`.
    - `labels: { <value>... }`: Line labels. Default: `none`.
    - `lw: <value>`: Line width. Default: `1`.
    - `xlim: { <min> <max> }`: x axis limits (%). Default: `{ 0 100 }`.
    - `zlim: { <min> <max> }`: z axis limits (m). Default: `{ 0 15 }`.
	"""
	input_ = args[:-1]
	output = args[-1]

	if plot_type in ('backscatter_hist', 'backscatter_sd_hist', 'cloud_occurrence'):
		width = width if width is not None else 5
		height = height if height is not None else 5
	else:
		width = width if width is not None else 10
		height = height if height is not None else 6

	opts = {
		'lr': lr,
		'subcolumn': subcolumn,
		'grid': grid,
		'colors': colors,
		'linestyle': linestyle,
		'lw': lw,
		'labels': labels,
		'sigma': sigma,
		'title': title,
		'cloud_mask': cloud_mask,
		'width': width,
		'height': height,
	}

	if xlim is not None: opts['xlim'] = xlim
	if zlim is not None: opts['zlim'] = zlim
	if vlim is not None: opts['vlim'] = vlim
	if vlog is not None: opts['vlog'] = vlog

	state = {}
	if plot_type in ('cloud_occurrence', 'backscatter_sd_hist'):
		dd = []
		for file in input_:
			print('<- %s' % file)
			dd += [ds.read(file, VARIABLES)]
		plot(plot_type, dd, output, **opts)
		print('-> %s' % output)
	elif plot_type == 'backscatter_hist':
		print('<- %s' % input_[0])
		d = ds.read(input_[0], VARIABLES)
		plot(plot_type, d, output, **opts)
		print('-> %s' % output)
	elif plot_type == 'backscatter':
		for input1 in input_:
			if os.path.isdir(input1):
				for file_ in sorted(os.listdir(input1)):
					filename = os.path.join(input1, file_)
					output_filename = os.path.join(
						output,
						os.path.splitext(file_)[0] + '.png'
					)
					print('<- %s' % filename)
					d = ds.read(filename, VARIABLES)
					plot(plot_type, d, output_filename, **opts)
					print('-> %s' % output_filename)
			else:
				print('<- %s' % input_)
				d = ds.read(input_, VARIABLES)
				plot(plot_type, d, output, **opts)
	else:
		raise ValueError('Invalid plot type "%s"' % plot_type)
