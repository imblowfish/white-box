import tkinter as tk
import tkinter.ttk as ttk

from visualization import (
	hierarchy_viewer as hv,
	source_content_viewer as scv
)


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
	def view_hierarchy(self, hierarchy, command):
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
		self.h_viewer.hierarchy.bind("<Button-1>", command)
		
	# получение имени элемента иерархии по тому, на что кликнул пользователь	
	def get_hierarchy_clicked_name(self, event):
		item = self.h_viewer.hierarchy.identify('item', event.x, event.y)
		return self.h_viewer.hierarchy.item(item,"text")
	
	# возможно будет лучше убрать отсюда это, и переместить в core
	def view_file_content(self, path):
		if len(path) == 0:
			return
		source_content_viewer = scv.SourceContentViewer(self.root, path)
		
	def view_file_members(self, members):
		if len(members) == 0:
			return
		source_members_viewer = scv.SourceMembersViewer(self.root, members)
		