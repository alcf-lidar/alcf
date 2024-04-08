# -*- coding: utf-8 -*-

import os
import sys
import logging
import traceback
import copy
import numpy as np
import datetime as dt
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.dates import date2num, AutoDateFormatter, AutoDateLocator
from matplotlib.colors import ListedColormap, Normalize, BoundaryNorm, LogNorm
import matplotlib.lines as mlines
import aquarius_time as aq
import ds_format as ds
from alcf import misc, algorithms
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
	'backscatter_mol',
	'backscatter_sd_full',
	'backscatter_sd_hist',
	'zfull',
	'lr',
	'cbh',
	'cl',
	'clt',
	'n',
	'cloud_mask',
	'backscatter_hist',
	'backscatter_full',
	'altitude',
	'clw',
	'cli',
]

def time_to_dt(time):
	time_dt = aq.to_datetime(time)
	for i, t in enumerate(time_dt):
		if t.microsecond >= 0.5e6:
			t += dt.timedelta(microseconds=(1e6 - t.microsecond))
		else:
			t -= dt.timedelta(microseconds=t.microsecond)
		time_dt[i] = t
	return time_dt

def plot_legend(*args, theme='light', **kwargs):
	legend = plt.legend(*args, fontsize=8, **kwargs)
	f = legend.get_frame()
	f.set_facecolor('k' if theme == 'light' else 'white')
	f.set_linewidth(0)
	f.set_alpha(0.1 if theme == 'light' else 0.9)

