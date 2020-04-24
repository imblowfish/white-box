'''
	Модуль парсеров xml вывода doxygen
'''

import xml.etree.ElementTree as et

# базовый класс для парсеров вывода xml doxygen
class BaseXMLParser:
	doxy_table = None #ссылка на таблицу файлов doxygen
	id_table = None #ссылка на таблицу идентификаторов
	
	#--------------------------------
	def __init__(self, doxy_table, id_table_ref):
		
		#создаем ссылки на таблицы
		self.doxy_table = doxy_table
		self.id_table = id_table_ref
	#--------------------
	def __del__(self):
		#удаляем все ссылки на таблицы
		self.doxy_table = None 
		self.id_table = None
	#--------------------------
	def parse(self, file_path): # разбор xml-файла
		#получаем структуру xml файла
		try:
			tree = et.parse(file_path)
		except:
			print(f"BaseXMLParser: Something went wrong with parsing {file_path}")
			return
		#получаем корень
		self.root = tree.getroot()
		#начинаем разбор с корня
		self.parse_xml_node(self.root)
		# print(f"BaseXMLParser: {file_path} success parsing")
	#-------------------------------------
	def node_has_attrib(self, node, tags): # проверка, содержит ли узел xml атрибут
		# если параметр список атрибутов
		if type(tags) is list:
			# проверяем по каждому
			for tag in tags:
				if tag not in node.attrib.keys():
					return False
		else:
			# иначе, проверяем один атрибут
			if tags not in node.attrib.keys():
				return False
		return True
	#------------------------------
	def parse_xml_node(self, node): # виртуальная функций разбора узла, перегружается в наследниках
		pass
#---BaseXMLParser END---

# парсер файла index.xml вывода doxygen	
class IndexParser(BaseXMLParser):
	#------------------------------
	def parse_xml_node(self, node): # перегруженная функция разбора узла
		# просматриваем каждый дочерний элемент узла
		for child in node:
			# нужная информация хранится в элементах с тегом compound, иначе пропускаем узел
			if child.tag != "compound": 
				continue
			# проверяем, хранится ли в узле информация о виде и ссылка на файл doxygen
			if not self.node_has_attrib(child, ["kind", "refid"]):
				continue
			# узнаем имя, вид и ссылку
			name = child.find("name").text
			kind = child.attrib["kind"]
			doxy_ref = child.attrib["refid"]
			# игнорируем директории, т.к. в них хранится только информация
			# о содержимом директории, это будем узнавать позже без doxygen
			if kind == "dir":
				continue
			# добавляем запись о файле в таблицу файлов doxygen
			self.doxy_table.add_record(name, kind, doxy_ref)
			# добавляем запись в таблицу идентификаторов
			self.id_table.add_record(name, kind)		
#---IndexParser END---		

