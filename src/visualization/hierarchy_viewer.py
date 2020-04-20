# Модуль визуализации проекта

import tkinter as tk
from math import *
# добавить отображение директорий, поддиректорий и файлов в директориях

class Node:
	child_elements = None
	type = None
	name = None
	level = None
	is_collapsed = None
	def __init__(self, name, type, level):
		self.name = name
		self.type = type
		self.level = level
		self.is_collapsed = False
		self.child_elements = []

	def add_child(self, c_name, type):
		self.child_elements.append(Node(c_name, type, self.level+1))
	
class Tree:
	root_elements = None
	height = None
	
	def __init__(self):
		pass
		
	def add_element(self, element_name, type):
		if not self.root_elements:
			self.root_elements = []
			self.height = 1
		if self.find_element(element_name, self.root_elements):
			print("Элемент уже добавлен в дерево")
			return
		self.root_elements.append(Node(element_name, type, 0))
		
	def add_child_element(self, p_name, c_name, type):
		p_node = self.find_element(p_name, self.root_elements)
		if not p_node:
			return False
		c_node = self.find_child_in_node(p_node, c_name)
		if not c_node:
			child_level = p_node.level + 1
			p_node.add_child(c_name, type)
			if child_level + 1 > self.height:
				self.height = child_level + 1
		else:
			print("Дочерний элемент уже добавлен")
		return True
		
	def find_element(self, name, nodes):
		if not nodes:
			return None
		for node in nodes:
			if node.name == name:
				return node
			if not node.child_elements:
				continue
			for child in node.child_elements:
				child_res = self.find_element(name, child)
				if not child_res:
					return child_res
		return None
		
	def find_child_in_node(self, p_node, child_name):
		for child in p_node.child_elements:
			if child.name == child_name:
				return child
		return None
		
	def get_root(self):
		return self.root_elements

	
# отображение директории
class DirectoryScreen:
	tree = None
	scale = None
	width = None
	height = None
	
	def __init__(self):
		self.tree = Tree()
		
	def clear_all(self):
		pass
		
	def get_dir_name(self, dir_name):
		dir_paths = dir_name.split('/')
		if len(dir_name.split('\\')) > len(dir_paths):
			dir_paths = dir_name.split('\\')
		for i in range(len(dir_paths)-1, -1, -1):
			dir_name = dir_paths[i].replace('.', '')
			if len(dir_name) > 0:
				return dir_name
		return ""
		
	def get_file_name(self, file_name):
		file_paths = file_name.split('/')
		if len(file_name.split('\\')) > len(file_paths):
			file_paths = file_name.split('\\')
		for i in range(len(file_paths)-1, -1, -1):
			if len(file_paths[i]) > 0:
				return file_paths[i]
		return ""
	
	def add_directory(self, dir_name):
		# получение имени директории
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

	def draw(self):
		self.root = tk.Tk()
		# создание canvas
		self.scale = 1
		self.width = 500
		self.height = 500
		self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="white")
		# добавление событий мыши элементам canvas
		self.draw_tree()
		# отображение узлов дерева со связями
		print("Отображаю директорию")
		self.canvas.pack()
		self.root.mainloop()

	def draw_tree(self):
		self.draw_nodes(self.tree.root_elements)
		
	def draw_nodes(self, nodes, level=0):
		if not nodes:
			return
		for node in nodes:
			if node.type == "dir":
				print("Draw directory")
				# dir_w = self.width/100 * 10 * self.scale
				# dir_h = self.height/100 * 10 * self.scale
				# start_x = self.width/2 - dir_w * self.tree.height
				# start_y = 10
				# w_space = 10
				# h_space = 10
				# x1 = start_x + w_space * level + dir_w * level
				# y1 = start_y + h_space * level + dir_h * level
				# self.canvas.create_rectangle(x1, y1, x1+dir_w, y1+dir_h)
				# if not node.child_elements or node.is_collapsed:
					# continue
				# self.draw_nodes(node.child_elements, level+1)
			elif node.type == "file":
				print("Draw file")
				
		
	
# ds = DirectoryScreen()
# ds.add_directory("/aaa")
# ds.add_subdirectory("/aaa", "/aaa/bbb")
# ds.add_subdirectory("/aaa", "/aaa/ccc")
# ds.add_inner_file("/aaa", "/aaa/text.txt")
# ds.draw()











# canvas_objects = []
# old_x = 0
# old_y = 0

# root = tk.Tk()
# canvas = tk.Canvas(root, width=500, height=500)
		
# def canv_move_y(event):
	# for object in canvas_objects:
		# canvas.move(object, 0, event.delta/10)


# canvas.bind("<B1-Motion>", canv_move)
# canvas.bind("<MouseWheel>", canv_move_y)

# for i in range(0, 100):
	# obj_width = 10
	# obj_height = 10
	# w_space = 10
	# h_space = 10
	# x1 = obj_width * i + w_space
	# y1 = obj_height * i + h_space * i
	# canvas_objects.append( canvas.create_rectangle(x1, y1, x1 + obj_width, y1 + obj_height) )


# canvas.pack()
# root.mainloop()

# главный экран
class MainScreen:
	root = None
	canvas = None
	
	def __init__(self):
		self.root = tk.Tk()
		self.root.geometry("500x500")
		self.canvas = tk.Canvas(self.root, width=500, height=500, bg="grey")
		self.canvas.pack()
	def start(self):
		self.root.mainloop()
	
	def view_directories(self, directories):
		dir_screen = DirectoryScreen()
		for dir in directories:
			dir_name = dir[0]
			dir_screen.add_directory(dir_name)
			# print(f"Имя директории {dir_name}")
			subdirs = dir[1]
			inner_files = dir[2]
		# root_dir = directory_contents[0]
		# subdirs = directory_contents[1]
		# innerfiles = directory_contents[2]
		# print(f"Корень:{root_dir}")
		# print(f"Поддиректории:{subdirs}")
		# print(f"Файлы директории:{innerfiles}")
		# 
		# for subdir in subdirs:
			# dir_screen.add_subdirectory(root_dir, subdir)
		# for file in innerfiles:
			# dir_screen.add_innerfile(root_dir, file)


# ms = MainScreen()
# directories = [
	# ("./examples", ["./examples/src", "./examples/git"], ["log.txt"]),
	# ("./examples/src", ["./examples/src/include"], ["main.cpp"]),
	# ("./examples/git", ["./examples/git/1231239834y8734y875y32", "./examples/git/99999239834y8734y875y32", "./examples/git/411239834y8734y3231242"], [".gitignore"]),
	# ("./examples/src/include", [], ["header1.h", "header2.h", "header1.h", "fuheAqwerfsd.h"])
# ]
# ms.view_directories(directories)
# ms.start()