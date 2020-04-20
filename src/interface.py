from visualization import (
	hierarchy_viewer as hv
)
from screens import (
	main_screen
)

class InterfaceManager:
	def __init__(self):
		print("Init main_screen")
		print("Init another screens")
		print("InterfaceManager is created")
	def select_directory(self):
		dir_name = "C:/"
		return dir_name