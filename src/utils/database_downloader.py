import requests
import os
from .zip_worker import ZipWorker

class DatabaseDownloader:
	host = "127.0.0.1"
	port = 8080
	output_dir = "."
	database_name = "database.zip"
	url = f"http://{host}:{port}/{database_name}"
	
	def download(self, unzip=False):
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
		# try:
			# path = f"{self.output_dir}/{self.database_name}"
			# req = requests.get(self.url)
		# except:
			# return (False, "Connetion error")
		# if req.status_code != 200:
			# print(f"Can't load database {self.url}")
			# return (False, req.status_code)
		# if not os.path.exists(self.output_dir):
			# os.mkdir(self.output_dir)
		# file = open(path, "wb")
		# file.write(req.content)
		# file.close()
		# if unzip:
			# zw = ZipWorker()
			# zw.unzip(path, self.output_dir)
			# os.remove(path)
		# return (True, req.status_code)