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
	# иерархия директории
	def dir_hierarchy(self, dir_path):
		tree = os.walk(dir_path)
		# for i in tree:
			# print(i)
		return tree
	# получение относительного пути до директории относительно директории приложения
	def relative_path_to(self, dir_path):
		return os.path.relpath(dir_path, self.app_dir)

# элемент иерархии(файл, директория, и т.д.)
def HierarchyElement:
	pass

# класс хранения иерархии
def ProjectHierarchy:
	root = None
	
	
	def __init__(self):
		pass
	
# класс для работы с проектом
class ProjectWorker:
	dir_worker = None
	project_path = None
	hierarchy = None
	
	def __init__(self):
		self.dir_worker = DirectoryWorker()
		
	def open_project(self, project_path):
		self.hierarchy = None
		# получение относительного пути до проекта
		self.project_path = self.dir_worker.relative_path_to(project_path)
		tree = self.dir_worker.dir_hierarchy(self.project_path)
		
	
p_w = ProjectWorker()
project_path = "C:\\Users\\Юрий\\Desktop\\InDev\\examples\\imap"
p_w.open_project(project_path)