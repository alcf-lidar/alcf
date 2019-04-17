import convert
import model
import simulate
import lidar
import stats
import compare
import plot
import calibrate
#import plot_stats

CMDS = {
	'convert': convert.run,
	'model': model.run,
	'simulate': simulate.run,
	'lidar': lidar.run,
	'stats': stats.run,
	'compare': compare.run,
	'plot': plot.run,
	'calibrate': calibrate.run,
	#'plot_stats': plot_stats.run,
}
