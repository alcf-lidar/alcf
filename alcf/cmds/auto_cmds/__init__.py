from . import model
from . import lidar
from . import compare

CMDS = {
	'model': model.run,
	'lidar': lidar.run,
	'compare': compare.run,
}
