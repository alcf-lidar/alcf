
alcf calibrate - calibrate ALC backscatter

Supported methods:

- O'Connor et al. (2004) - calibrate based on lidar ratio (LR) of fully
opaque stratocumulus clouds.

Usage: `alcf calibrate { <start> <end> }... <input>`

- `start`: interval start (see Time format below)
- `end`: interval end (see Time format below)
- `input`: input directory (output of uncalibrated alcf lidar)

Time format:

"YYYY-MM-DD[THH:MM[:SS]]", where YYYY is year, MM is month, DD is day,
HH is hour, MM is minute, SS is second. Example: 2000-01-01T00:00:00.
	