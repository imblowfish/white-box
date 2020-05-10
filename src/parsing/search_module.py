import codecs
import re
from . import directory_parser as dp
# import unicode

def get_all_pos_in_file(file_path, str):
	try:
		file = codecs.open(file_path, "r")
	except:
		print(f"Something went wrong with open file {file_path} in search_module")
		return
	lines = []
	line_num = 1
	try:
		for line in file:
			if str in line:
				lines.append((line_num, line))
			line_num += 1
	except:
		return 
	finally:
		file.close()
	return lines
	
def get_all_pos_in_dir(dir_path, str):
	tree = dp.dir_tree(dir_path)
	if not tree:
		return
	pos = {}
	for node in tree:
		for file in node[2]:
			pos[f"{node[0]}\\{file}"] = {
				"name": file
			}
	delete_keys = []
	for key in pos.keys():
		res = get_all_pos_in_file(key, str)
		pos[key]["lines"] = res
		if not pos[key]["lines"] or len(pos[key]["lines"]) == 0:
			delete_keys.append(key)
	for key in delete_keys:
		del pos[key]
	return pos
		