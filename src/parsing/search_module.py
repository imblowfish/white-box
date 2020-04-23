import codecs
import re
from . import directory_worker_main as dw

def get_all_pos_in_file(file_path, str):
	try:
		file = codecs.open(file_path, "r", "utf_8_sig")
	except:
		print(f"Something went wrong with open file {file_path} in search_module")
		return
	content = file.read()
	pos = [m.start() for m in re.finditer(str, content)]
	file.close()
	# print(pos)
	return pos
	
def get_all_pos_in_dir(dir_path, str):
	tree = dw.dir_hierarchy(dir_path)
	if not tree:
		return
	pos = {}
	for node in tree:
		for file in node[2]:
			pos[node[0] + '/' + file] = []
	delete_keys = []
	for key in pos.keys():
		pos[key] = get_all_pos_in_file(key, str)
		if len(pos[key]) == 0:
			delete_keys.append(key)
	for key in delete_keys:
		del pos[key]
	return pos
		