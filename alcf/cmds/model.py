import sys
import os
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
import numpy as np
import aquarius_time as aq
import ds_format as ds
from alcf.models import MODELS, META
from alcf import misc

def point_to_track(point, time):
	time_mid = 0.5*(time[0] + time[1])
	return {
		'lon': np.array([point[0], point[0]], dtype=np.float64),
		'lat': np.array([point[1], point[1]], dtype=np.float64),
		'time': np.array([time[0], time[1]], dtype=np.float64),
		'time_bnds': np.array([[time[0], time_mid], [time_mid, time[1]]],
			dtype=np.float64),
	}

def track_auto_time_bnds(time, track_gap=0):
	n = len(time)
	time_bnds = np.full((n, 2), np.nan, np.float64)
	time_bnds[0,0] = time[0]
	time_bnds[-1,1] = time[-1]
	time_avg = 0.5*(time[:-1] + time[1:])
	time_bnds[1:,0] = time_avg
	time_bnds[:-1,1] = time_avg
	if track_gap != 0:
		time_diff = time[1:] - time[:-1]
		mask1 = np.full(n, False, bool)
		mask2 = np.full(n, False, bool)
		mask1[:-1] = time_diff > track_gap
		mask2[1:] = time_diff > track_gap
		time_bnds[mask1,1] = time[mask1]
		time_bnds[mask2,0] = time[mask2]
	return time_bnds

def read_track(filenames, lon_180=False, track_gap=0):
	if type(filenames) not in [list, tuple]:
		filenames = [filenames]
	dd = []
	for filename in filenames:
		d = ds.read(filename, jd=True)
		if len(d['time']) < 2:
			raise ValueError('%s: Track must contain at least two records', filename)
		if 'time_bnds' not in d:
			d['time_bnds'] = track_auto_time_bnds(d['time'], track_gap)
			d['.']['time_bnds'] = {
				'.dims': ['time', 'bnds'],
				'long_name': 'time bounds',
				'standard_name': 'time',
				'units': 'days since -4713-11-24 12:00 UTC',
				'calendar': 'proleptic_gregorian',
			}
		dd += [d]
	d = ds.merge(dd, 'time')
	if lon_180:
		d['lon'] = np.where(d['lon'] > 0, d['lon'], 360. + d['lon'])
	return d

def override_year_in_time(time, year):
	try: len(time)
	except:	return override_year_in_time(np.array([time]), year)[0]
	date = aq.to_date(time)
	y = date[1]
	n = len(y)
	if np.all(y == year):
		return time
	ones = np.ones(n, int)
	zeros = np.zeros(n, int)
	start_old = aq.from_date([ones, y, ones, ones, zeros, zeros, zeros, zeros])
	start_new_1 = aq.from_date([1, year, 1, 1, 0, 0, 0])
	start_new = np.full(n, start_new_1)
	dt = time - start_old
	time_new = start_new + dt
	# Do this again in case the day overflows because of the old year is a leap
	# year while the new is not, and the time as near the end of the year.
	return override_year_in_time(time_new, year)

def track_has_seg(track, t1, t2):
	mask = (track['time_bnds'][:,0] < t2) & (track['time_bnds'][:,1] >= t1)
	return np.any(mask)

def worker(type_, input_, index, output, track, start, debug, r,
	override_year=None):
	try:
		if override_year is not None:
			t1 = override_year_in_time(start, override_year)
		else:
			t1 = start
		t2 = t1 + 1

		def track_f(t):
			dt = t - t1
			return misc.track_at(track, start + dt)

		model = MODELS[type_]
		output_filename = os.path.join(output, '%s.nc' % \
			aq.to_iso(start).replace(':', ''))
		warnings = []
		d = model.read(input_, index, track_f, t1, t2,
			warnings=warnings,
			recursive=r,
		)
		for w in warnings:
			if len(w) == 2:
				print('Warning: %s' % w[0], file=sys.stderr)
				if debug: print(w[1], file=sys.stderr)
				else: print('Use --debug to print debugging information.', file=sys.stderr)
			else:
				print('Warning: %s' % w, file=sys.stderr)
		if d is not None:
			if 'time_bnds' not in d and 'time' in d:
				d['time_bnds'] = misc.time_bnds(d['time'], model.STEP, t1, t2)
			for var in ['time', 'time_bnds']:
				if 'time' in d:
					d[var] = start + (d[var] - t1)
			d['.'] = META
			ds.write(output_filename, d)
			print('-> %s' % output_filename)
	except Exception as e:
		print('Warning: %s' % str(e), file=sys.stderr)
		if debug: print(traceback.format_exc(), file=sys.stderr)
		else: print('Use --debug to print debugging information.', file=sys.stderr)

