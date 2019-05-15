# -*- coding: utf-8 -*-

import os
import sys
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.dates import date2num, AutoDateFormatter, AutoDateLocator
from matplotlib.colors import ListedColormap, Normalize, BoundaryNorm, LogNorm
import scipy.ndimage as ndimage
import aquarius_time as aq
import ds_format as ds
from alcf import misc
from alcf.lidars import LIDARS

mpl.use('Agg')

COLORS = [
	'#0084c8',
	'#dc0000',
	'#009100',
	'#ffc022',
	'#ba00ff',
]

VARIABLES = [
	'time',
	'backscatter',
	'backscatter_sd',
	'zfull',
	'lr',
	'cloud_occurrence',
	'n',
	'cloud_mask',
	'backscatter_hist',
	'backscatter_full',
]

# COLORS_GREY = [
# 	'#000000',
# 	'#333333',
# 	'#666666',
# 	'#999999',
# 	'#cccccc',
# 	'#ffffff',
# ]

# def format_lonlat(lon, lat):
# 	s_lon = '%d$^\circ$E' % lon if lon > 0 else '%d$^\circ$W' % -lon
# 	s_lat = '%d$^\circ$N' % lat if lat > 0 else '%d$^\circ$S' % -lat
# 	return s_lat + ' ' + s_lon

def plot_profile(plot_type, d, cax, subcolumn=0, sigma=0., ylim=None, **opts):
	if plot_type == 'backscatter':
		cmap = 'viridis'
		levels = np.arange(20, 201, 20)
		norm = Normalize(20, 200)
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
			b[b < (b - sigma*b_sd)] = 0.
		im = plt.imshow((b - sigma*b_sd).T*1e6,
			extent=(t1, t2, z1*1e-3, z2*1e-3),
			aspect='auto',
			origin='bottom',
			norm=norm,
			cmap=cmap,
		)
		im.cmap.set_under(under)
		# im.cmap.set_over(over)
		plt.colorbar(
			cax=cax,
			label=u'Backscatter (×10$^{-6}$ m$^{-1}$sr$^{-1}$)',
		)
		if opts.get('cloud_mask'):
			cf = plt.contour(d['time'], d['zfull']*1e-3, cloud_mask.T,
				colors='red',
				linewidths=0.3,
				linestyles='dashed',
				levels=[-1., 0.5, 2.],
			)
		# plt.grid(color='k', lw=0.1, alpha=0.5)
	plt.xlabel('Time (UTC)')
	plt.ylabel('Height (km)')

	plt.ylim(ylim[0], ylim[1])

	def formatter_f(t, pos):
# 		if track is not None:
# 			lon = np.interp(t, track['time'], track['lon'])
# 			lat = np.interp(t, track['time'], track['lat'])
# 			s = format_lonlat(lon, lat)
# 			return aq.to_datetime(t).strftime('%m-%d %H:%M\n' + s)
# 		else:
		return aq.to_datetime(t).strftime('%d/%m\n%H:%M')

	formatter = plt.FuncFormatter(formatter_f)
	locator = AutoDateLocator()
	plt.gca().xaxis.set_major_formatter(formatter)
	plt.gca().xaxis.set_major_locator(locator)

def plot_lr(d):
	plt.plot(d['time'], d['lr'], lw=0.7, color='#0087ed')
	locator = AutoDateLocator()
	plt.gca().xaxis.set_major_locator(locator)
	plt.grid(lw=0.1, color='black')
	def f(x, pos):
		return aq.to_datetime(x).strftime('%d/%m\n%H:%M')
	formatter = plt.FuncFormatter(f)
	plt.gca().xaxis.set_major_formatter(formatter)
	# if xlim is not None:
	# 	plt.xlim(xlim[0], xlim[1])
	plt.xlim(np.min(d['time']), np.max(d['time']))
	plt.ylim(0, 50)
	plt.ylabel('Lidar ratio (sr)')
	plt.xlabel('Time (UTC)')

