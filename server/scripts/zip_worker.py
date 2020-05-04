import os
from zipfile import ZipFile

class ZipWorker:
	def zip_dir(self, dir_path, zip_path):
		zip_file = ZipFile(zip_path, "w")
		for root, dirs, files in os.walk(dir_path):
			for file in files:
				zip_file.write(os.path.join(root, file))
		zip_file.close()

	def unzip(self, file_path, unzip_path):
		zip_file = ZipFile(file_path, "r")
		zip_file.extractall(unzip_path)
