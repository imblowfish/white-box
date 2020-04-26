'''
	Корневой модуль проекта, через который осуществляется управление
	его работой
'''

import tkinter as tk
from screens.windows import (
	MainWindow
)
from whitebox_core_commands import WhiteBoxCommands

# Класс корня проекта
class WhiteBoxCore(WhiteBoxCommands):
	project_directory = None # рабочая директория текущего проекта
	id_table = None # таблица идентификаторов проекта
	main_win = None # главное окно приложения
	
	#------------------
	def __init__(self): # конструктор
		print("WhiteBoxCore init")
		# инициализация главного окна
		self.main_win= MainWindow()
		# меню
		self.init_menu()
		# привязка команд
		self.bind_commands()
		# запуск главного окна
		self.main_win.start()
	#-------------------
	def init_menu(self): # инициализация меню главного окна
		# создание меню
		self.main_win.menu_bar = tk.Menu(self.main_win.master)
		self.main_win.master["menu"] = self.main_win.menu_bar
		# создание пунктов меню
		self.main_win.open_menu = tk.Menu(self.main_win.menu_bar, tearoff = 0)
		self.main_win.menu_bar.add_cascade(label="File", menu=self.main_win.open_menu)
		self.main_win.open_menu.add_command(label="Open project", command=lambda: self.open_project(None))
	#-----------------------
	def bind_commands(self): # связывание окон и фреймов с командами
		tree = self.main_win.hierarchy_frame.tree_widget
		tree.bind("<Double-Button-1>", self.hierarchy_click)
		tree = self.main_win.file_info_frame.info_tree
		tree.bind("<Double-Button-1>", self.file_info_click)
#---WhiteBoxCore---
	