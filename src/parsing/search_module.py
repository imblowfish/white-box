import codecs
import re
from . import directory_parser as dp
from screens.frames.tokenizer.tokenizer import Tokenizer
"""
	Модуль поиска упоминаний идентификатора в файлах проекта
"""

def get_all_pos_in_file(file_path, str):
	"""
		Поиск упоминаний в файле
	"""
	try:
		file = codecs.open(file_path, "r", "utf_8_sig")
	except:
		try:
			file = codecs.open(self.file_path, "r")
		except:
			print(f"Something went wrong with open file {file_path} in search_module")
			return
	lines = []
	try:
		for num, line in enumerate(file):
			tokenizer = Tokenizer()
			t_value = ""
			t_type = None
			i = 0
			while i < len(line):
				t_value += line[i]
				now_type = tokenizer.get_token_type(t_value)
				if not now_type or i+1 == len(line):
					if t_type:
						if i+1 < len(line):
							i -= 1
							t_value = t_value[:-1]
						if t_value == str:
							lines.append((num+1, line))
					t_value = ""
				t_type = now_type
				i+=1
	except:
		return 
	finally:
		file.close()
	return lines
	
def get_all_pos_in_dir(dir_path, str):
	"""
		Поиск упоминаний в директории
	"""
	# получаем дерево директории
	tree = dp.dir_tree(dir_path)
	if not tree:
		return
	pos = {}
	# получаю список файлов в директориии и путь до них
	for node in tree:
		for file in node[2]:
			pos[f"{node[0]}\\{file}"] = {
				"name": file
			}
	delete_keys = []
	# ищу упоминания строки в каждом файле
	for key in pos.keys():
		res = get_all_pos_in_file(key, str)
		pos[key]["lines"] = res
		if not pos[key]["lines"] or len(pos[key]["lines"]) == 0:
			delete_keys.append(key)
	for key in delete_keys:
		del pos[key]
	return pos
		