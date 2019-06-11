import sys
import os
import numpy as np
import aquarius_time as aq
import ds_format as ds
from alcf.models import MODELS

def model(type_, input_, point=None, time=None, track=None):
	model = MODELS.get(type_)
	if model is None:
		raise ValueError('Invalid type: %s' % type_)
	if point is not None and time is not None:
		lon = np.array([point[0], point[0]], dtype=np.float64)
		lat = np.array([point[1], point[1]], dtype=np.float64)
		time = np.array([time[0], time[1]], dtype=np.float64)
		track = {
			'lon': lon,
			'lat': lat,
			'time': time,
		}
	elif track is not None:
		pass
	else:
		raise ValueError('point and time or track is required')

	d = model.read(input_, track)
	return d

def run(type_, input_, output, point=None, time=None, track=None):
	"""
alcf model - extract model data at a point or along a track

Usage:

    alcf model <type> point: { <lon> <lat> } time: { <start> <end> } <input>
    	<output>
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

Types:

- `amps`: Antarctic Mesoscale Prediction System (AMPS)
- `merra2`: Modern-Era Retrospective Analysis for Research and Applications,
	Version 2 (MERRA-2)
- `nzcsm`: New Zealand Convection Scale Model (NZCSM)

Time format:

"YYYY-MM-DD[THH:MM[:SS]]", where YYYY is year, MM is month, DD is day,
HH is hour, MM is minute, SS is second. Example: 2000-01-01T00:00:00.

Track:

Track file is a NetCDF file containing 1D variables lon, lat, and time.
	"""
	time1 = [None, None]
	for i in 0, 1:
		time1[i] = aq.from_iso(time[i])
		if time1[i] is None:
			raise ValueError('Invalid time format: %s' % time[i])
	track1 = track

	if os.path.isdir(output):
		t1, t2 = time1[0], time1[1]
		for t in np.arange(np.floor(t1 - 0.5), np.ceil(t2 - 0.5)) + 0.5:
			output_filename = os.path.join(output, '%s.nc' % aq.to_iso(t))
			d = model(type_, input_, point, time=[t, t + 1.], track=track)
			if d is not None:
				ds.to_netcdf(output_filename, d)
				print('-> %s' % output_filename)
	else:
		d = model(type_, input_, point, time=time1, track=track)
		if d is not None:
			ds.to_netcdf(output, d)
			print('-> %s' % output)