def plot_profile(plot_type, d,
	cax=None,
	subcolumn=0,
	sigma=5,
	remove_bmol=True,
	vlim=None,
	vlog=None,
	zres=50,
	zlim=None,
	render='antialiased',
	**opts
):
	if plot_type == 'backscatter':
		cmap = copy.copy(mpl.cm.get_cmap('viridis'))
		under = '#222222'
		label = 'Att. vol. backscattering coef. (×10$^{-6}$ m$^{-1}$sr$^{-1}$)'
		if vlim is None:
			vlim = [0.1, 200]
		if vlog is None:
			vlog = True
		if len(d['backscatter'].shape) == 3:
			b = d['backscatter'][:,:,subcolumn]
			cloud_mask = d['cloud_mask'][:,:,subcolumn]
			bsd = d['backscatter_sd'][:,:,subcolumn] if 'backscatter_sd' in d \
				else np.zeros(b.shape, dtype=np.float64)
		else:
			b = d['backscatter']
			cloud_mask = d['cloud_mask']
			bsd = d['backscatter_sd'] if 'backscatter_sd' in d \
				else np.zeros(b.shape, dtype=np.float64)
		if sigma > 0:
			b -= sigma*bsd
		if remove_bmol and 'backscatter_mol' in d:
			bmol = d['backscatter_mol']
			mask = ~np.isnan(bmol)
			b[mask] -= bmol[mask]
		x = b*1e6
		x[x <= 0.] = 0.5*vlim[0] # A value below the limit.
		zfull = d['zfull']
	elif plot_type in ('clw', 'cli', 'cl'):
		cmap = copy.copy(mpl.cm.get_cmap({
			'clw': 'Reds',
			'cli': 'Blues',
			'cl': 'Greys_r',
		}[plot_type]))
		under = {
			'clw': 'white',
			'cli': 'white',
			'cl': 'k',
		}[plot_type]
		label = {
			'clw': 'Cloud water (g/kg)',
			'cli': 'Cloud ice (g/kg)',
			'cl': 'Cloud fraction (%)',
		}[plot_type]
		if vlim is None:
			vlim = {
				'clw': [1e-3, 1],
				'cli': [1e-3, 1],
				'cl': [0, 100],
			}[plot_type]
		if vlog is None:
			vlog = {
				'clw': True,
				'cli': True,
				'cl': False
			}[plot_type]
		x = d[plot_type]
		if plot_type in ('clw', 'cli', 'clw+cli'):
			x *= 1e3
		if x.shape == 3:
			x = x[:,:,subcolumn]
		if zlim is None:
			zlim = [np.min(d['zfull']), np.max(d['zfull'])]
		zhalf = np.arange(zlim[0], zlim[1] + zres, zres)
		zfull = 0.5*(zhalf[1:] + zhalf[:-1])
		xp = np.full((x.shape[0], len(zfull)), np.nan, np.float64)
		for i in range(xp.shape[0]):
			zhalfi = misc.half(d['zfull'][i,:])
			xp[i,:] = algorithms.interp(
				zhalfi, x[i,:], zhalf
			)
		x = xp
	else:
		raise ValueError('Invalid plot type "%s"' % plot_type)

	if vlog:
		norm = LogNorm(vlim[0], vlim[1])
	else:
		norm = Normalize(vlim[0], vlim[1])

	time = d['time']
	time_dt = time_to_dt(time)

	t1 = time_dt[0] - 0.5*(time_dt[1] - time_dt[0])
	t2 = time_dt[-1] + 0.5*(time_dt[-1] - time_dt[-2])
	z1 = zfull[0] - 0.5*(zfull[1] - zfull[0])
	z2 = zfull[-1] + 0.5*(zfull[-1] - zfull[-2])

	try:
		interpolation = {
			'antialiased': 'antialiased',
			'standard': 'none',
		}[render]
	except KeyError:
		raise ValueError('Invalid rendering method "%s"' % render) from None

	im = plt.imshow(x.T,
		extent=(date2num(t1), date2num(t2), z1*1e-3, z2*1e-3),
		aspect='auto',
		origin='lower',
		norm=norm,
		cmap=cmap,
		interpolation=interpolation,
	)
	im.cmap.set_under(under)

	cb = plt.colorbar(
		cax=cax,
		label=label,
		pad=0.03,
		fraction=0.05,
		extend='both',
	)

	if zlim is not None:
		plt.ylim(zlim[0]*1e-3, zlim[1]*1e-3)

	plt.xlabel('Time (UTC)')
	plt.ylabel('Height (km)')

	def format_func(t, p):
		return mpl.dates.num2date(t).strftime('%d/%m\n%H:%M')

	formatter = plt.FuncFormatter(format_func)
	locator = AutoDateLocator()
	plt.gca().xaxis.set_major_formatter(formatter)
	plt.gca().xaxis.set_major_locator(locator)

	if plot_type == 'backscatter' and opts.get('cloud_mask'):
		time_dt_exp = np.array([t1] + time_dt.tolist() + [t2])
		cloud_mask_exp = np.concatenate((
			cloud_mask[0:1,:],
			cloud_mask,
			cloud_mask[-2:-1,:],
		))
		cf = plt.contour(
			date2num(time_dt_exp),
			d['zfull']*1e-3,
			cloud_mask_exp.T,
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
		plt.plot(date2num(time_dt), d['altitude']*1e-3, color='red', lw=0.5)

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
	plt.ylabel('Eff. lidar ratio (sr)')
	plt.xlabel('Time (UTC)')

def plot_cloud_dist(plot_type, dd,
	colors=COLORS,
	linestyle=LINESTYLE,
	lw=None,
	labels=None,
	subcolumn=0,
	xlim=[0., 100.],
	zlim=[0., 15000],
	**kwargs
):
	var = {
		'cbh': 'cbh',
		'cloud_occurrence': 'cl',
	}[plot_type]
	for i, d in enumerate(dd):
		zfull = d['zfull']
		x = d[var][:,subcolumn] \
			if len(d[var].shape) == 2 \
			else d[var]
		label = (labels[i] if labels is not None else '')
		if plot_type == 'cloud_occurrence':
			clt = d['clt'][subcolumn] \
				if len(d['clt'].shape) == 1 \
				else d['clt']
			label += ' | CF: %d%%' % clt
		plt.plot(x, 1e-3*zfull,
			color=colors[i],
			linestyle=(linestyle[i] if type(linestyle) is list else linestyle),
			lw=lw,
			label=label,
		)
	plt.xlim(xlim[0], xlim[1])
	plt.ylim(zlim[0]*1e-3, zlim[1]*1e-3)
	plt.xlabel({
		'cbh': 'Cloud base height distribution (%)',
		'cloud_occurrence': 'Cloud occurrence (%)',
	}[plot_type])
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
	cmap = copy.copy(mpl.cm.get_cmap('viridis'))
	cmap.set_under(under)
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
		cmap=cmap,
	)
	plt.gca().set_facecolor(under)
	plt.gca().set_box_aspect(1)
	cax = plt.gca().inset_axes([1.03, 0, 0.03, 1],
		transform=plt.gca().transAxes)
	plt.gcf().colorbar(im,
		cax=cax,
		extend='both',
		label='Occurrence (%)',
	)
	if xlim is not None:
		plt.xlim(xlim)
	if zlim is not None:
		plt.ylim(zlim[0]*1e-3, zlim[1]*1e-3)
	plt.xlabel('Attenuated volume backscattering coefficient (×10$^{-6}$ m$^{-1}$sr$^{-1}$)')
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
	plt.xlabel('Attenuated volume backscattering coefficient (×10$^{-6}$ m$^{-1}$sr$^{-1}$)')
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
	fontsdir = os.path.join(os.path.dirname(__file__), '../fonts')
	for font in mpl.font_manager.findSystemFonts(fontsdir):
		mpl.font_manager.fontManager.addfont(font)
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
	elif plot_type in ('clw', 'cli', 'cl'):
		gs = GridSpec(1, 2,
			width_ratios=[0.985, 0.015],
			wspace=0.05,
		)
		cax = plt.subplot(gs[1])
		ax = plt.subplot(gs[0])
		plot_profile(plot_type, d, cax, **kwargs)
	elif plot_type == 'clw+cli':
		r = 10./(plt.gcf().get_figwidth())*0.045
		gs = GridSpec(1, 4,
			width_ratios=[max(0.015, 1. - 2*0.015 - r), 0.015, r, 0.015],
			wspace=0.15,
			figure=plt.gcf(),
		)
		cax1 = plt.subplot(gs[1])
		cax2 = plt.subplot(gs[3])
		ax = plt.subplot(gs[0])
		plot_profile('clw', d, cax1, alpha=0.5, **kwargs)
		plot_profile('cli', d, cax2, alpha=0.5, **kwargs)
	elif plot_type in ('cbh', 'cloud_occurrence'):
		plot_cloud_dist(plot_type, d, **kwargs)
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
	lr=True,
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
	sigma=5.,
	remove_bmol=True,
	cloud_mask=True,
	title=None,
	zres=50,
	render='antialiased',
	**kwargs
):
	'''
alcf-plot -- Plot lidar data.
=========

Synopsis
--------

    alcf plot <plot_type> [<options>] [<plot_options>] [--] <input> <output>

Description
-----------

Arguments following `--` are treated as literal strings. Use this delimiter if the input or output file names might otherwise be interpreted as non-strings, e.g. purely numerical file names.

Arguments
---------

- `plot_type`: Plot type (see Plot types below).
- `input`: Input filename or directory.
- `output`: Output filename or directory.
- `options`: See Options below.
- `plot_options`: Plot type specific options. See Plot options below.

Plot types
----------

- `backscatter`: Plot backscatter from `alcf lidar` output on time-height axes.
- `backscatter_hist`: Plot backscatter histogram from `alcf stats` output on backscatter-height axes.
- `backscatter_sd_hist`: Plot backscatter standard deviation histogram from `alcf stats` output.
- `cbh`: Plot cloud base height distribution from `alcf stats` output.
- `cl`: Plot model cloud area fraction from `alcf lidar` output on time-height axes.
- `cli`: Plot model mass fraction of cloud ice from `alcf lidar` output on time-height axes.
- `cloud_occurrence`: Plot cloud occurrence by height from `alcf stats` output.
- `clw`: Plot model mass fraction of cloud liquid water from `alcf lidar` output on time-height axes.
- `clw+cli`: Plot model mass fraction of cloud liquid water and ice from `alcf lidar` output on time-height axes.

General options
---------------

- `dpi: <value>`: Resolution in dots per inch (DPI). Default: `300`.
- `--grid`: Plot grid.
- `height: <value>`: Plot height (inches). Default: `5` if `plot_type` is `cloud_occurrence` or `backscatter_hist` else `4`.
- `subcolumn: <value>`: Model subcolumn to plot. Default: `0`.
- `title: <value>`: Plot title.
- `width: <value>`: Plot width (inches). Default: `5` if `plot_type` is `cloud_occurrence` or `backscatter_hist` else `10`.
- `render: <value>`: Render profiles anti-aliased (`antialiased`) or standard (`standard`). Standard is more suitable for short time intervals. Default: `antialiased`.

backscatter options
-------------------

- `lr: <value>`: Plot effective lidar ratio. Default: `true`.
- `cloud_mask: <value>`: Plot cloud mask. Default: `true`.
- `remove_bmol: <value>`: Remove molecular backscatter (observed data have to be coupled with model data via the `couple` option of `alcf lidar`). Default: `true`.
- `sigma: <value>`: Remove of number of standard deviations of backscatter from the mean backscatter (real). Default: `5`.
- `vlim: { <min> <max }`: Value limits (10^-6 m-1.sr-1). Default: `{ 0.1 200 }`.
- `vlog: <value>`: Plot values on logarithmic scale: `true` of `false`. Default: `true`.

backscatter_hist options
------------------------

- `vlim: { <min> <max> }`: Value limits (%) or `none` for auto. If `none` and `vlog` is `none`, `min` is set to 1e-3 if less or equal to zero. Default: `none`.
- `--vlog`: Use logarithmic scale for values.
- `xlim: { <min> <max> }`: x axis limits (10^-6 m-1.sr-1) or `none` for automatic. Default: `none`.
- `zlim: { <min> <max> }`: z axis limits (m) or `none` for automatic. Default: `none`.

backscatter_sd_hist options
---------------------------

- `xlim: { <min> <max> }`: x axis limits (10^-6 m-1.sr-1) or `none` for automatic. Default: `none`.
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

cbh and cloud_occurrence options
--------------------------------

- `colors: { <value>... }`: Line colors. Default: `{ #0084c8 #dc0000 #009100 #ffc022 #ba00ff }`
- `linestyle: { <value> ... }`: Line style (`solid`, `dashed`, `dotted`). Default: `solid`.
- `labels: { <value>... }`: Line labels. Default: `none`.
- `lw: <value>`: Line width. Default: `1`.
- `xlim: { <min> <max> }`: x axis limits (%). Default: `{ 0 100 }`.
- `zlim: { <min> <max> }`: z axis limits (m). Default: `{ 0 15 }`.

Examples
--------

Plot backscatter from processed Vaisala CL51 data in `alcf_cl51_lidar` and store the output in the directory `alcf_cl51_backscatter`.

    alcf plot backscatter alcf_cl51_lidar alcf_cl51_backscatter
	'''
	input_ = args[:-1]
	output = args[-1]

	if plot_type in ('backscatter_hist', 'backscatter_sd_hist', 'cbh', 'cloud_occurrence'):
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
		'remove_bmol': remove_bmol,
		'title': title,
		'cloud_mask': cloud_mask,
		'width': width,
		'height': height,
		'render': render,
	}

	if xlim is not None: opts['xlim'] = xlim
	if zlim is not None: opts['zlim'] = zlim
	if vlim is not None: opts['vlim'] = vlim
	if vlog is not None: opts['vlog'] = vlog
	if zres is not None: opts['zres'] = zres

	state = {}
	if plot_type in ('cbh', 'cloud_occurrence', 'backscatter_sd_hist'):
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
	elif plot_type in ('backscatter', 'clw', 'cli', 'clw+cli', 'cl'):
		for input1 in input_:
			if os.path.isdir(input1):
				for file_ in sorted(os.listdir(input1)):
					filename = os.path.join(input1, file_)
					output_filename = os.path.join(
						output,
						os.path.splitext(file_)[0] + '.png'
					)
					try:
						print('<- %s' % filename)
						d = ds.read(filename, VARIABLES)
					except SystemExit:
						raise
					except SystemError:
						raise
					except:
						logging.warning(traceback.format_exc())
					try:
						plot(plot_type, d, output_filename, **opts)
						print('-> %s' % output_filename)
					except SystemExit:
						raise
					except SystemError:
						sys.exit(1)
					except:
						logging.warning(traceback.format_exc())
					finally:
						plt.close()
			else:
				print('<- %s' % input1)
				d = ds.read(input1, VARIABLES)
				try:
					plot(plot_type, d, output, **opts)
				except SystemExit:
					raise
				except SystemError:
					sys.exit(1)
	else:
		raise ValueError('Invalid plot type "%s"' % plot_type)