# def plot_particle_type(tt, z):
# 	legend = plt.legend([
# 		plt.Line2D((0,1),(0,0), color='red'),
# 		plt.Line2D((0,1),(0,0), color='green'),
# 		plt.Line2D((0,1),(0,0), color='blue'),
# 		plt.Line2D((0,1),(0,0), color='purple'),
# 		plt.Line2D((0,1),(0,0), color='orange'),
# 		plt.Line2D((0,1),(0,0), color='turquoise'),
# 	], [
# 		'Warm Cloud',
# 		'Mixed Cloud',
# 		'Ice/Dust/Ash',
# 		'Rain/Dust',
# 		'Clean Aerosol',
# 		'Polluted Aerosol',
# 	],
# 		fontsize=8,
# 		ncol=6,
# 		labelspacing=0.1,
# 		fancybox=False,
# 		framealpha=1,
# 		facecolor='#ffffff',
# 		loc='upper center'
# 	)
# 	legend.get_frame().set_linewidth(0)
# 	plt.contour(tt, z.T*1e-3, pt.T == 6, colors='turquoise', linewidths=0.1)
# 	plt.contour(tt, z.T*1e-3, pt.T == 5, colors='orange', linewidths=0.1)
# 	plt.contour(tt, z.T*1e-3, pt.T == 3, colors='purple', linewidths=0.1)
# 	plt.contour(tt, z.T*1e-3, pt.T == 2, colors='blue', linewidths=0.1)
# 	plt.contour(tt, z.T*1e-3, pt.T == 1, colors='green', linewidths=0.1)
# 	plt.contour(tt, z.T*1e-3, pt.T == 0, colors='red', linewidths=0.1)

# def plot_cbh(time, cbh):
# 	mask = (np.isfinite(cbh) & (cbh >= 0)).astype(int)
# 	mask_diff = np.diff(mask)
# 	i = 0
# 	segments = []
# 	for j in range(len(time)):
# 		if j == len(time) - 1:
# 			if mask[j] == 1:
# 				segments.append([i, j])
# 		elif mask_diff[j] == -1:
# 			segments.append([i, j])
# 		elif mask_diff[j] == 1:
# 			i = j
# 	for s in segments:
# 		plt.plot(time[s[0]:s[1]], cbh[s[0]:s[1]]*1e-3, color='red')

def plot_cloud_occurrence(dd,
	colors=COLORS,
	lw=None,
	labels=None,
	subcolumn=0,
	xlim=[0., 100.],
	ylim=[0., 15.],
	**kwargs
):
	for i, d in enumerate(dd):
		zfull = d['zfull']
		cloud_occurrence = d['cloud_occurrence'][:,subcolumn] \
			if len(d['cloud_occurrence'].shape) == 2 \
			else d['cloud_occurrence']
		n = d['n']
		plt.plot(cloud_occurrence, 1e-3*zfull,
			color=colors[i],
			lw=lw,
			label=(labels[i] if labels is not None else None),
		)
	plt.xlim(xlim[0], xlim[1])
	plt.ylim(ylim[0], ylim[1])
	plt.xlabel('Cloud occurrence (%)')
	plt.ylabel('Height (km)')

	if labels is not None:
		legend = plt.legend()
		f = legend.get_frame()
		f.set_facecolor('k')
		f.set_linewidth(0)
		f.set_alpha(0.1)

