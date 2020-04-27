class Node:
	child_elements = None
	type = None
	name = None
	level = None
	is_collapsed = None
	def __init__(self, name, type, level=0):
		self.name = name
		self.type = type
		self.level = level
		self.is_collapsed = False
		self.child_elements = []

	def add_child(self, c_name, type):
		self.child_elements.append(Node(c_name, type, self.level+1))
	
class ProjectTree:
	root_elements = None
	height = None
		
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
		
	def add_element(self, name, type):
		name = self.get_name(name, "dir")
		if not self.root_elements:
			self.root_elements = []
			self.height = 1
		if not self.find_element(name, self.root_elements):
			self.root_elements.append(Node(name, type))
				
	def add_child_element(self, p_name, c_name, type):
		p_name = self.get_name(p_name, "dir")
		c_name = self.get_name(c_name, type)
		p_node = self.find_element(p_name, self.root_elements)
		if not p_node:
			return False
		c_node = self.find_child_in_node(p_node, c_name)
		if not c_node:
			child_level = p_node.level + 1
			p_node.add_child(c_name, type)
			if child_level + 1 > self.height:
				self.height = child_level + 1
		return True
		
	def find_element(self, name, nodes):
		if not nodes:
			return None
		for node in nodes:
			if node.name == name:
				return node
			if not node.child_elements:
				continue
			child_res = self.find_element(name, node.child_elements)
			if child_res:
				return child_res
		return None
		
	def find_child_in_node(self, p_node, child_name):
		for child in p_node.child_elements:
			if child.name == child_name:
				return child
		return None
		
	def get_root(self):
		return self.root_elements
		
	def create(self, hierarchy):
		for element in hierarchy:
			directory = element[0]
			self.add_element(directory, "dir")
			subdirs = element[1]
			files = element[2]
			for subdir in subdirs:
				self.add_child_element(directory, subdir, "dir")
			for file in files:
				self.add_child_element(directory, file, "file")