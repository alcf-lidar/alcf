import convert
import model
import simulate
import lidar
import stats
import compare
import plot
import calibrate

CMDS = {
	'convert': convert.run,
	'model': model.run,
	'simulate': simulate.run,
	'lidar': lidar.run,
	'stats': stats.run,
	'compare': compare.run,
	'plot': plot.run,
	'calibrate': calibrate.run,
}
