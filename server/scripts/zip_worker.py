import os
from zipfile import ZipFile

"""
	Модуль работы с Zip архивами
"""

class ZipWorker:
	def zip_dir(self, dir_path, zip_path):
		"""
			Архиватор директории, принимает путь до директории и файла архивации,
			по окончанию генерирует по заданному пути zip-архив
		"""
		zip_file = ZipFile(zip_path, "w")
		for root, dirs, files in os.walk(dir_path):
			for file in files:
				zip_file.write(os.path.join(root, file))
		zip_file.close()

	def unzip(self, file_path, unzip_path):
		"""
			Разархивация файла в директорию, принимает путь до zip-файла и путь для разархивации
		"""
		zip_file = ZipFile(file_path, "r")
		zip_file.extractall(unzip_path)
