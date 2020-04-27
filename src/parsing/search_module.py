import codecs
import re
from . import directory_parser as dp

def get_all_pos_in_file(file_path, str):
	try:
		file = codecs.open(file_path, "r", "utf_8_sig")
	except:
		print(f"Something went wrong with open file {file_path} in search_module")
		return
	lines = []
	line_num = 0
	for line in file:
		if str in line:
			lines.append(line_num)
		line_num += 1
	# content = file.read()
	# pos = [m.start() for m in re.finditer(str, content)]
	file.close()
	return lines
	
def get_all_pos_in_dir(dir_path, str):
	tree = dp.get_dir_tree(dir_path)
	if not tree:
		return
	pos = {}
	for node in tree:
		for file in node[2]:
			pos[node[0] + '\\' + file] = []
	delete_keys = []
	for key in pos.keys():
		pos[key] = get_all_pos_in_file(key, str)
		if len(pos[key]) == 0:
			delete_keys.append(key)
	for key in delete_keys:
		del pos[key]
	return pos
		