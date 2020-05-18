import requests
import os
from .zip_worker import ZipWorker

"""
	Модуль загрузки архивированной базы данных с сервера
"""

class DatabaseDownloader:
	# host = "127.0.0.1"
	# port = 8080
	output_dir = "."
	database_name = "database.zip"
	# url = f"http://{host}:{port}/{database_name}"
	
	def __init__(self):
		self.set_host_and_port()
		
	def set_host_and_port(self):
		"""
			Установка хоста и порта по значениям в файле настроек
		"""
		try:
			file = open("./conf/settings", "r")
		except:
			print("Can't find settings file")
			return
		for line in file:
			if line.find("host") >= 0:
				self.host = line.split('=')[-1][:-1]
			elif line.find("port") >= 0:
				self.port = int(line.split('=')[-1])
		self.url = f"http://{self.host}:{self.port}/{self.database_name}"
		file.close()
	
	def download(self, unzip=False):
		"""
			Загрузка базы данных
		"""
		path = f"{self.output_dir}/{self.database_name}"
		try:
			req = requests.get(self.url, stream=True)
		except:
			return (False, "Connetion error")
		if req.status_code != 200:
			print(f"Can't load database {self.url}")
			return (False, req.status_code)
		try:
			f = open(path, "wb")
		except:
			return (False, "Create database file error")
		for chunk in req.iter_content(chunk_size=1024):
			f.write(chunk)
		f.close()
		if unzip:
			zw = ZipWorker()
			zw.unzip(path, self.output_dir)
			os.remove(path)
		return (True, req.status_code)