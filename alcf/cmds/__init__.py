from . import convert
from . import model
from . import simulate
from . import lidar
from . import stats
from . import compare
from . import plot
from . import calibrate
from . import auto

CMDS = {
	'convert': convert.run,
	'model': model.run,
	'simulate': simulate.run,
	'lidar': lidar.run,
	'stats': stats.run,
	'compare': compare.run,
	'plot': plot.run,
	'calibrate': calibrate.run,
	'auto': auto.run,
}
