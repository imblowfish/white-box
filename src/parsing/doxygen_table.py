'''
	Модуль работы с таблицей файлов doxygen
'''

from copy import deepcopy

"""
	Модуль для хранения файлов, директорий, классов и другой необходимой информации при
	разборе doxygen-файла
"""

class DoxyTableRecord:
	"""
		класс записи таблицы файлов doxygen
	"""
	name = None
	kind = None
	ref = None
	def __init__(self, name, kind, ref):
		self.name = name
		self.kind = kind
		self.ref = ref

class DoxyTable:
	"""
		класс таблицы записей
	"""
	path_to_doc = None # путь к сгенерированной doxygen документации
	records = None # записи таблицы

	def __init__(self, path_to_doc):
		# устанавливаем путь к директории с документацией
		self.path_to_doc = path_to_doc 
		# если путь не заканчивается на символ '/' , добавляем
		if self.path_to_doc[-1] != '/':
			self.path_to_doc += '/'
		# создаем массив записей
		self.records = []

	def __del__(self):
		self.records = None
		self.path_to_doc = None

	def add_record(self, name, kind, ref):
		"""
			добавление записи в таблицу
		"""
		self.records.append( DoxyTableRecord(name, kind, self.path_to_doc+ref+".xml") )

	def get_records(self):
		"""
			получение всех записей таблицы
		"""
		return deepcopy(self.records)

	def get_record_by_name(self, name):
		"""
			получение записи по имени
		"""
		for record in self.records:
			if record.name == name:
				return deepcopy(record)
		return None

	def get_record_by_id(self, id):
		"""
			по идентификатору
		"""
		for record in self.records:
			if record.ref == id:
				return deepcopy(record)
		return None

	def get_records_by_kind(self, kind):
		"""
			по виду
		"""
		records_by_type = []
		for record in self.records:
			if record.kind == kind:
				records_by_type.append(deepcopy(record))
		return records_by_type	