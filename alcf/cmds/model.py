import sys
import os
import numpy as np
import aquarius_time as aq
import ds_format as ds
from alcf.models import MODELS

def get_track_segment(track, t1, t2):
	mask = (track['time'] >= t1) & (track['time'] < t2)
	n = np.sum(mask)
	lon1, lon2 = np.interp([t1, t2], track['time'], track['lon'])
	lat1, lat2 = np.interp([t1, t2], track['time'], track['lat'])
	time = np.full(n + 2, np.nan, np.float64)
	lon = np.full(n + 2, np.nan, np.float64)
	lat = np.full(n + 2, np.nan, np.float64)
	time[1:-1] = track['time'][mask]
	lon[1:-1] = track['lon'][mask]
	lat[1:-1] = track['lat'][mask]
	time[0], time[-1] = t1, t2
	lon[0], lon[-1] = lon1, lon2
	lat[0], lat[-1] = lat1, lat2
	return {
		'time': time,
		'lon': lon,
		'lat': lat,
		'.': track['.']
	}

def model(type_, input_, point=None, time=None, track=None, debug=False):
	model = MODELS.get(type_)
	warnings = []
	if model is None:
		raise ValueError('Invalid type: %s' % type_)
	if track is not None:
		track_segment = get_track_segment(track, time[0], time[1])
		d = model.read(input_, track_segment, warnings=warnings)
	else:
		lon = np.array([point[0], point[0]], dtype=np.float64)
		lat = np.array([point[1], point[1]], dtype=np.float64)
		time = np.array([time[0], time[1]], dtype=np.float64)
		track = {
			'lon': lon,
			'lat': lat,
			'time': time,
		}
		d = model.read(input_, track, warnings=warnings)
	for w in warnings:
		if len(w) == 2:
			print('Warning: %s' % w[0], file=sys.stderr)
			if debug: print(w[1], file=sys.stderr)
			else: print('Use --debug to print debugging information.', file=sys.stderr)
		else:
			print('Warning: %s' % w, file=sys.stderr)
	return d

def run(type_, input_, output,
	point=None,
	time=None,
	track=None,
	track_override_year=None,
	track_lon_180=False,
	debug=False,
	**kwargs
):
	"""
alcf model - extract model data at a point or along a track

Usage:

    alcf model <type> point: { <lon> <lat> } time: { <start> <end> } <input>
    	<output> [options]
    alcf model <type> track: <track> <input> <output>

Arguments:

- `type`: input data type (see Types below)
- `input`: input directory
- `output`: output directory
- `lon`: point longitude
- `lat`: point latitutde
- `start`: start time (see Time format below)
- `end`: end time (see Time format below)
- `track`: track NetCDF file (see Track below)
- `options`: see Options below

Options:

- `track_override_year: <year>`: Override year in track.
    Use if comparing observations with a model statistically. Default: `none`.
- `--track_lon_180`: expect track longitude between -180 and 180 degrees

Types:

- `amps`: Antarctic Mesoscale Prediction System (AMPS)
- `era5`: ERA5
- `jra55`: JRA-55
- `merra2`: Modern-Era Retrospective Analysis for Research and Applications,
	Version 2 (MERRA-2)
- `nzcsm`: New Zealand Convection Scale Model (NZCSM)
- `nzesm`: New Zealand Earth System Model (NZESM) (experimental)
- `um`: UK Met Office Unified Model (UM)

Time format:

"YYYY-MM-DD[THH:MM[:SS]]", where YYYY is year, MM is month, DD is day,
HH is hour, MM is minute, SS is second. Example: 2000-01-01T00:00:00.

Track:

Track file is a NetCDF file containing 1D variables `lon`, `lat`, and `time`.
`time` is time in format conforming with the NetCDF standard,
`lon` is longitude between 0 and 360 degrees and `lat` is latitude between
-90 and 90 degrees.

Examples:

Extract MERRA-2 model data in `M2I3NVASM.5.12.4` at 45 S, 170 E between
1 and 2 January 2020 and store the output in the directory `alcf_merra2_model`.

    alcf model merra2 point: { -45.0 170.0 } time: { 2020-01-01 2020-01-02 } \\
    M2I3NVASM.5.12.4 alcf_merra2_model
	"""
	time1 = None
	track1 = None
	if track is not None:
		track1 = ds.read(track)
		if track_override_year is not None:
			date = aq.to_date(track1['time'])
			date[1][:] = track_override_year
			track1['time'] = aq.from_date(date)
		if track_lon_180:
			track1['lon'] = np.where(
				track1['lon'] > 0,
				track1['lon'],
				360. + track1['lon']
			)
		time1 = track1['time'][0], track1['time'][-1]
	elif point is not None and time is not None:
		pass
	else:
		raise ValueError('Point and time or track is required')

	if time is not None:
			time1 = [None, None]
			for i in 0, 1:
				time1[i] = aq.from_iso(time[i])
				if time1[i] is None:
					raise ValueError('Invalid time format: %s' % time[i])

	# if os.path.isdir(output):
	t1, t2 = time1[0], time1[1]
	for t in np.arange(np.floor(t1 - 0.5), np.ceil(t2 - 0.5)) + 0.5:
		output_filename = os.path.join(output, '%s.nc' % \
			aq.to_iso(t).replace(':', ''))
		d = model(type_, input_, point, time=[t, t + 1.],
			track=track1, debug=debug)
		if d is not None:
			ds.write(output_filename, d)
			print('-> %s' % output_filename)
	# else:
	# 	d = model(type_, input_, point, time=time1, track=track1)
	# 	if d is not None:
	# 		ds.to_netcdf(output, d)
	# 		print('-> %s' % output)
