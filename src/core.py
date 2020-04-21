import tkinter as tk
from tkinter import filedialog

from analyzer import Analyzer
from parsing import directory_worker_main as dw
from screens.main_screen import MainScreen

class Core:
	main_screen = None
	analyzer = None
	dir_worker = None
	def __init__(self):
		self.analyzer = Analyzer()
		self.dir_worker = dw.DirectoryWorker()
		self.show_main_screen()
		self.open_project()
		self.main_screen.view()
		
	def show_main_screen(self):
		if self.main_screen:
			del self.main_screen
		self.main_screen = MainScreen()
		self.main_screen.init_menu(self.menu_callback)
		# self.main_screen.view()
		
	def menu_callback(self, menu):
		label = menu.entrycget(0, "label")
		# проход по вариантам label и вызов нужной функции
		if label == "Open Project":
			self.open_project()
		
	def open_project(self):
		# получение пути до директории проекта
		# project_dir = self.dir_worker.relative_path_to( tk.filedialog.askdirectory() )
		project_dir = "../examples/imap"
		# разбор проекта и получение таблицы идентификаторов
		self.analyzer.parse_project(project_dir)
		# отображение иерархии проекта
		self.main_screen.view_hierarchy( self.dir_worker.dir_hierarchy(project_dir) )
		# отображение тестового содержимого файла
		
		# отображение абстракций языка в файле
