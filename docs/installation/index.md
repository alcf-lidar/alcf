---
title: Installation
layout: default
---

## Installation

ALCF is written in Python and Fortran. Installation on Linux is recommended.
Installation on other operating systems may be possible and planned in the
future, but is not described here at the moment.

### Linux

The installation has been tested on Debian GNU/Linux 10 (buster).

Install the following required software:

- [PGI compiler](https://www.pgroup.com/products/community.htm)
- Python 3 (usually pre-installed on Linux distributions)

Once you have installed PGI, make sure the command `pgf95` works in the console.

Download and unpack the [latest ALCF version](https://github.com/peterkuma/alcf/archive/master.zip),
and run commands below in the unpacked directory.

To download and build dependencies
([UDUNITS](https://www.unidata.ucar.edu/software/udunits/),
[NetCDF](https://www.unidata.ucar.edu/software/netcdf/),
[NetCDF-Fortran](https://www.unidata.ucar.edu/software/netcdf/docs-fortran/),
[OSSP uuid](http://www.ossp.org/pkg/lib/uuid/),
[HDF5](https://www.hdfgroup.org/solutions/hdf5),
[CMOR](https://pcmdi.github.io/cmor-site/),
[COSP](https://github.com/peterkuma/COSPv1)):

```sh
./download_dep
./build_dep
make
```

**Note:** ALCF uses the Python libraries [ds-python](https://github.com/peterkuma/ds-python),
[aquarius-time](https://github.com/peterkuma/aquarius-time) and
[pst](https://github.com/peterkuma/pst), which are installed with the commands
below.

To install in system directories:

```sh
pip3 install https://github.com/peterkuma/ds-python/archive/master.zip \
    https://github.com/peterkuma/aquarius-time/archive/master.zip \
    https://github.com/peterkuma/pst/archive/master.zip \
python3 setup.py install
```

To install in user directories (make sure `~/.local/bin` is in the environmental variable `PATH`):

```sh
pip3 install --user https://github.com/peterkuma/ds-python/archive/master.zip \
    https://github.com/peterkuma/aquarius-time/archive/master.zip \
    https://github.com/peterkuma/pst/archive/master.zip \
python3 setup.py install --user
```

You should now be able to run ALCF in the terminal:

```sh
alcf
```

should output:

```
{% include cmd_main.md %}
```
