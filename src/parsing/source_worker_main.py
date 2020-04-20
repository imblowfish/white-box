# разбор файла исходного кода
source_path = "../examples/imap/main.cpp"

# проверить на остальных файлах

import re

class Tokenizer:
	token_types = {
		"PREPROC": r"#\S*",
		"SYMBOL": r"'[\w\s]*'",
		"STRING": r"\"[^\"]*\"*",
		"COMMENT": r"//?[\w\s]*",
		"MULTILINE COMMENT": r"/\**[\w\s]*\*?/?",
		"FIXED_NUM": r"(0[1-8]+)|(0x[a-fA-F]+)|(0b[01]+)|0|([1-9]+[0-9]*)",
		"FLOAT_NUM": r"[0-9]\.[0-9]*",
		"IDENTIFIER": r"[\_a-zA-Z.][\_a-zA-Z0-9.]*",
	}
	keywords = None
	
	def __init__(self):
		self.init_keywords()
		
	def init_keywords(self):
		try:
			file = open("./keywords.txt")
		except:
			print("Tokenizer: Keywords file open error")
			return
		self.keywords = []
		for line in file:
			words = line.split(',')
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
		return word in self.keywords
			
			
# tokenizer = Tokenizer()
# file = open("../examples/imap/main.cpp")

# value = ""
# token_type = None
# for line in file:
	# i = 0
	# while True:
		# if i >= len(line):
			# break
		# else:
			# value += line[i]
		# res = tokenizer.get_token_type(value)
		# if not res:
			# if token_type:
				# value = value[:-1]
				# if tokenizer.is_keyword(value):
					# token_type = "KEYWORD"
				# print(f"[{token_type}]{value}", end='')
				# i-=1
			# else:
				# print(value, end='')
			# value = ""
		# token_type = res
		# i+=1
		
# file.close()