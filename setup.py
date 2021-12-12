#!/usr/bin/env python3

from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
import os
import os.path
import subprocess

class BuildCOSP(build_py):
	def run(self):
		subprocess.run('make', cwd='cosp', check=True)
		subprocess.run('make', check=True)
		build_py.run(self)

setup(
	name='alcf',
	version='1.1.3',
	description='Automatic Lidar and Ceilometer Framework (ALCF)',
	author='Peter Kuma, Adrian J. McDonald, Olaf Morgenstern, Richard Querel, Israel Silber, Connor J. Flynn',
	author_email='peter@peterkuma.net',
	license='MIT',
	scripts=['bin/alcf'],
	packages=find_packages(),
	zip_safe=False,
	package_data={'alcf': ['cosp_alcf'] + \
		[os.path.join('fonts', x) for x in os.listdir('alcf/fonts')]},
	install_requires=[
		'numpy>=1.16.2',
		'scipy>=1.1.0',
		'matplotlib>=3.0.2',
		'netCDF4>=1.2.9',
		'cl2nc>=3.3.0',
		'aquarius-time>=0.1.0',
		'ds-format>=1.0.0',
		'pst-format>=1.1.1',
		'astropy>=3.1.2',
		'cftime>=1.5.1',
	],
	keywords=['alc', 'ceilometer', 'lidar', 'atmosphere', 'model', 'simulator', 'nwp', 'gcm', 'cosp', 'actsim', 'vaisala', 'cl51', 'cl31', 'lufft', 'chm-15k', 'minimpl', 'amps', 'merra-2', 'um'],
	url='https://alcf-lidar.github.io',
	classifiers=[
		'Development Status :: 5 - Production/Stable',
		'Environment :: Console',
		'Intended Audience :: Science/Research',
		'License :: OSI Approved :: MIT License',
		'Operating System :: POSIX',
		'Programming Language :: Python :: 3',
		'Programming Language :: Fortran',
		'Topic :: Scientific/Engineering :: Atmospheric Science',
		'Topic :: Scientific/Engineering :: Physics',
		'Topic :: Scientific/Engineering :: Visualization',
	],
	cmdclass={
		'build_py': BuildCOSP,
	}
)
