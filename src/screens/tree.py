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
	
class Tree:
	root_elements = None
	height = None
	
	def __init__(self):
		pass
		
	def add_element(self, element_name, type):
		if not self.root_elements:
			self.root_elements = []
			self.height = 1
		if not self.find_element(element_name, self.root_elements):
			# print(f"Add :{element_name}: in tree")
			# print(self.find_element(element_name, self.root_elements))
			self.root_elements.append(Node(element_name, type))
				
	def add_child_element(self, p_name, c_name, type):
		p_node = self.find_element(p_name, self.root_elements)
		if not p_node:
			return False
		c_node = self.find_child_in_node(p_node, c_name)
		if not c_node:
			# print(f"Add child :{c_name}: to :{p_name}:")
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