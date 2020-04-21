import tkinter as tk
import tkinter.ttk as ttk

from visualization import hierarchy_viewer as hv


class MainScreen:
	root = None
	menus = None
	menu_bar = None
	def __init__(self):
		self.root = tk.Tk()
		self.root.geometry("800x600")
		self.root.title("WhiteBox")
		self.h_viewer = hv.HierarchyViewer()
	def view(self):
		self.root.mainloop()

	def init_menu(self, command):
		self.menu_bar = tk.Menu(self.root)
		self.root["menu"] = self.menu_bar
		# File
		file_menu = tk.Menu(self.menu_bar, tearoff=0)
		self.menu_bar.add_cascade(label="File", menu=file_menu)
		# File commands
		file_menu.add_command(label="Open Project", command = lambda: command(file_menu))
		
	#отображение иерархии проекта	
	def view_hierarchy(self, hierarchy):
		for element in hierarchy:
			parent_dir = element[0]
			self.h_viewer.add_directory(parent_dir)
			subdirs = element[1]
			files = element[2]
			for subdir in subdirs:
				self.h_viewer.add_subdirectory(parent_dir, subdir)
			for file in files:
				self.h_viewer.add_inner_file(parent_dir, file)
		self.h_viewer.view(self.root)