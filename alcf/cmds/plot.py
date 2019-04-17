# -*- coding: utf-8 -*-

import os
import sys
import numpy as np
import lidar_toolbox as lidar
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.dates import date2num, AutoDateFormatter, AutoDateLocator
from matplotlib.colors import ListedColormap, Normalize
import scipy.ndimage as ndimage
import aquarius_time as aq
import ds_format as ds
from alcf import misc
from alcf.lidars import LIDARS

VARIABLES = [
	'time',
	'backscatter',
	'zfull',
	'lr',
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

def plot_backscatter(d): #tt, z, bf, grey=False, xlim=None, ylim=None, track=None):
	# if grey:
	# 	cmap = ListedColormap(COLORS_GREY[1:-1])
	# 	levels = np.arange(10, 60, 10)
	# 	under = COLORS_GREY[0]
	# 	over = COLORS_GREY[-1]
	# else:
	cmap = 'nipy_spectral'
	levels = np.arange(20, 201, 20)
	under = '#ffffff'
	over = '#990000'
	# print(d['time'].shape, d['zfull'].shape, d['backscatter'].shape)

	# time_dt = aq.to_datetime(d['time'])
	cf = plt.contourf(d['time'], d['zfull']*1e-3, d['backscatter'].T*1e6,
		cmap=cmap,
		levels=levels,
		extend='both',
	)
	cf.cmap.set_under(under)
	cf.cmap.set_over(over)
	cf.set_clim(10, 200)
	# plt.grid(color='k', lw=0.1, alpha=0.5)
	plt.colorbar(
		# orientation='horizontal',
		pad=0.02,
		label=u'Backscatter (×10$^{-6}$ m$^{-1}$sr$^{-1}$)',
		fraction=0.07,
		aspect=30,
	)
	# if ylim is not None:
	# 	plt.ylim(ylim[0], ylim[1])
	# if xlim is not None:
	# 	plt.xlim(xlim[0], xlim[1])
	plt.xlabel('Time (UTC)')
	plt.ylabel('Height (km)')

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
	plt.plot(d['time'], d['lr'], lw=0.8, color='#0087ed')
	locator = AutoDateLocator()
	plt.gca().xaxis.set_major_locator(locator)
	plt.grid(lw=0.1, color='black')
	def f(x, pos):
		return aq.to_datetime(x).strftime('%d/%m\n%H:%M')
	formatter = plt.FuncFormatter(f)
	plt.gca().xaxis.set_major_formatter(formatter)
	# if xlim is not None:
	# 	plt.xlim(xlim[0], xlim[1])
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

def plot(plot_type, d, output,
	# ylim=[0, 7],
	# backscatter_sum=False,
	title='',
	# track=None,
	width=None,
	height=None,
	lr=False,
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

	# plt.rc('font', family='Open Sans')
	# plt.rc('lines', linewidth=1)
	if width is not None and height is not None:
		fig = plt.figure(figsize=[width, height])

	if plot_type == 'backscatter':
		if lr:
			gs = GridSpec(2, 1, height_ratios=[0.7, 0.3], hspace=0.3)
			plt.subplot(gs[0])
		plot_backscatter(d
			# grey=(type_ == 'particle_type'),
			# xlim=[t1, t2],
			# ylim=ylim,
			# track=d_track,
		)
		# # plot_cbh(tt, cbh)
		# if type_ == 'particle_type':
		# 	plot_particle_type()
		if lr:
			plt.subplot(gs[1])
			plot_lr(d)
		#plot_lr(t, 2.0*0.7/b_int, xlim=[t1, t2])
		# plt.suptitle(title, y=0.91)
		plt.savefig(output, bbox_inches='tight', dpi=300)
		# plt.clf()
		# plt.close()
		# plt.close(fig)
	else:
		raise ValueError('Unsupported plot type "%s"' % plot_type)

def run(plot_type, input_, output,
	lr=False,
	width=12,
	height=6,
	dpi=300,
):
	"""
alcf plot

Plot lidar data.

Usage:

	alcf plot <plot_type> <input> <output> [options]

Arguments:

- plot_type: plot type (see Plot types below)
- input: input filename or directory
- output: output filename or directory
- options: see Options below

Plot types:

- backscatter: plot backscatter

Options:

- lr: Plot lidar ratio (LR), Default: false.
- width: Plot width (inches). Default: 10.
- height: Plot height (inches). Default: 5.
- dpi: DPI. Default: 300.
	"""
	opts = {
		'width': width,
		'height': height,
		'lr': lr,
	}

	state = {}
	if os.path.isdir(input_):
		files = sorted(os.listdir(input_))
		for file in files:
			filename = os.path.join(input_, file)
			output_filename = os.path.join(
				output,
				os.path.splitext(file)[0] + '.png'
			)
			print('<- %s' % filename)
			d = ds.read(filename, VARIABLES)
			plot(plot_type, d, output_filename, **opts)
			print('-> %s' % output_filename)
	else:
		filename = _input
		output_filename = output_
		print('<- %s' % filename)
		d = ds.read(filename, VARIABLES)
		plot(plot_type, d, output_filename, **opts)
		print('-> %s' % output_filename)
