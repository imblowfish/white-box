'''
	Модуль работы с таблицей идентификаторов
'''

from copy import deepcopy

# класс записи таблицы идентификаторов
class IDTableRecord:
	id = None # идентификатор записи
	name = None # имя записи
	kind = None # вид записи
	type = None # ее тип
	args = None # аргументы
	modifier = None # модификатор доступа
	parents_id = None # идентификаторы родительских записей
	members_id = None # идентификаторы членов записи
	bases_id = None # идентификаторы базовых классов(для классов)
	inheritors_id = None # массив наследников класса
	
	def __init__(self, id, name, kind, type=None, args=None, modifier=None): # конструктор записи 
		self.id = id
		self.name = name
		self.kind = kind
		self.type = type
		self.args = args
		self.modifier = modifier

	def add_parent(self, parent_id): # добавление родителя к записи
		# если еще не был создан массив родительских идентификаторов
		if not self.parents_id:
			self.parents_id = []
		# проверяем, был ли уже добавлен такой родительский идентификатор
		for id in self.parents_id:
			if id == parent_id:
				return
		# если не был, добавляем новый идентификатор
		self.parents_id.append(parent_id)

	def add_member(self, member_id): # добавление нового члена идентификатора
		# все аналогично предыдущей функции
		if not self.members_id:
			self.members_id = []
		for id in self.members_id:
			if id == member_id:
				return
		self.members_id.append(member_id)

	def add_base(self, base_id): # добавление базового класса
		# аналогично предыдущей функции
		if not self.bases:
			self.bases = []
		for id in self.bases_id:
			if id == base_id:
				return
		self.bases.append(base_id)

	def add_inheritor(self, inheritor_id): # добавление наследника класса
		# аналогично предыдущей функции
		if not self.inheritors:
			self.inheritors = []
		for id in self.inheritors:
			if id == inheritor_id:
				return
		self.inheritors.append(inheritor_id)
		
	def __str__(self):
		info = ""
		if self.kind:
			info += self.kind + ' '
		if self.modifier:
			info += self.modifier + ' '
		if self.type:
			info += self.type + ' '
		info += self.name
		if self.args:
			info += self.args
		return info

# класс таблицы идентификаторов
class IDTable:
	now_id = None # текущий id
	records = None # массив записей таблицы идентификаторов
	
	def __init__(self):
		self.records = [] # создаем массив записей
		self.now_id = 0 # обнуляем текущий id

	def __del__(self):
		self.records = None # удаляем массив записей
		self.now_id = None # удаляем текущий id
		
	def empty(self):
		if len(self.records) == 0:
			return True
		return False

	def add_record(self, name, kind, type=None, args=None, modifier=None): # добавление записи в таблицу
		self.records.append( IDTableRecord(self.now_id, name, kind, type, args, modifier) )
		self.now_id += 1

	def add_parent(self, record_id, parent_name, parent_kind): # добавление родителя записи
		# ищем запись, в которой добавляем родителя
		record = self.get_record_by_id(record_id) 
		# ищем запись, которая будет родительской
		parent_record = self.get_record_by_name_and_kind(parent_name, parent_kind) 
		# если родительская отсутствует
		if not parent_record: 
			# добавляем ее
			self.add_record(parent_name, parent_kind)
			parent_record = self.get_record_by_name_and_kind(parent_name, parent_kind)
		if record:
			# добавляем родителя записи
			record.add_parent(parent_record.id)
			# добавляем запись родителю в члены
			parent_record.add_member(record.id)

	def add_base(self, record_id, base_name, base_type): # добавление базового класса
		# работа аналогична предыдущей функции
		record = self.get_record_by_id(record_id)
		base_record = self.get_record_by_name(base_name)
		if not base_record:
			self.add_record(base_name, base_type)
			base_record = self.get_record_by_name(base_name)
		if record:
			record.add_base(base_record.id)
			base_record.add_inheritor(record.id)

	def add_member(self, parent_id, c_name, c_kind, c_type=None, c_args=None, c_modif=None): # добавление члена текущей записи
		parent_record = self.get_record_by_id(parent_id)
		child_record = self.get_record_by_name_and_kind(c_name, c_kind)
		if not child_record:
			self.add_record(c_name, c_kind, c_type, c_args, c_modif)
			child_record = self.get_record_by_name_and_kind(c_name, c_kind)
		if parent_record:
			child_record.add_parent(parent_record.id)
			parent_record.add_member(child_record.id)

	def get_record_by_id(self, id, copy=False): # получение записи по идентификатору
		if id < 0:
			return None
		for record in self.records:
			if record.id == id:
				if copy:
					return deepcopy(record)
				return record
		return None

	def get_record_by_name(self, name, copy=False): # по имени
		for record in self.records:
			if record.name == name:
				if copy:
					return deepcopy(record)
				return record
		return None

	def get_record_by_name_and_kind(self, name, kind, copy=False):
		for record in self.records:
			if record.name == name and record.kind == kind:
				if copy:
					return deepcopy(record)
				return record
		return None

	def get_id_by_name(self, name): # получение идентификатора по имени
		for record in self.records:
			if record.name == name:
				return record.id
		return -1
		
	def has_record_in_file(self, file, name):
		record = self.get_record_by_name_and_kind(file, "file")
		if not record:
			return False
		return self.search_child_in_record(record, name)
	
	def search_child_in_record(self, record, name):
		if not record.members_id:
			return False
		for id in record.members_id:
			member = self.get_record_by_id(id)
			if member.name == name or self.search_child_in_record(member, name):
				return True
		return False
		
	def has_record(self, name):
		for record in self.records:
			if record.name == name:
				return True
		return False

	def print_all(self): # вывод таблицы идентификаторов
		for record in self.records:
			print(record.id, record.kind, 
				  record.name, record.type, 
				  record.args, record.parents_id,
				  record.members_id,
				  record.inheritors_id)

	def get_members_by_name(self, p_name):
		members = []
		parent_id = self.get_id_by_name(p_name)
		for record in self.records:
			if not record.parents_id:
				continue
			for id in record.parents_id:
				if id == parent_id:
					members.append(deepcopy(record))
		return members

	def get_records(self):
		return deepcopy(self.records)