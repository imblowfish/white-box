import tkinter as tk
from tkinter import filedialog

from analyzer import Analyzer
from parsing import directory_worker_main as dw
from screens.main_screen import MainScreen
from screens.project_hierarchy_screen import ProjectHierarchyScreen
from screens.file_viewer_screen import FileViewerScreen
from screens.members_viewer_screen import MembersViewerScreen
from screens.id_table_info_screen import IdTableInfoScreen
from screens.connection_graph_screen import ConnectionGraphScreen
from screens.source_modules_screen import SourceModulesScreen

# при клике на имя открывается не только информация о членах, но и граф зависимости, где отображается связь с родителями
# также, при клике на файл, отображается информация

class Core:
	project_dir = None
	analyzer = None
	id_table = None
	# окна
	main_screen = None
	project_hierarchy_screen = None
	file_viewer_screen = None
	members_viewer_screen = None
	id_table_info_screen = None
	connection_graph_screen = None
	source_modules_screen = None
	
	def __init__(self):
		self.analyzer = Analyzer() #инициализация анализатора
		self.init_main_screen()	#инициализация главного окна
		self.init_project_hierarchy_screen() #инициализация окна иерархии
		self.init_file_viewer_screen()
		self.init_members_viewer_screen()
		self.init_id_table_info_screen()
		self.init_connection_graph_screen()
		self.init_source_modules_screen()
		
		# для теста
		self.project_dir = "../examples/imap"
		self.open_project_command(None)
		# self.show_hierarchy_command()
		self.main_screen.view()
		
	# ИНИЦИАЛИЗАЦИЯ ОКОН	
	def init_main_screen(self):
		self.main_screen = MainScreen()
		self.main_screen.open_proj.bind("<Button-1>", self.open_project_command)
		self.main_screen.show_hierarchy.bind("<Button-1>", self.show_hierarchy_command)
		
	def init_project_hierarchy_screen(self):
		self.project_hierarchy_screen = ProjectHierarchyScreen()
	
	def init_file_viewer_screen(self):
		self.file_viewer_screen = FileViewerScreen()
		
	def init_members_viewer_screen(self):
		self.members_viewer_screen = MembersViewerScreen()
	
	def init_id_table_info_screen(self):
		self.id_table_info_screen = IdTableInfoScreen()
	
	def init_connection_graph_screen(self):
		self.connection_graph_screen = ConnectionGraphScreen()
	
	def init_source_modules_screen(self):
		self.source_modules_screen = SourceModulesScreen()
	
	# КОМАНДЫ
	def open_project_command(self, event):
		# self.project_dir = dw.relative_path_to( tk.filedialog.askdirectory() )
		self.project_dir = "../examples/imap"
		if not self.project_dir:
			print("Empty path")
			return
		self.id_table = self.analyzer.get_id_table(self.project_dir)
		# тестирование графа зависимостей для всего проекта
		
		# self.connection_graph_screen.show_project_connections(self.id_table.get_records(), self.id_table)
		
		self.show_hierarchy_command()
		
	def show_hierarchy_command(self, event = None): #event здесь только для вида
		# отображение иерархии проекта
		dir_hierarchy = dw.dir_hierarchy(self.project_dir)
		self.project_hierarchy_screen.add_new_hierarchy(dir_hierarchy)
		self.project_hierarchy_screen.hierarchy.bind("<Button-1>", self.project_hierarchy_screen_click)
		
	def project_hierarchy_screen_click(self, event):
		# определение имени объекта, по которому нажали
		item = self.project_hierarchy_screen.hierarchy.identify('item', event.x, event.y)
		name = self.project_hierarchy_screen.hierarchy.item(item, "text")
		if len(name) == 0:
			return
		kind = self.id_table.get_kind_by_name(name)
		if not kind:
			print("not kind")
			return
		path_to_file = dw.get_path_to(name, self.project_dir)
		members = self.id_table.get_members_by_name(name)
		
		# self.connection_graph_screen.show_record_connections(name, self.id_table)
		
		# отображение файла и вывод информации о нем
		self.file_viewer_screen.show(path_to_file, self.id_table, self.file_viewer_click, self.selection_file_viewer)
		# self.members_viewer_screen.show(members, self.members_viewer_click)
			
	def file_viewer_click(self, event, tag):
		name = self.file_viewer_screen.get_word_under_mouse(event, tag)
		
		self.connection_graph_screen.show_record_connections(name, self.id_table)
		
		# self.id_table_info_screen.show_info(name, self.id_table)
		# получение информации по имени из таблицы идентификаторов и вывод ее на экран
		
	def selection_file_viewer(self, event):
		text = self.file_viewer_screen.text.selection_get()
		self.source_modules_screen.add_in_module(text)
	
	def members_viewer_click(self, event):
		item = self.members_viewer_screen.members.identify('item', event.x, event.y)
		name = self.members_viewer_screen.members.item(item, "text")
		# self.id_table_info_screen.show_info(name, self.id_table)
		self.connection_graph_screen.show_record_connections(name, self.id_table)
		# получение информации по имени из таблицы идентификаторов и вывод ее на экран
		
	# def menu_callback(self, menu):
		# label = menu.entrycget(0, "label")
		# проход по вариантам label и вызов нужной функции
		# if label == "Open Project":
			# self.open_project()
			