def run(type_, input_, output,
	point=None,
	time=None,
	track=None,
	track_gap=21600,
	override_year=None,
	track_lon_180=False,
	debug=False,
	r=False,
	njobs=None,
	**kwargs
):
	'''
alcf-model -- Extract model data at a point or along a track.
==========

Synopsis
--------

    alcf model <type> point: { <lon> <lat> } time: { <start> <end> } [options] [--] <input> <output>

    alcf model <type> track: <track> [--] <input> <output>

Description
-----------

Arguments following `--` are treated as literal strings. Use this delimiter if the input or output file names might otherwise be interpreted as non-strings, e.g. purely numerical file names.

Arguments
---------

- `type`: Input data type (see Types below).
- `input`: Input directory.
- `output`: Output directory.
- `lon`: Point longitude (degrees East).
- `lat`: Point latitutde (degrees North).
- `start`: Start time (see Time format below).
- `end`: End time (see Time format below).
- `track: <file>`, `track: { <file>... }`: One or more track NetCDF files (see Files below). If multiple files are supplied and `time_bnds` is not present in the files, they are assumed to be multiple segments of a discontinous track unless the last and first time of adjacent tracks are the same.
- `track_gap: <interval>`: If the interval is not 0, a track file is supplied, the `time_bnds` variable is not defined in the file and any two adjacent points are separated by more than the specified time interval (seconds), then a gap is assumed to be present between the two data points, instead of interpolating location between the two points. Default: `21600` (6 hours).
- `options`: See Options below.

Options
-------

- `njobs: <n>`: Number of parallel jobs. Default: number of CPU cores.
- `-r`: Process the input directory recursively.
- `--track_lon_180`: Expect track longitude between -180 and 180 degrees.
- `override_year: <year>`: Override year in the track. Use if comparing observations with a model statistically and the model output does not have a corresponding year available. The observation time is converted to the same time relative to the start of the year in the specified year. Note that if the original year is a leap year and the override year is not, as a consequence of the above 31 December is mapped to 1 January. The output retains the original year as in the track, even though the model data come from the override year. Default: `none`.

Types
-----

- `amps`: Antarctic Mesoscale Prediction System (AMPS).
- `era5`: ERA5.
- `icon`: ICON.
- `icon_intake_healpix`: ICON through Intake-ESM on HEALPix grid.
- `jra55`: JRA-55.
- `merra2`: Modern-Era Retrospective Analysis for Research and Applications, Version 2 (MERRA-2).
- `nzcsm`: New Zealand Convection Scale Model (NZCSM).
- `nzesm`: New Zealand Earth System Model (NZESM). [Experimental]
- `um`: UK Met Office Unified Model (UM).

Time format
-----------

`YYYY-MM-DD[THH:MM[:SS]]`, where `YYYY` is year, `MM` is month, `DD` is day, `HH` is hour, `MM` is minute, `SS` is second. Example: `2000-01-01T00:00:00`.

Files
-----

The track file is a NetCDF file containing 1D variables `lon`, `lat`, `time`, and optionally `time_bnds`. `time` and `time_bnds` are time in format conforming with the CF Conventions (has a valid `units` attribute and optional `calendar` attribute), `lon` is longitude between 0 and 360 degrees and `lat` is latitude between -90 and 90 degrees. If `time_bnds` is provided, discontinous track segments can be specified if adjacent time bounds are not coincident. The variables `lon`, `lat` and `time` have a single dimension `time`. The variable `time_bnds` has dimensions (`time`, `bnds`).

Examples
--------

Extract MERRA-2 model data in `M2I3NVASM.5.12.4` at 45 S, 170 E between 1 and 2 January 2020 and store the output in the directory `alcf_merra2_model`.

    alcf model merra2 point: { -45.0 170.0 } time: { 2020-01-01 2020-01-02 } M2I3NVASM.5.12.4 alcf_merra2_model
	'''
	time_lim = [-np.inf, np.inf]
	if time is not None:
		for i in [0, 1]:
			time_lim[i] = aq.from_iso(time[i])
			if time_lim[i] is None:
				raise ValueError('Invalid time format: %s' % time[i])

	d_track = None
	if track is not None:
		d_track = read_track(track, track_lon_180, track_gap/86400.)
	elif point is not None and time is not None:
		d_track = point_to_track(point, time_lim)
	else:
		raise ValueError('Point and time or track is required')

	time_start = max(d_track['time_bnds'][0,0], time_lim[0])
	time_end = min(d_track['time_bnds'][-1,1], time_lim[1])

	# if os.path.isdir(output):

	model = MODELS.get(type_)
	if model is None:
		raise ValueError('Invalid type: %s' % type_)

	if njobs is None: njobs = os.cpu_count()

	warnings = []
	index = None
	if hasattr(model, 'index'):
		index = model.index(input_, warnings=warnings, recursive=r, njobs=njobs)

	with ProcessPoolExecutor(max_workers=njobs) as ex:
		fs = []
		tt = np.arange(np.floor(time_start - 0.5), np.ceil(time_end - 0.5)) + 0.5
		for t in tt:
			if not track_has_seg(d_track, t, t + 1):
				continue
			f = ex.submit(worker, type_, input_, index, output, d_track, t,
				debug, r, override_year)
			fs += [f]
	for w in warnings:
		if len(w) == 2:
			print('Warning: %s' % w[0], file=sys.stderr)
			if debug: print(w[1], file=sys.stderr)
			else: print('Use --debug to print debugging information.', file=sys.stderr)
		else:
			print('Warning: %s' % w, file=sys.stderr)
