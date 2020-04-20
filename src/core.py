# корень всей системы, через который осуществляется управление всем остальным

from analyzer import AnalysisManager
from interface import InterfaceManager

class Core:
	analyzer = None # модуль анализа кода
	interface = None # модуль работы с интерфейсом
	
	def __init__(self):
		self.analyzer = AnalysisManager()
		self.interface = InterfaceManager()
		print("Core is created")
	def __del__(self):
		self.analyzer = None
		self.interface = None
		print("Core is deleted")