from analyzer import AnalysisManager

from visualization import (
	hierarchy_viewer as hv
)
from screens.main_screen import MainScreen

class Core:
	main_screen = None
	
	def __init__(self):
		self.main_screen = MainScreen()
		print("InterfaceManager is created")
	def start(self):
		self.main_screen.start()
	def select_directory(self):
		dir_name = "C:/"
		return dir_name