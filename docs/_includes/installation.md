## Installation

Below you can find installation instructions for supported operating systems:

* [Linux](#linux) (recommended)
* [Windows](#windows) with the Windows Subsystem for Linux (Ubuntu)
* [macOS](#macos)

You can also [build the ALCF from the source code](#building-from-the-source-code)
if you want to modify any of its parts.

### Linux

The instructions below assume that you enter the commands in the terminal.

1. Install required programs and libraries:

    On Debian-based Linux distributions (Ubuntu, Debian, Devuan, ...), install
    dependencies with:

    ```sh
    sudo apt install gcc make gfortran libhdf5-dev libnetcdf-dev \
        libnetcdff-dev python3 python3-setuptools python3-pip
    ```

    On Fedora, install dependencies with:

    ```sh
    sudo yum install make gcc gfortran hdf5-devel netcdf-devel \
        netcdf-fortran-devel python3-setuptools python3-pip
    ```

2. Install the ALCF with:

    ```sh
    # To install globally:
    sudo pip3 install alcf --upgrade

    # To install in the user's home directory
    # (make sure "$HOME/.local/bin" is in the PATH environment variable):
    pip3 install alcf --upgrade --user
    ```

### Windows

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

The installation has been tested on macOS Monterey Intel. Installation on Apple
M1 may be possible but is untested.

1. Install [Anaconda](https://anaconda.org).

2. Install [MacPorts](https://www.macports.org).

3. Install required MacPorts packages:

    ```sh
    sudo port install gcc11 hdf5 netcdf netcdf-fortran
    sudo port select --set gcc mp-gcc11
    ```

4. Install the ALCF with:

    ```sh
    pip install alcf
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

### Building from the source code

If you want to build the ALCF from the source code, run the following commands
in the source code directory:

```sh
./download_cosp
pip3 install .
# Replace "pip3" with "pip" if you are using Anaconda.
```

This will download and unpack [ALCF-COSP](https://github.com/alcf-lidar/alcf-cosp)
(a version of COSP with support for ground-based lidars), and compile and
install the ALCF. Use this option if you want to customise any parts of the
ALCF.

You can also use the following command to continusly change code and have
changes applied in the alcf command without re-installing:

```sh
python3 setup.py develop
# Replace "python3" with "python" if you are using Anaconda.
```

## Releases

Below is a list of releases of the ALCF. The version numbers follow
the [Semantic Versioning](https://semver.org). Installation instructions
have been changing with versions. Please follow the installation instructions
in the documentation of the particular version.

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
