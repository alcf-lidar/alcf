#!/usr/bin/env python3

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

import os
import sys
import pst
from alcf.cmds import main

def main_wrapper():
	args, kwargs = pst.decode_argv(sys.argv, as_unicode=True)
	ret = main.run(*args[1:], **kwargs)
	sys.exit(ret)

if __name__ == '__main__':
	main_wrapper()
