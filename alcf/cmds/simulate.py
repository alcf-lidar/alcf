import os
import copy
import tempfile
from warnings import warn
from string import Template
import subprocess
import ds_format as ds
import alcf
from alcf import misc
from alcf.lidars import LIDARS

VARS = [
	'lon',
	'lat',
	'time',
	'time_bnds',
	'ps',
	'orog',
	'zfull',
	'ta',
	'pfull',
	'clw',
	'cli',
	'cl',
]

CONFIG_TEMPLATE = """
&config_nml
	config%NPOINTS_IT=500,
	config%NCOLUMNS=${ncolumns},
	config%NLEVELS=${nlevels},
	config%USE_VGRID=.true.,
	config%NLR=40,
	config%CSAT_VGRID=.true.,
	config%RADAR_FREQ=94.0,
	config%SURFACE_RADAR=0,
	config%use_mie_tables=0,
	config%use_gas_abs=1,
	config%do_ray=0,
	config%melt_lay=0,
	config%k2=-1,
	config%use_reff=.true.,
	config%use_precipitation_fluxes=.false.,
	config%Nprmts_max_hydro=12,
	config%Naero=1,
	config%Nprmts_max_aero=1,
	config%lidar_ice_type=0,
	config%lidar_wavelength=${wavelength},
	config%lidar_max_range=${max_range},
	config%surface_lidar=${surface_lidar},
	config%OVERLAP=${overlap},
	config%ISCCP_TOPHEIGHT=1,
	config%ISCCP_TOPHEIGHT_DIRECTION=2,
	config%Platform=1,
	config%Satellite=15,
	config%Instrument=0,
	config%Nchannels=8,
	config%Channels=1,3,5,6,8,10,11,13,
	config%Surfem=0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,
	config%ZenAng=50.0,
	config%CO2=5.241e-04,
	config%CH4=9.139e-07,
	config%N2O=4.665e-07,
	config%CO=2.098e-07,
	config%output%Lradar_sim=.false.,
	config%output%Llidar_sim=.true.,
	config%output%Lisccp_sim=.false.,
	config%output%Lmisr_sim=.false.,
	config%output%Lmodis_sim=.false.,
	config%output%Lrttov_sim=.false.,
	config%output%Ltoffset=.true.,
	config%output%Lcfaddbze94=.false.,
	config%output%Ldbze94=.false.,
	config%output%Latb532=.false.,
	config%output%LcfadLidarsr532=.false.,
	config%output%Lclcalipso=.false.,
	config%output%Lclhcalipso=.false.,
	config%output%Lcllcalipso=.false.,
	config%output%Lclmcalipso=.false.,
	config%output%Lcltcalipso=.false.,
	config%output%LparasolRefl=.false.,
	config%output%Lclcalipsoliq=.false.,
	config%output%Lclcalipsoice=.false.,
	config%output%Lclcalipsoun=.false.,
	config%output%Lclcalipsotmp=.false.,
	config%output%Lclcalipsotmpliq=.false.,
	config%output%Lclcalipsotmpice=.false.,
	config%output%Lclcalipsotmpun=.false.,
	config%output%Lclhcalipsoliq=.false.,
	config%output%Lcllcalipsoliq=.false.,
	config%output%Lclmcalipsoliq=.false.,
	config%output%Lcltcalipsoliq=.false.,
	config%output%Lclhcalipsoice=.false.,
	config%output%Lcllcalipsoice=.false.,
	config%output%Lclmcalipsoice=.false.,
	config%output%Lcltcalipsoice=.false.,
	config%output%Lclhcalipsoun=.false.,
	config%output%Lcllcalipsoun=.false.,
	config%output%Lclmcalipsoun=.false.,
	config%output%Lcltcalipsoun=.false.,
	config%output%Lalbisccp=.false.,
	config%output%Lboxptopisccp=.false.,
	config%output%Lboxtauisccp=.false.,
	config%output%Lpctisccp=.false.,
	config%output%Lclisccp=.false.,
	config%output%Ltauisccp=.false.,
	config%output%Lcltisccp=.false.,
	config%output%Lmeantbisccp=.false.,
	config%output%Lmeantbclrisccp=.false.,
	config%output%LclMISR=.false.,
	config%output%Lclcalipso2=.false.,
	config%output%Lcltlidarradar=.false.,
	config%output%Lfracout=.false.,
	config%output%LlidarBetaMol532=.false.,
	config%output%Lcltmodis=.true.,
	config%output%Lclwmodis=.true.,
	config%output%Lclimodis=.true.,
	config%output%Lclhmodis=.true.,
	config%output%Lclmmodis=.true.,
	config%output%Lcllmodis=.true.,
	config%output%Ltautmodis=.true.,
	config%output%Ltauwmodis=.true.,
	config%output%Ltauimodis=.true.,
	config%output%Ltautlogmodis=.true.,
	config%output%Ltauwlogmodis=.true.,
	config%output%Ltauilogmodis=.true.,
	config%output%Lreffclwmodis=.true.,
	config%output%Lreffclimodis=.true.,
	config%output%Lpctmodis=.true.,
	config%output%Llwpmodis=.true.,
	config%output%Liwpmodis=.true.,
	config%output%Lclmodis=.true.,
	config%output%Lcrimodis=.true.,
	config%output%Lcrlmodis=.true.,
	config%output%Ltbrttov=.false.,
/
"""