def plot_backscatter_hist(d,
	subcolumn=0,
	xlim=None,
	ylim=None,
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
	if ylim is not None:
		plt.ylim(ylim)
	plt.xlabel('Total attenuated backscatter coefficient (×10$^{-6}$ m$^{-1}$sr$^{-1}$)')
	plt.ylabel('Height (km)')

def plot(plot_type, d, output,
	# ylim=[0, 7],
	# backscatter_sum=False,
	title='',
	# track=None,
	width=None,
	height=None,
	lr=False,
	grid=False,
	dpi=300,
	**kwargs
):

	# t1 = aq.from_datetime(time_start)
	# t2 = aq.from_datetime(time_end)
	# dd = lidar.read_interval(input_, time_start, time_end, [
	# 	'range',
	# 	'height',
	# 	'backscatter',
	# 	'time',
	# 	'particle_type',
	# 	'cbh'
	# ])
	# if len(dd) == 0: return
	# t = []
	# b = []
	# bf = []
	# z = []
	# r = None
	# pt = []
	# cbh = []
	# for d in dd:
	# 	n, m = d['backscatter'].shape
	# 	bf0 = lidar.filter_noise(d['backscatter'], d['range'])
	# 	t = np.hstack([t, d['time']])
	# 	r = d['range']
	# 	z.append(d['height'])
	# 	b.append(d['backscatter'])
	# 	bf.append(bf0)
	# 	if type_ == 'particle_type':
	# 		pt.append(d['particle_type'])
	# 	if 'cbh' in d:
	# 		cbh.append(d['cbh'])
	# if z[0].ndim == 2:
	# 	z = np.vstack(z)
	# else:
	# 	z = z[0]
	# b = np.vstack(b)
	# bf = np.vstack(bf)
	# if type_ == 'particle_type':
	# 	pt = np.vstack(pt)
	# cbh = np.hstack(cbh)

	# b = lidar.subsample(b)
	# bf = lidar.subsample(bf)
	# t = lidar.subsample(t)
	# cbh = lidar.subsample(cbh)

	# if b.shape[0] < 2: return

	# if track is not None:
	# 	d_track = lidar.read_track(track)
	# else:
	# 	d_track = None

	# b_int = np.zeros(len(t))
	# for i in range(len(t)):
	# 	b_int[i] = np.sum(bf[i,:]*np.diff([0] + list(r)))
	# if z.ndim == 2:
	# 	tt = np.outer(np.ones(z.shape[1]), t)
	# else:
	# 	tt = t

	mpl.rcParams['font.family'] = 'Open Sans'
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
		plot_profile(plot_type, d, cax, **kwargs
			# grey=(type_ == 'particle_type'),
			# xlim=[t1, t2],
			# ylim=ylim,
			# track=d_track,
		)
		# # plot_cbh(tt, cbh)
		# if type_ == 'particle_type':
		# 	plot_particle_type()
		if lr:
			plt.subplot(gs[2])
			plot_lr(d)
		#plot_lr(t, 2.0*0.7/b_int, xlim=[t1, t2])
		# plt.suptitle(title, y=0.91)
	elif plot_type == 'cloud_occurrence':
		plot_cloud_occurrence(d, **kwargs)
	elif plot_type == 'backscatter_hist':
		plot_backscatter_hist(d, **kwargs)
	else:
		raise ValueError('Invalid plot type "%s"' % plot_type)

	if grid:
		plt.grid(lw=0.5, color='k', alpha=0.3)
	plt.savefig(output, bbox_inches='tight', dpi=dpi)
	# plt.clf()
	# plt.close()
	# plt.close(fig)

def run(plot_type, *args,
	lr=False,
	subcolumn=0,
	width=None,
	height=None,
	dpi=300,
	grid=False,
	colors=COLORS,
	lw=1,
	labels=None,
	xlim=None,
	ylim=None,
	vlim=None,
	vlog=None,
	sigma=3.,
	cloud_mask=False,
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
- `cloud_occurrence`: plot cloud occurrence

Options:

- `subcolumn`: Model subcolumn to plot. Default: 0.
- `width`: Plot width (inches).
    Default: 5 if `plot_type` is `cloud_occurrence` else 10.
- `height`: Plot height (inches).
    Default: 5 if `plot_type` is `cloud_occurrence` else 4.
- `dpi`: DPI. Default: 300.
- `grid`: Plot grid (`true` or `false`). Default: false.

Plot options:

- `backscatter`:
	- `lr`: Plot lidar ratio (LR), Default: false.
	- `sigma`: Suppress backscatter less than a number of standard deviations
		from the mean backscatter (real). Default: 3.
	- `plot_cloud_mask`: Plot cloud mask. Default: false.
- `backscatter_hist`:
    - `xlim`: x axis limits `{ <min> <max> }` (10^6 m-1.sr-1) or non for auto.
        Default: none.
    - `zlim`: y axis limits `{ <min> <max> }` (km) or none for auto.
        Default: none.
    - `vlim`: value limits `{ <min> <max }` (%) or none for auto. If none and
        vlog is none, `min` is set to 1e-3 if less or equal to zero.
        Default: none.
    - 'vlog': use logarithmic scale for values. Default false.
- `cloud_occurrence`:
    - `xlim`: x axis limits `{ <min> <max> }` (%). Default: { 0 100 }.
    - `ylim`: y axis limits `{ <min> <max> }` (km). Default: { 0 15 }.
    - `colors`: Line colors. Default: { #0084c8 #dc0000 #009100 #ffc022 #ba00ff }
    - `lw`: Line width. Default: 1.
    - `labels`: Line labels. Default: `none`.
	"""
	input_ = args[:-1]
	output = args[-1]


	if plot_type in ('backscatter_hist', 'cloud_occurrence'):
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
		'lw': lw,
		'labels': labels,
		'sigma': sigma,
		'cloud_mask': cloud_mask,
	}

	if xlim is not None: opts['xlim'] = xlim
	if ylim is not None: opts['ylim'] = ylim
	if vlim is not None: opts['vlim'] = vlim
	if vlog is not None: opts['vlog'] = vlog

	state = {}
	if plot_type == 'cloud_occurrence':
		dd = []
		for file in input_:
			print('<- %s' % file)
			dd += [ds.read(file, VARIABLES)]
		plot(plot_type, dd, output, **opts)
		print('-> %s' % output)
	if plot_type == 'backscatter_hist':
		print('<- %s' % input_[0])
		d = ds.read(input_[0], VARIABLES)
		plot(plot_type, d, output, **opts)
		print('-> %s' % output)
	else:
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
