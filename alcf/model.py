from models import MODELS

def run(type_, input_, output, point=None, time=None, track=None, *args, **kwargs):
	"""
alcf model - extract model data at a point or along a track

Usage:

	alcf model <type> point: { <lon> <lat> } time: { <start> <end> } <input> <output>
	alcf model <type> track: <track> <input> <output>

- `type`: input data type (see Types below)
- `input`: input dirname
- `output`: output dirname
- `lon`: point longitude
- `lat`: point latitutde
- `start`: start time (see Time format below)
- `end`: end time (see Time format below)
- `track`: track NetCDF file (see Track below)

Types:

- `cmip5`: CMIP5 models

Time format:

"YYYY-MM-DDTHH:MM:SS", where YYYY is year, MM is month, DD is day, HH is hour,
MM is minute, SS is second. Example: 2000-01-01T00:00:00.

Track:

Track file is a NetCDF file containing 1D variables `lon`, `lat`, and `time`.
	"""

	model = MODELS.get(type_)
	if model is None:
		raise ValueError('Invalid type: %s' % type_)

	if point is not None and time is not None:
		lon = np.array([point[0], point[0]], dtype=np.float64)
		lat = np.array([point[1], point[1]], dtype=np.float64)
		time = np.array([time[0], time[1]], dtype=np.float64)
		track1 = {
			'lon': lon,
			'lat': lat,
			'time': time,
		}
	elif track is not None:
		track1 = None
	else:
		raise ValueError('point and time or track is required')

	model.read(input_, track1)
