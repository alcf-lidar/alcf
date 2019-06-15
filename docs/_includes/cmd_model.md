
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
- `merra2`: Modern-Era Retrospective Analysis for Research and Applications,
	Version 2 (MERRA-2)
- `nzcsm`: New Zealand Convection Scale Model (NZCSM)
- `nzesm`: New Zealand Earth System Model (NZESM) (experimental)

Time format:

"YYYY-MM-DD[THH:MM[:SS]]", where YYYY is year, MM is month, DD is day,
HH is hour, MM is minute, SS is second. Example: 2000-01-01T00:00:00.

Track:

Track file is a NetCDF file containing 1D variables `lon`, `lat`, and `time`.
`time` is time in format conforming with the NetCDF standard,
`lon` is longitude between 0 and 360 degrees and `lat` is latitude between
-90 and 90 degrees.
	