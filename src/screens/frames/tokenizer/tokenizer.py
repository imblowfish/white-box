# разбор файла исходного кода
source_path = "../examples/imap/main.cpp"

# проверить на остальных файлах

import re

class Tokenizer:
	# добавить имя файла
	token_types = {
		"id": r"[\_a-zA-Z][\_a-zA-Z0-9]*",
		"comment": r"//?[^\n]*",
		"multiline comment": r"/\*?[^\*]*",
		"num": r"(0[1-8]+)|(0x[a-fA-F]+)|(0b[01]+)|0|([1-9]+[0-9]*)",
		"float_num": r"[0-9]\.[0-9]*",
	}
	keywords = None
	
	def __init__(self):
		self.init_keywords()
		
	def init_keywords(self):
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
		for key, reg in self.token_types.items():
			res = re.match(reg, value)
			if res and (len(value) <= res.end()):
				return key
		return None
	
	def is_keyword(self, word):
		if not self.keywords:
			return None
		return word in self.keywords