import convert
import resample
import model
import simulate
import lidar
import stats
import plot
import plot_stats

CMDS = {
	'convert': convert.run,
	'resample': resample.run,
	'model': model.run,
	'simulate': simulate.run,
	'lidar': lidar.run,
	'stats': stats.run,
	'plot': plot.run,
	'plot_stats': plot_stats.run,
}
