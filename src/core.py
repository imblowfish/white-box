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
			
	def hierarchy_callback(self, event):
		# получение имени объекта, по которому был клик
		name = self.main_screen.get_hierarchy_clicked_name(event)
		# name = 
		type = self.id_table.get_kind_by_name(name)
		if len(type) == 0:
			return
		# получение пути до файла
		path = self.dir_worker.get_path_to(name, self.project_dir)
		# self.main_screen.view_file_content(path)
		members = self.id_table.get_members_by_parent_name(name)
		
		# сделать визуальное отображение функции в случае клика
		self.main_screen.view_file_members(members)
		
		
		# отображение зависимостей файла
		
		
		# print(path_to_file)
		# отображение членов файла
		# self.main_screen.view_file_content(path_to_file)
		# self.main_screen.view_file_members()
		# парсинг содержимого файла
		
	def open_project(self):
		self.id_table = None
		# получение пути до директории проекта
		# project_dir = self.dir_worker.relative_path_to( tk.filedialog.askdirectory() )
		self.project_dir = "../examples/imap/"
		# разбор проекта и получение таблицы идентификаторов
		self.id_table = self.analyzer.get_id_table(self.project_dir)
		# отображение иерархии проекта
		self.main_screen.view_hierarchy( self.dir_worker.dir_hierarchy(self.project_dir), self.hierarchy_callback )
