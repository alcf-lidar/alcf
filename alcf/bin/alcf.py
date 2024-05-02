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
