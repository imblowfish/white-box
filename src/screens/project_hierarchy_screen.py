# Модуль визуализации проекта
import tkinter as tk
import tkinter.ttk as ttk
from .tree import Tree

# отображение директории
# добавить выбор объекта в treeview
class ProjectHierarchyScreen:
	tree = None
	hierarchy = None
	
	def __init__(self):
		self.tree = Tree()
		
	def clear_all(self):
		if self.hierarchy:
			for child in self.hierarchy.get_children():
				self.hierarchy.delete(child)
		
	def get_name(self, name, type):
		splitted = name.split('/')
		if len(name.split('\\')[-1]) < len(splitted[-1]):
			splitted = name.split('\\')
		for i in range(len(splitted)-1, -1, -1):
			if type == "dir":
				name = splitted[i].replace('.', '')
			if len(name) > 0:
				return name
		return ""
	
	def add_directory(self, dir_name):
		dir_name = self.get_name(dir_name, "dir")
		self.tree.add_element(dir_name, "dir")
		
	def add_child(self, p_dir_name, c_name, type):
		p_dir_name = self.get_name(p_dir_name, "dir")
		c_name = self.get_name(c_name, type)
		self.tree.add_child_element(p_dir_name, c_name, type)
		
	def add_new_hierarchy(self, hierarchy):
		self.clear_all()
		for element in hierarchy:
			parent_dir = element[0]
			self.add_directory(parent_dir)
			subdirs = element[1]
			files = element[2]
			for subdir in subdirs:
				self.add_child(parent_dir, subdir, "dir")
			for file in files:
				self.add_child(parent_dir, file, "file")
		self.view()

	def view(self):
		self.root = tk.Tk()
		self.hierarchy = ttk.Treeview(self.root)
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
			
