import os
import numpy as np
import ds_format as ds
import aquarius_time as aq
from alcf.algorithms import tsample, zsample
from alcf import misc

VARIABLES = [
	'time',
	'cloud_mask',
	'zfull',
]

def read(d):
	print('<- %s' % d['filename'])
	if d is not None:
		d0 = ds.read(d['filename'], VARIABLES)
		d.update(d0)

def read_stream(dd, state):
	return misc.stream(dd, state, read)

def compare_stream(ddd, state):
	n = len(ddd)
	state['ddd'] = state.get('ddd', [[] for i in range(n)])
	for i in range(n):
		state['ddd'][i] += ddd[i]
	if np.all(np.array([
		len(state['ddd'][i]) > 0
		for i in range(n)
	])):
		for i in range(n):
			time = state['ddd'][i][0]['time']
			t1 = time[0]
	return []

def stream(ddd, state):
	n = len(ddd)
	state['ddd'] = state.get('ddd', [[] for i in range(n)])
	state['read_stream_state'] = state.get('read_stream_state', {})
	state['compare_stream_state'] = state.get('compare_stream_state', {})
	compare_stream([[] for i in range(n)], state['compare_stream_state'])
	for i, dd in enumerate(ddd):
		state['ddd'][i] += dd
	while True:
		for i in range(n):
			if len(state['compare_stream_state']['ddd'][i]) == 0 and \
				len(state['ddd'][i]) > 0:
				dd = [state['ddd'][i][0]]
				state['ddd'][i] = state['ddd'][i][1:]
				dd = read_stream(dd, state['read_stream_state'])
				ddd0 = [[] for j in range(n)]
				ddd0[i] = dd
				dd = compare_stream(ddd0, state['compare_stream_state'])
	return dd

def run(arg1, arg2, arg3, *args):
	'''
alcf-compare -- Calculate comparison statistics from multiple lidar time series.
============

Synopsis
--------

    alcf compare <input_1> <input_2> [<input_n>...] <output>

Arguments
---------

- `input_*`: Input lidar data directory.
- `output`: Output filename.
	'''
	args = [arg1, arg2, arg3] + list(args)
	input_ = args[:-1]
	output = args[-1]

	n = len(input_)
	files = [
		[
			{'filename': os.path.join(dirname, f)}
			for f in sorted(os.listdir(dirname))
			if os.path.isfile(os.path.join(dirname, f))
		]
		for dirname in input_
	]
	state = {}
	stream(files, state)
	dd = stream([[None] for i in range(n)], state)
	print('-> %s' % output)
	#ds.to_netcdf(output, dd[0])
