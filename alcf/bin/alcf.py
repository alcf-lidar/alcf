#!/usr/bin/env python3

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

import os
import sys
import pst
import warnings
from alcf.cmds import main


def main_wrapper():
	args, kwargs = pst.decode_argv(sys.argv, as_unicode=True)

	def formatwarning(message, category, filename, lineno, line=None):
		if 'debug' in kwargs:
			s = 'Warning: %s (line %d): %s\n' % (filename, lineno, message)
			if line is not None: s += line + '\n'
			return s
		else:
			return 'Warning: %s\n%s\n' % (message, 'Use --debug for more information')
	warnings.simplefilter('always')

	# Restore warning blocking done by NumPy:
	#
	# Filter out Cython harmless warnings
	# https://github.com/numpy/numpy/blob/c31e59993874f0f3b2dfce24df3bd910b44a632d/numpy/__init__.py#L320
	warnings.filterwarnings('ignore', message='numpy.dtype size changed')
	warnings.filterwarnings('ignore', message='numpy.ufunc size changed')
	warnings.filterwarnings('ignore', message='numpy.ndarray size changed')

	warnings.formatwarning = formatwarning

	try:
		ret = main.run(*args[1:], **kwargs)
		sys.exit(ret)
	except Exception as e:
		if 'debug' in kwargs:
			raise e
		else:
			print('Error: ' + str(e), file=sys.stderr)
			print('Use --debug for more information', file=sys.stderr)

if __name__ == '__main__':
	main_wrapper()
