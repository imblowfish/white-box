import os

class DirectoryWorker:
	app_dir = None
	def __init__(self):
		# получаем текущую директорию
		self.app_dir = os.getcwd()
	# проверка существования пути
	def check_path(self, path):
		return os.path.exists(path)
	# получение списка файлов и поддиректорий в директории
	def list_in_dir(self, dir_path):
		return os.listdir(dir_path)
	def get_path_to(self, name, dir):
		tree = self.dir_hierarchy(dir)
		for item in tree:
			for dir in item[1]:
				if dir == name:
					return item[0]+'/'+name
			for file in item[2]:
				if file == name:
					return item[0]+'/'+name
		return ""
	# иерархия директории
	def dir_hierarchy(self, dir_path):
		tree = os.walk(dir_path)
		# for i in tree:
			# print(i)
		return tree
	def relative_path_to(self, dir_path):
		return os.path.relpath(dir_path, self.app_dir)