# парсер файлов xml связанных с исходными файлами проекта
class SourceFileParser(BaseXMLParser):
	now_file = None # текущий разбираемый файл
	
	#---------------
	def parse(self): # перегруженная функция разбора
		# получаем список файлов из таблицы doxygen
		files = self.doxy_table.get_records_by_kind("file")
		# разбираем каждый файл
		for self.now_file in files:
			super().parse(self.now_file.ref)
		# удаляем ссылку на файл
		self.now_file = None
	#------------------------------
	def parse_xml_node(self, node):
		# получаем список включаемых файлов текущего файла
		includes = node[0].findall("includes")
		# получаем список членов файла
		members = node[0].findall("sectiondef")
		# members = node[0].findall("memberdef")
		# получаем список классов файла
		inner_classes = node[0].findall("innerclass")
		# получаем идентификатор файла в таблице идентификаторов
		file_id = self.id_table.get_id_by_name(self.now_file.name)
		# добавляем включаемые файлы как родителей записи текущего файла
		for include_file in includes:
			self.id_table.add_parent(file_id, include_file.text, "file")
		# добавляем классы как члены записи текущего файла
		for inner_class in inner_classes:
			self.id_table.add_member(file_id, inner_class.text, "class")
		# разбираем остальных членов файла
		self.parse_members(file_id, members)
	#---------------------------------
	def parse_members(self, parent_id, nodes): # разбор членов файла
		for node in nodes:
			# получаем имя и вид
			name = node[0].find("name").text
			kind = node.attrib["kind"]
			type = node[0].find("type")
			# не у каждого элемента есть тип
			if type is not None:
				type = type.text
			# если не функция, то информации об имени и виде нам хватит
			if kind != "func":
				# добавляем запись, как члена файла
				self.id_table.add_member(parent_id, name, kind, type)
				# если вид записи enum, значит нужно еще узнать значения
				if kind != "enum":
					continue
			# если функция
			if kind == "func":
				# иначе, получаем тип и аргументы
				type = node[0].find("type").text
				args = node[0].find("argsstring").text
				kind = "function"
				# добавляем запись, как члена файла
				self.id_table.add_member(parent_id, name, kind, type, args)
			else:
				# если enum, получаем id записи enum
				enum_id = self.id_table.get_id_by_name(name)
				# получаем список узлов со значениями enum
				enum_values = node[0].findall("enumvalue")
				# проходим каждое
				for enum_value in enum_values:
					value = enum_value.find("name").text
					# и добавляем
					self.id_table.add_member(enum_id, value, "enum_value")
#---SourceFileParser END---

# парсер xml файлов классов проекта
class ClassParser(BaseXMLParser):
	now_class = None # текущий разбираемый файл класса
	
	#---------------
	def parse(self):
		# аналогично разбору файлов разбираем каждый файл класса
		classes = self.doxy_table.get_records_by_kind("class")
		for self.now_class in classes:
			super().parse(self.now_class.ref)
		self.now_class = None
	#------------------------------
	def parse_xml_node(self, node):
		# получаем список классов класса
		inner_classes = node[0].findall("innerclass")
		# родителей класса
		base_classes = node[0].findall("basecompounddef")
		# и членов класса
		members = node[0].findall("sectiondef")
		# узнаем идентификатор записи класса в таблице идентификаторов
		class_id = self.id_table.get_id_by_name(self.now_class.name)
		# добавляем классы класса, как члены текущего класса
		for inner_class in inner_classes:
			self.id_table.add_member(class_id, inner_class.text, "class")
		# добавляем родительские классы текущего класса
		for base_class in base_classes:
			self.id_table.add_base(class_id, base_class.text, "class")
		# разбор членов класса
		self.parse_members(class_id, members)
	#-----------------------------------------
	def parse_members(self, parent_id, nodes): # разбор членов класса
		# проходим по каждому узлу
		for node in nodes:
			# обычно kind членов группирует все члены и выглядит как 'kind-(private/public/protected)',
			# например, все пирватные функции будут храниться в private-func
			# берем то, что до '-', и узнаем вид
			pos = node.attrib["kind"].find('-')
			# берем то, что после '-' и узнаем модификатор доступа
			modif = node.attrib["kind"][0:pos]
			# проходим по всем дочерним узлам группы членов
			for child in node:
				# узнаем вид, нельзя брать то, что было в группе членов, т.к., например, private-attrib 
				# содержит как переменные, так и множества и т.д.
				kind = child.attrib["kind"]
				# дальше все аналогично SourceFileParser
				name = child.find("name").text
				type = child.find("type")
				if type is not None:
					type = type.text
				if kind != "function":
					self.id_table.add_member(parent_id, name, kind, type, None, modif)
					if kind != "enum":
						continue
				if kind == "function":
					args = child.find("argsstring").text
					self.id_table.add_member(parent_id, name, kind, type, args, modif)
				else:
					enum_id = self.id_table.get_id_by_name(name)
					enum_values = child.findall("enumvalue")
					for enum_value in enum_values:
						value = enum_value.find("name").text
						self.id_table.add_member(enum_id, value, "enum_value")
#---ClassParser END---