import os

# проверка существования пути
def check_path(path):
	return os.path.exists(path)
# получение списка файлов и поддиректорий в директории
def list_in_dir(dir_path):
	return os.listdir(dir_path)
def get_path_to(name, dir):
	tree = dir_hierarchy(dir)
	for item in tree:
		for dir in item[1]:
			if dir == name:
				return item[0]+'/'+name
		for file in item[2]:
			if file == name:
				return item[0]+'/'+name
	return ""
# иерархия директории
def dir_hierarchy(dir_path):
	tree = os.walk(dir_path)
	return tree
def relative_path_to(dir_path):
	if len(dir_path) == 0:
		return None
	app_dir = os.getcwd()
	return os.path.relpath(dir_path, app_dir)