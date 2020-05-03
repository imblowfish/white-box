from zipfile import ZipFile
import os

def zip_dir(dir_path, zip_path):
	zip_file = ZipFile(zip_path, "w")
	for root, dirs, files in os.walk(dir_path):
		for file in files:
			zip_file.write(os.path.join(root, file))
	zip_file.close()

def unzip(file_name, unzip_path):
	zip_file = ZipFile(file_path, "r")
	zip_file.extractall(unzip_path)
