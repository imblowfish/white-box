import re

"""
	Модуль тоенизатора для поиска идентификаторов, цифр, имен файлов и т.д. в файле
	Используется для подсветки синтаксиса
"""

class Tokenizer:
	"""
		Класс токенизатора
	"""
	# имена токенов и соответсвующие им регулярные выражения
	token_types = {
		"id": r"[\_a-zA-Z][\_a-zA-Z0-9^\.^h]*\.?h?",
		"comment": r"//?[^\n]*",
		"multiline comment": r"/\*?[^\*]*",
		"num": r"(0[1-8]+)|(0x[a-fA-F]+)|(0b[01]+)|0|([1-9]+[0-9]*)",
		"float_num": r"[0-9]\.[0-9]*",
	}
	# список ключевых слов
	keywords = None
	
	def __init__(self):
		self.init_keywords()
		
	def init_keywords(self):
		"""
			Инициализация списка ключевых слов из файла
		"""
		try:
			file = open("./conf/cpp_keywords.txt")
		except:
			print("Tokenizer: Keywords file open error")
			return
		self.keywords = []
		for line in file:
			words = line.split('\n')
			for word in words:
				if len(word.strip()) > 0:
					self.keywords.append(word.strip())
		
	def get_token_type(self, value):
		"""
			Получение типа токена по значению
		"""
		# ищем совпадения по регулярным выражениям типов токена
		for key, reg in self.token_types.items():
			res = re.match(reg, value)
			# если нашли, и длина значения < результата, то возвращаем ключ
			# по факту совпадение есть, но нас оно не устраивает, поэтому делаем такую проверку,
			# чтобы исключить некорректные результат, когда, например abcde по math = ab
			if res and (len(value) <= res.end()):
				return key
		return None
	
	def is_keyword(self, word):
		"""
			Проверка слова по списку ключевых слов
		"""
		if not self.keywords:
			return None
		return word in self.keywords