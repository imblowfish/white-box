# Модуль визуализации проекта
import tkinter as tk
import tkinter.ttk as ttk
from .tree import Tree

# отображение директории
# добавить выбор объекта в treeview
class HierarchyViewer:
	tree = None
	hierarchy = None
	
	def __init__(self):
		self.tree = Tree()
		
	def clear_all(self):
		if self.hierarchy:
			for child in self.hierarchy.get_children():
				self.hierarchy.delete(child)
		
	def get_dir_name(self, dir_name):
		dir_paths = dir_name.split('/')
		if len(dir_name.split('\\')[-1]) < len(dir_paths[-1]):
			dir_paths = dir_name.split('\\')
		for i in range(len(dir_paths)-1, -1, -1):
			dir_name = dir_paths[i].replace('.', '')
			if len(dir_name) > 0:
				return dir_name
		return ""
		
	def get_file_name(self, file_name):
		file_paths = file_name.split('/')
		if len(file_name.split('\\')[-1]) < len(file_paths[-1]):
			file_paths = file_name.split('\\')
		for i in range(len(file_paths)-1, -1, -1):
			if len(file_paths[i]) > 0:
				return file_paths[i]
		return ""
	
	def add_directory(self, dir_name):
		dir_name = self.get_dir_name(dir_name)
		self.tree.add_element(dir_name, "dir")
		
	def add_subdirectory(self, p_dir_name, c_dir_name):
		p_dir_name = self.get_dir_name(p_dir_name)
		c_dir_name = self.get_dir_name(c_dir_name)
		self.tree.add_child_element(p_dir_name, c_dir_name, "dir")
		
	def add_inner_file(self, p_dir_name, file_name):
		p_dir_name = self.get_dir_name(p_dir_name)
		file_name = self.get_file_name(file_name)
		self.tree.add_child_element(p_dir_name, file_name, "file")

	def view(self, parent):
		self.clear_all()
		self.hierarchy = ttk.Treeview(parent)
		self.hierarchy.heading("#0", text="")
		self.draw_nodes(self.tree.root_elements)
		self.hierarchy.pack()

	def draw_nodes(self, nodes, parent=""):
		if not nodes:
			return
		for node in nodes:
			# next_parent = self.hierarchy.insert(parent, "end", text=node.type+":"+node.name, open=True)
			next_parent = self.hierarchy.insert(parent, "end", text=node.name, open=True)
			if not node.child_elements:
				continue
			self.draw_nodes(node.child_elements, next_parent)
			
