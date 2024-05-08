#!/usr/bin/env python3

from setuptools import setup, find_packages, Extension
from setuptools.command.build_py import build_py
import os
import os.path
import subprocess

try:
	import numpy as np
	numpy_include_dirs = [np.get_include()]
except ModuleNotFoundError:
	numpy_include_dirs = []

class BuildCOSP(build_py):
	def run(self):
		subprocess.run('make', cwd='cosp', check=True)
		subprocess.run('make', check=True)
		build_py.run(self)

setup(
	name='alcf',
	version='2.0.1',
	description='Automatic Lidar and Ceilometer Framework (ALCF)',
	author='Peter Kuma, Adrian J. McDonald, Olaf Morgenstern, Richard Querel, Israel Silber, Connor J. Flynn',
	author_email='peter@peterkuma.net',
	license='MIT',
	entry_points={
		'console_scripts': 'alcf = alcf.bin.alcf:main_wrapper',
	},
	packages=find_packages(),
	ext_modules=[
		Extension(
			'alcf.algorithms.interp.area_block',
			['alcf/algorithms/interp/area_block.pyx'],
			include_dirs = numpy_include_dirs,
		),
		Extension(
			'alcf.algorithms.interp.area_linear',
			['alcf/algorithms/interp/area_linear.pyx'],
			include_dirs = numpy_include_dirs,
		),
	],
	zip_safe=False,
	package_data={'alcf': ['cosp_alcf'] + \
		[os.path.join('fonts', x) for x in os.listdir('alcf/fonts')]},
	data_files=[('share/man/man1',
		[os.path.join('man', x) for x in os.listdir('man')])],
	setup_requires=[
		'cython',
		'numpy',
	],
	install_requires=[
		'numpy>=1.24.2',
		'scipy>=1.10.1',
		'matplotlib>=3.7.2',
		'netCDF4>=1.6.4',
		'cl2nc>=3.4.0',
		'mpl2nc>=1.3.6',
		'aquarius-time>=0.4.0',
		'ds-format>=4.1.0',
		'pst-format>=2.0.0',
		'astropy>=5.3.2',
		'cftime>=1.6.2',
		'requests>=2.31.0',
		'cdsapi>=0.7.0',
	],
	keywords=['alc', 'ceilometer', 'lidar', 'atmosphere', 'model', 'simulator', 'nwp', 'gcm', 'cosp', 'actsim', 'vaisala', 'cl51', 'cl31', 'lufft', 'chm-15k', 'minimpl', 'amps', 'merra-2', 'um'],
	url='https://alcf.peterkuma.net',
	classifiers=[
		'Development Status :: 5 - Production/Stable',
		'Environment :: Console',
		'Intended Audience :: Science/Research',
		'License :: OSI Approved :: MIT License',
		'Operating System :: POSIX',
		'Programming Language :: Python :: 3',
		'Programming Language :: Cython',
		'Programming Language :: Fortran',
		'Topic :: Scientific/Engineering :: Atmospheric Science',
		'Topic :: Scientific/Engineering :: Physics',
		'Topic :: Scientific/Engineering :: Visualization',
	],
	cmdclass={
		'build_py': BuildCOSP,
	}
)
