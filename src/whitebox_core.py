'''
	Корневой модуль проекта, через который осуществляется управление
	его работой
'''

import tkinter as tk
from screens.windows import MainWindow
from whitebox_core_commands import WhiteBoxCommands
from utils.server_searcher import ServerSearcher

# Класс корня проекта
class WhiteBoxCore(WhiteBoxCommands):
	project_directory = None # рабочая директория текущего проекта
	id_table = None # таблица идентификаторов проекта
	main_win = None # главное окно приложения
	
	def __init__(self): # конструктор
		# инициализация главного окна
		self.main_win= MainWindow()
		# меню
		self.init_menu()
		self.main_win.log("Menu inited")
		# привязка команд
		self.bind_commands()
		self.main_win.log("Commands binded")
		self.main_win.log("WhiteBoxCore init")
		self.main_win.log("Start MainWindow")
		# запуск главного окна
		self.main_win.start()

	def init_menu(self): # инициализация меню главного окна
		# создание меню
		self.main_win.menu_bar = tk.Menu(self.main_win.master)
		self.main_win.master["menu"] = self.main_win.menu_bar
		# создание пунктов меню
		self.main_win.open_menu = tk.Menu(self.main_win.menu_bar, tearoff = 0)
		self.main_win.database_menu = tk.Menu(self.main_win.menu_bar, tearoff = 0)
		self.main_win.settings_menu = tk.Menu(self.main_win.menu_bar, tearoff = 0)
		
		self.main_win.menu_bar.add_cascade(label="File", menu=self.main_win.open_menu)
		self.main_win.menu_bar.add_cascade(label="Database", menu=self.main_win.database_menu)
		self.main_win.menu_bar.add_command(label="Modules...", command=self.main_win.text_in_module_adding)
		
		self.main_win.open_menu.add_command(label="Open project", command=lambda: self.open_project_click(None))
		self.main_win.open_menu.add_command(label="Open file", command=lambda: self.open_file_click(None))
		
		self.main_win.database_menu.add_command(label="Search ID..", command=lambda: self.main_win.search_id(ServerSearcher(), self.run_html_viewer))
		self.main_win.database_menu.add_command(label="Download database", command=self.download_database)

	def bind_commands(self): # связывание окон и фреймов с командами
		tree = self.main_win.hierarchy_frame.tree_widget
		tree.bind("<Double-Button-1>", self.hierarchy_click)
		tree = self.main_win.file_info_frame.info_tree
		tree.bind("<Double-Button-1>", self.file_info_click)
		notebook = self.main_win.files_frame.notebook
		notebook.bind("<Button-1>", lambda e: self.files_tab_click(e))
		self.main_win.file_dependency_frame.zoom_btn.bind("<Button-1>", self.maximize_file_dependencies)

	