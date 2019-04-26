#!/usr/bin/env python3

from setuptools import setup, find_packages
import os.path

setup(
	name='alcf',
	version='1.0.0',
	description='Command line tool for processing of automatic lidar and ceilometer data and comparison with atmospheric models',
	author='Peter Kuma',
	author_email='peter.kuma@fastmail.com',
	license='MIT',
	scripts=['bin/alcf', 'bin/cosp_alcf'],
	packages=find_packages(),
	zip_safe=False,
	package_data={'alcf': [
		os.path.join('..',p,f)
		for p,_,fs in os.walk('alcf/opt')
	 	for f in fs
	]},
	install_requires=[
		'netCDF4>=1.2.9',
		'cl2nc',
	],
	keywords=['alc', 'ceilometer', 'lidar', 'atmospheric', 'model', 'nwp', 'gcm', 'cosp', 'actsim', 'vaisala', 'cl51', 'cl31', 'lufft', 'chm-15k', 'amsp', 'cmip5'],
	url='https://github.com/peterkuma/alcf',
	classifiers=[
		'Development Status :: 2 - Pre-Alpha',
		'Environment :: Console',
		'Intended Audience :: Science/Research',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 2.7',
		'Topic :: Scientific/Engineering :: Atmospheric Science',
	]
)
