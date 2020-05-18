"""
	Модуль дерева проекта, строится при отображении иерархии проекта
"""

class Node:
	"""
		Класс узла
	"""
	child_elements = None # дочерние элементы узла
	type = None # тип узла
	name = None # имя
	level = None # уровень в дереве
	is_collapsed = None # будет ли он свернут при отображении в иерархии директории проекта
	def __init__(self, name, type, level=0):
		self.name = name
		self.type = type
		self.level = level
		self.is_collapsed = False
		self.child_elements = []

	def add_child(self, c_name, type):
		self.child_elements.append(Node(c_name, type, self.level+1))
	
class ProjectTree:
	"""
		Класс дерева
	"""
	root_elements = None # корневые элементы
	height = None # высота дерева
		
	def get_name(self, name, type):
		"""
			Получение имени из пути
			Принимает также аргумент type
			Если type dir, то исключает из имени все точки
			В файле такое не происходит, так как точка отделяет имя от расширения
		"""
		# разделяем имя
		splitted = name.split('/')
		# если при разделении обратным слешем длина последнего элемента массива оказалась меньше
		if len(name.split('\\')[-1]) < len(splitted[-1]):
			# делим обратным слешем
			splitted = name.split('\\')
		# с конца проходим элементы разделенной строки
		for i in range(len(splitted)-1, -1, -1):
			# если директория, убираем точки(относительный путь)
			if type == "dir":
				name = splitted[i].replace('.', '')
			# нашли имя, возвращаем
			if len(name) > 0:
				return name
		return ""
		
	def add_element(self, name, type):
		""" 
			Добавление элемента в дерево проекта
			Принимает имя и тип(директория, файл)
		"""
		# получаем имя из пути
		name = self.get_name(name, "dir")
		# иницилазируем корень, если еще не
		if not self.root_elements:
			self.root_elements = []
			self.height = 1
		# если нет элемента в дереве
		if not self.find_element(name, self.root_elements):
			# добавляем к кореню
			self.root_elements.append(Node(name, type))
				
	def add_child_element(self, p_name, c_name, type):
		"""
			Добавление дочернего элемента
		"""
		# получаем имена из путей
		p_name = self.get_name(p_name, "dir")
		c_name = self.get_name(c_name, type)
		# ищем родительский узел
		p_node = self.find_element(p_name, self.root_elements)
		if not p_node:
			return False
		# ищем дочерний узел в родительском
		c_node = self.find_child_in_node(p_node, c_name)
		# если не нашли
		if not c_node:
			# присваиваем дочернему узлу уровень на 1 больше родительского
			child_level = p_node.level + 1
			# добавляем узел
			p_node.add_child(c_name, type)
			# если уровень дочернего узла больше текущей высоты дерева, увеличиваем высоту дерева
			if child_level + 1 > self.height:
				self.height = child_level + 1
		return True
		
	def find_element(self, name, nodes):
		"""
			Поик элемента в дереве
		"""
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
		"""
			Поиск дочернего элемента в узле по имени
		"""
		for child in p_node.child_elements:
			if child.name == child_name:
				return child
		return None
		
	def get_root(self):
		"""
			Список корневых узлов
		"""
		return self.root_elements
		
	def create(self, hierarchy):
		"""
			Создание дерева из кортежа директории list_dir
		"""
		for element in hierarchy:
			directory = element[0]
			self.add_element(directory, "dir")
			subdirs = element[1]
			files = element[2]
			for subdir in subdirs:
				self.add_child_element(directory, subdir, "dir")
			for file in files:
				self.add_child_element(directory, file, "file")