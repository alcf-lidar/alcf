import numpy as np
from . import area_block
from . import area_linear
from . import linear

INTERP = {
	'default': area_block,
	'area_block': area_block,
	'area_linear': area_linear,
	'linear': linear,
}

def interp(type_, *args):
	try:
		module = INTERP['default' if type_ is None else type_]
	except KeyError:
		raise ValueError('Invalid interpolation method "%s"' % type_)
	return module.interp(*[np.array(x).astype(np.float64) for x in args])