OVERLAP = {
	'maximum': 1,
	'random': 2,
	'maximum-random': 3,
}

def cosp_alcf(config, input_, output):
	_, config_filename = tempfile.mkstemp('.nml', prefix='alcf_config_', text=False)
	try:
		with open(config_filename, 'w') as f:
			f.write(config)
		program = os.path.join(os.path.dirname(__file__), '../cosp_alcf')
		subprocess.call([program, config_filename, input_, output])
	finally:
		os.unlink(config_filename)

def run(type_, input_, output,
	ncolumns=10,
	overlap='maximum-random',
	debug=False,
	**kwargs
):
	'''
alcf-simulate -- Simulate lidar measurements from model data using COSP.
=============

Synopsis
--------

    alcf simulate <type> [<options>] [--] <input> <output>

Description
-----------

Arguments following `--` are treated as literal strings. Use this delimiter if the input or output file names might otherwise be interpreted as non-strings, e.g. purely numerical file names.

Arguments
---------

- `type`: Type of lidar to simulate.
- `input`: Input filename or directory (the output of "alcf model").
- `output`: Output filename or directory.
- `options`: See Options below.

Types
-----

- `caliop`: CALIPSO/CALIOP.
- `chm15k`: Lufft CHM 15k.
- `cl31`: Vaisala CL31.
- `cl51`: Vaisala CL51.
- `cl61`: Vaisala CL61.
- `mpl`: Sigma Space MiniMPL.

Options
-------

- `ncolumns: <ncolumns>`: Number of SCOPS subcolumns to generate. Default: `10`.
- `overlap: <overlap>`: Cloud overlap assumption in the SCOPS subcolumn generator. `maximum` for maximum overlap, `random` for random overlap, or `maximum-random` for maximum-random overlap. Default: `maximum-random`.

Examples
--------

Simulate a Vaisala CL51 instrument from model data in `alcf_merra2_model` previously extracted using `alcf model` and store the output in the direcctory `alcf_merra2_simulate`.

    alcf simulate cl51 alcf_merra2_model alcf_merra2_simulate
	'''
	lidar = LIDARS.get(type_)
	if lidar is None:
		raise ValueError('Invalid type: %s' % type_)

	overlap_flag = OVERLAP.get(overlap)
	if overlap_flag is None:
		raise ValueError('Invalid overlap: %s' % overlap)

	nlevels = 60

	template = Template(CONFIG_TEMPLATE)
	config = template.substitute(
		ncolumns=ncolumns,
		nlevels=nlevels,
		overlap=overlap_flag,
		wavelength=lidar.WAVELENGTH,
		max_range=lidar.MAX_RANGE,
		surface_lidar=(1 if lidar.SURFACE_LIDAR else 0),
	)

	if os.path.isfile(input_):
		print('<- %s' % input_)
		cosp_alcf(config, input_, output)
	else:
		files = sorted(os.listdir(input_))
		for file_ in files:
			input_filename = os.path.join(input_, file_)
			output_filename = os.path.join(output, file_)
			if not os.path.isfile(input_filename):
				continue
			print('<- %s' % input_filename)
			try:
				d = ds.read(input_filename, VARS)
				misc.require_vars(d, VARS)
			except Exception as e:
				if debug: warn('%s: %s' % (file_, traceback.format_exc()))
				else: warn('%s: %s' % (file_, str(e)))
				continue
			cosp_alcf(config, input_filename, output_filename)
			print('<- %s' % output_filename)
			d = ds.read(output_filename)
			d['.']['.'] = alcf.META
			ds.write(output_filename, d)
			print('-> %s' % output_filename)
