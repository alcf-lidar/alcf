---
title: Installation
layout: default
---

## Installation

Below you can find installation instructions for supported operating systems:

* [Linux](#linux) (recommended)
* [Windows](#windows) with the Windows Subsystem for Linux (Ubuntu)
* [macOS](#macos)

You can also [build the ALCF from the source code](#building-from-the-source-code)
if you want to modify any of its parts.

### Linux

The instructions below assume that you enter the commands in the terminal.

1. Install required system packages.

    On Debian-based Linux distributions (Ubuntu, Debian, Devuan, ...), install
    dependencies with:

    ```sh
    sudo apt install gcc make gfortran libhdf5-dev libnetcdf-dev \
        libnetcdff-dev python3 python3-setuptools python3-pip cython3 pipx \
        libeccodes-tools ncl-ncarg
    ```

    On Fedora, install dependencies with:

    ```sh
    sudo yum install make gcc gfortran hdf5-devel netcdf-devel \
        netcdf-fortran-devel python3-setuptools python3-pip python3-Cython \
        pipx eccodes ncl
    ```

    On AlmaLinux 9 (or later), install dependencies with:

    ```sh
    sudo dnf install epel-release
    sudo dnf config-manager --set-enabled crb
    sudo dnf install make gcc gfortran hdf5-devel netcdf-devel \
        netcdf-fortran-devel python3-devel python3-pip python3-setuptools \
        python3-numpy python3-Cython pipx eccodes ncl
    ```

2. Install the ALCF with:

    ```sh
    pipx install alcf
    mkdir -p ~/.local/share/man/man1
    ln -s ~/.local/pipx/venvs/alcf/share/man/man1/alcf*.1 ~/.local/share/man/man1/
    ```

    Make sure that `$HOME/.local/bin` is in the PATH environment variable.

### Windows

It is recommended to run ALCF on [Linux](#linux).

Installation on Windows is possible under the "Windows Subsystem for Linux".

1. Install "Ubuntu" from the Microsoft Store. You might have to enable
"Windows Subsystem for Linux" under "Windows Features" first.

2. Open "Ubuntu" from the Start Menu. Update packages with:

    ```sh
    apt update
    apt upgrade
    ```

    Follow the instructions above for installation on [Linux](#linux)
    (Debian-based distributions).

    Note: You can use `cd /mnt/c/Users/<user>`, where `<user>` is your Windows
    user name to change the current directory to your home directory, and `ls`
    to list the directory contents.

### macOS

The installation has been tested on macOS Ventura on Intel. Installation on
Apple ARM (M1 CPUs and later) may be possible but is untested.

1. Install [MacPorts](https://www.macports.org).

2. Install required MacPorts packages:

    ```sh
    sudo port install gcc12 hdf5 netcdf netcdf-fortran ecCodes ncarg
    sudo port select --set gcc mp-gcc12
    ```

3. Install required Python packages:

    ```sh
    python3 -m pip install numpy
    ```

4. Install the ALCF:

    ```sh
    python3 -m pip install alcf
    ```

Make sure that `/Users/<user>/Library/Python/<version>/bin` is included in the
`PATH` environment variable if not already, where `<user>` is your system
user name and `<version>` is the Python version. This path should be printed
by the above command. This can be done by adding this line to the file
`.zprofile` in your home directory and restart the Terminal:

```
PATH="$PATH:/Users/<user>/Library/Python/<version>/bin"
```

On macOS, the default shell zsh does not work with the command-line syntax
of the ALCF. It is highly recommeded to run any `alcf` commands in the `bash`
shell:

```sh
% bash
bash-3.2$ alcf
...
```

### Post-installation

After completing the installation, you should be able to run the ALCF in the
terminal:

```sh
alcf
```

should output:

```
{% include cmd_main.md %}
```

### How to uninstall ALCF

To uninstall ALCF on Linux:

```sh
pipx uninstall alcf
rm ~/.local/share/man/man1/alcf*.1
```

To uninstall ALCF on macOS with Anaconda:

```
pip uninstall alcf
```

### Building from the source code

If you want to build the ALCF from the source code, download the source code
from [GitHub](https://github.com/alcf-lidar/alcf) or one of the [releases
below](#releases), and run the following commands in the source code directory:

```sh
./download_cosp
pipx install . # Replace pipx with pip for installation in Anaconda.
mkdir -p ~/.local/share/man/man1
ln -s ~/.local/pipx/venvs/alcf/share/man/man1/alcf*.1 ~/.local/share/man/man1/
```

This will download and unpack [ALCF-COSP](https://github.com/alcf-lidar/alcf-cosp)
(a version of COSP with support for ground-based lidars), and compile and
install the ALCF. Use this option if you want to customise any parts of the
ALCF.

### Preparing a source distribution

To prepare a source distribution:

```sh
./download_cosp
python3 setup.py sdist
```

You might have to replace `python3` with `python` depending on the Python
distribution.

The resulting package can be found in `dist/alcf-<version>.tar.gz`. This is the
type of package available on [PyPI](https://pypi.org/).

## Releases

Below is a list of releases of the ALCF. The version numbers follow
the [Semantic Versioning](https://semver.org). Installation instructions
have been changing with versions. Please follow the installation instructions
in the documentation of the particular version.

#### [1.9.0](https://github.com/alcf-lidar/alcf/releases/tag/v1.9.0) (2024-05-03)

<details>
<summary>Release notes</summary>
<ul>
<li>Improvements in logging and error reporting.</li>
<li>Added --version option to print version and exit.</li>
<li>Added generic output file attributes (version and software).</li>
<li>alcf model: Empty files are no longer output.</li>
<li>alcf model: Check for filename instead of time variable in the UM module to ignore the orography file.</li>
<li>alcf stats: Avoid division by zero.</li>
<li>Improvements in the documentation.</li>
</ul>
</details>

#### [1.8.1](https://github.com/alcf-lidar/alcf/releases/tag/v1.8.1) (2024-04-26)

<details>
<summary>Release notes</summary>
<ul>
<li>alcf download: New command for downloading ERA5 and MERRA-2 data for a point or track.</li>
<li>alcf stats: Added cloud base height distribution calculation.</li>
<li>alcf auto: All-sky and clear fine backscatter histograms are now plotted.</li>
<li>alcf auto: Cloud base height distribution is now plotted.</li>
<li>alcf model: ERA5 cl variable is now trimmed to [0, 1] (-0.0 sometimes occurs in the data).</li>
<li>alcf model: Fixed handling of negative longitude.</li>
<li>alcf model: The option --track_lon_180 is now deprecated. The conversion is done automatically.</li>
<li>Division by zero warnings in LR calculation are now prevented.</li>
<li>Improvements in the documentation.</li>
</ul>
</details>

#### [1.7.0](https://github.com/alcf-lidar/alcf/releases/tag/v1.7.0) (2024-04-08)

<details>
<summary>Release notes</summary>
<ul>
<li>alcf model: New track_gap option to specify how gaps in the track should be detected. This changes the default behaviour to detect gaps for intervals longer than 6 hours. Previously gaps were never detected and the track was interpolated between every adjacent pair of points.</li>
<li>alcf stats: Fixed parsing of filter_include and filter_exclude options when only one filter file is supplied.</li>
<li>alcf stats: Fixed parsing of track option when multiple tracks are supplied.</li>
<li>Improvements in the documentation.</li>
</ul>
</details>

#### [1.6.0](https://github.com/alcf-lidar/alcf/releases/tag/v1.6.0) (2024-02-28)

<details>
<summary>Release notes</summary>
<ul>
<li>alcf model: Support for overriding year for situations when model time is different from observation time.</li>
<li>alcf model: Support for AMPS GRIB format converted to NetCDF with ncl_convert2nc.</li>
<li>alcf model: Support for ICON via Intake-ESM on HEALPix grid (icon_intake_healpix).</li>
<li>alcf model: Add support for caching of vgrid files in the icon module.</li>
<li>alcf convert: Support for converting AMPS GRIB to NetCDF with ncl_convert2nc.</li>
<li>alcf convert: Support for more file extensions, such as .asc for CL31.</li>
<li>alcf lidar: New cloud_threshold_exp option for exponentially varying cloud detection threshold.</li>
<li>alcf lidar: New options bsd and bsd_z for specifying explicit standard deviation of noise for cloud detection.</li>
<li>alcf lidar: New align_output option.</li>
<li>alcf lidar: New keep_vars option for keeping specified lidar variables.</li>
<li>alcf lidar: Fixed backscatter coupling.</li>
<li>alcf lidar: Fixed reading of lon and lat in the default lidar driver.</li>
<li>alcf stats: Added time_total output variable.</li>
<li>alcf stats: Specifying multiple filters is now supported.</li>
<li>Improved documentation.</li>
<li>eccodes is now a required package (required by alcf convert jra55).</li>
<li>mpl2nc is now a required package (required by alcf convert mpl).</li>
</ul>
</details>

#### [1.5.2](https://github.com/alcf-lidar/alcf/releases/tag/v1.5.2) (2023-09-09)

<details>
<summary>Release notes</summary>
<ul>
<li>Fixed installation of manual pages.</li>
<li>Fixed output aggregation with short time intervals.</li>
<li>Fixed installation on macOS Ventura.</li>
<li>aclf lidar: Fixed an array type error with certain values of zres.</li>
</ul>
</details>

#### [1.5.1](https://github.com/alcf-lidar/alcf/releases/tag/v1.5.1) (2023-08-19)

<details>
<summary>Release notes</summary>
<ul>
<li>alcf plot: New render option.</li>
<li>alcf plot: Fixed closing of temporary plot objects.</li>
<li>alcf plot: Fixed time axis tick locations.</li>
<li>alcf stats: Support for filtering by file.</li>
<li>alcf lidar: Support for adding near-range noise.</li>
<li>Fixes related to short output time intervals.</li>
<li>Support for installation with pipx.</li>
<li>Fixed output metadata.</li>
<li>Imporved documentation.</li>
</ul>
</details>

#### [1.5.0](https://github.com/alcf-lidar/alcf/releases/tag/v1.5.0) (2023-04-22)

<details>
<summary>Release notes</summary>
<ul>
<li>Fixed calculation of time and time bounds in model drivers.</li>
<li>Require ds-format 3.6.1, which fixes an issue with readdir.</li>
<li>Support for index reading in the AMPS model driver.</li>
<li>Less verbose output from the COSP simulator.</li>
</ul>
</details>

#### [1.4.1](https://github.com/alcf-lidar/alcf/releases/tag/v1.4.1) (2023-04-21)

<details>
<summary>Release notes</summary>
<ul>
<li>Fixed a missing function argument in model drivers.</li>
</ul>
</details>

#### [1.4.0](https://github.com/alcf-lidar/alcf/releases/tag/v1.4.0) (2023-04-21)

<details>
<summary>Release notes</summary>
<ul>
<li>IMPORTANT: Fixed temperature reading in the AMPS driver. Temperature was read as 32 K colder than it should, resulting in a relatively small but potentially significant error in lidar cloud occurrence calculated from AMPS data.</li>
<li>Fixed skip option handling.</li>
<li>Added support for ARM format of CL51 data.</li>
<li>Parallel processing of model input.</li>
<li>Partial time limiting support in lidar drivers using the time option.</li>
<li>Faster interpolation implemented in Cython.</li>
<li>Speed improvements in the ICON driver.</li>
<li>Improvements in documentation.</li>
</ul>
</details>

#### [1.3.1](https://github.com/alcf-lidar/alcf/releases/tag/v1.3.1) (2023-03-16)

<details>
<summary>Release notes</summary>
<ul>
<li>Fixed issues with a new version of NumPy.</li>
<li>Minor improvements in the documentation.</li>
</ul>
</details>

#### [1.3.0](https://github.com/alcf-lidar/alcf/releases/tag/v1.3.0) (2023-03-15)

<details>
<summary>Release notes</summary>
<ul>
<li>Support for the ICON model.</li>
<li>Minor improvements in the documentation.</li>
</ul>
</details>

#### [1.2.1](https://github.com/alcf-lidar/alcf/releases/tag/v1.2.1) (2023-01-30)

<details>
<summary>Release notes</summary>
<ul>
<li>Support for reading Vaisala CL61 data files with zero-dimensional elevation variables.</li>
</ul>
</details>

#### [1.2.0](https://github.com/alcf-lidar/alcf/releases/tag/v1.2.0) (2022-11-22)

<details>
<summary>Release notes</summary>
<ul>
<li>Recursive directory processing options in alcf convert, alcf lidar and alcf model.</li>
<li>Support for double-dash command line delimiter.</li>
<li>cl51: Reading of files with arbitrary time units.</li>
<li>alcf simulate NetCDF matadata.</li>
<li>Improved documentation.</li>
</ul>
</details>

#### [1.1.4](https://github.com/alcf-lidar/alcf/releases/tag/v1.1.4) (2021-12-12)

<details>
<summary>Release notes</summary>
<ul>
<li>Use proleptic Gregorian calendar for time variables.</li>
<li>Include required fonts.</li>
</ul>
</details>

#### [1.1.2](https://github.com/alcf-lidar/alcf/releases/tag/v1.1.2) (2021-11-30)

<details>
<summary>Release notes</summary>
<ul>
<li>Simplified installation by removing a dependency on CMOR.</li>
</ul>
</details>

#### [1.1.0](https://github.com/alcf-lidar/alcf/releases/tag/v1.1.0) (2021-06-29) [[documentation](https://github.com/alcf-lidar/alcf/releases/download/v1.1.0/alcf-doc-1.1.0.zip)] [DOI: [10.5281/zenodo.5153867](https://zenodo.org/record/5153867)]

<details>
<summary>Release notes</summary>
<ul>
<li>Support for Vaisala CL61 and NetCDF files produced by BL-VIEW.</li>
<li>Improved documentation.</li>
</ul>
</details>

#### [1.0.1](https://github.com/alcf-lidar/alcf/releases/tag/v1.0.1) (2021-02-24) [[documentation](https://github.com/alcf-lidar/alcf/releases/download/v1.0.1/alcf-doc-1.0.1.zip)] [DOI: [10.5281/zenodo.5036683](https://doi.org/10.5281/zenodo.5036683)]

<details>
<summary>Release notes</summary>
<ul>
<li>Fixed download links to dependencies (udunits archive was removed upstream).</li>
</ul>
</details>

#### [1.0.0](https://github.com/alcf-lidar/alcf/releases/tag/v1.0.0) (2021-01-02) [[documentation](https://github.com/alcf-lidar/alcf/releases/download/v1.0.0/alcf-doc-1.0.0.zip)] [DOI: [10.5281/zenodo.4411633](https://doi.org/10.5281/zenodo.4411633)]

<details>
<summary>Release notes</summary>
<ul>
<li>First stable release. No change from 1.0.0-beta.3.</li>
</ul>
</details>

#### [1.0.0-beta.3](https://github.com/alcf-lidar/alcf/releases/tag/v1.0.0-beta.3) (2020-10-15) [[documentation](https://github.com/alcf-lidar/alcf/releases/download/v1.0.0-beta.3/alcf-doc-1.0.0-beta.3.zip)] [DOI: [10.5281/zenodo.4088217](https://doi.org/10.5281/zenodo.4088217)]

<details>
<summary>Release notes</summary>
<ul>
<li>alcf lidar option for coupling of observed data with simulated molecular backscatter.</li>
<li>Removal of molecular backscatter in plots (if available).</li>
<li>alcf stats filter option now supports "night" and "day" and passing of multiple arguments.</li>
<li>New lidar type "default" for re-processing of already processed lidar data.</li>
<li>Support for plotting of model cloud liquid water, ice content and cloud fraction.</li>
<li>Calculation of lidar ratio changed to effective lidar ratio.</li>
<li>Backscatter plots now show effective lidar ratio and cloud mask by default.</li>
<li>Changed default vlim for backscatter plots to { 0.1 200 } and default sigma to 5.</li>
<li>Output files names are now without colons, which are not compatible with Windows.</li>
<li>More accurate plot labels.</li>
<li>Improved time sampling: exact profile time bounds are used from weighting.</li>
<li>Improved handling of errors and stopping with Ctrl+C.</li>
<li>Improved NetCDF metadata.</li>
<li>Improved compatibility with newer versions of matplotlib.</li>
<li>Fixed clearing of figures in alcf plot backscatter.</li>
</ul>
</details>

#### [1.0.0-beta.2](https://github.com/alcf-lidar/alcf/releases/tag/v1.0.0-beta.2) (2020-05-01) [[documentation](https://github.com/alcf-lidar/alcf-lidar.github.io/releases/download/v1.0.0-beta.2/alcf-doc-1.0.0-beta.2.zip)] [DOI: [10.5281/zenodo.3779518](https://doi.org/10.5281/zenodo.3779518)]

<details>
<summary>Release notes</summary>
<ul>
<li>Initial beta release.</li>
</ul>
</details>
