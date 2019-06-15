
alcf stats - calculate cloud occurrence statistics

Usage: `alcf stats <input> <output> [<options>]`

Arguments:

- `input`: input filename or directory
- `output`: output filename or directory

Options:

- `blim: <value>`: backscatter histogram limits (1e-6 m-1.sr-1).
    Default: `{ 5 200 }`.
- `bres: <value>`: backscatter histogram resolution (1e-6 m-1.sr-1).
    Default: `10`.
- `filter: <value>`: filter profiles by condition: `cloudy` for cloudy profiles
    only, `clear` for clear sky profiles only, `none` for all profiles.
    Default: `none`.
- `tlim: { <start> <end> }`: Time limits (see Time format below).
    Default: `none`.
- `zlim: { <low> <high> }`: Height limits (m). Default: `{ 0 15000 }`.
- `zres: <value>`: Height resolution (m). Default: `50`.
- `bsd_lim: { <low> <high> }`: backscatter standard deviation histogram limits
    (1e-6 m-1.sr-1). Default: `{ 0 10 }`.
- `bsd_log: <value>`: enable/disable logarithmic scale of the backscatter
    standard deviation histogram (`true` or `false`). Default: `true`.
- `bsd_res: <value>`: backscatter standard deviation histogram resolution
    (1e-6 m-1.sr-1). Default: `0.1`.
- `bsd_z: <value>`: backscatter standard deviation histogram height (m).
    Default: `8000`.

Time format:

"YYYY-MM-DD[THH:MM[:SS]]", where YYYY is year, MM is month, DD is day,
HH is hour, MM is minute, SS is second. Example: 2000-01-01T00:00:00.
	