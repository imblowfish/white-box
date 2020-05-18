import requests
import webbrowser
import os

class ServerSearcher:
	"""
		Класс поиска идентификатора в лок. БД, на сервере, вызова браузера с запросом
	"""
	# данные сервера
	host = "127.0.0.1"
	port = 8080
	local_database_path = f"./database" # путь до локальной БД
	path_for_minibrowser = "../../" # путь до минибраузера
	
	def __init__(self):
		self.set_host_and_port()
				
	def set_host_and_port(self):
		"""
			Установка хоста и порта по файлу настроек
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
		file.close()
		
	def search_on_server(self, host, port, id_name):
		"""
			Поиск на сервере
		"""
		if len(id_name) == 0:
			print("id_name len:0")
			return None
		try:
			url = f"http://{host}:{port}/{id_name}.html"
			r = requests.get(url=url);
		except:
			print(f"Connection error to http://{host}:{port}/{id_name}.html")
			return None
		if r.status_code != 200:
			return None
		return True
		
	def search_on_local_database(self, id_name):
		"""
			Поиск в локальной БД
		"""
		file_name = f"{id_name}.html"
		print(f"search on {self.local_database_path}")
		for root, dirs, files in os.walk(self.local_database_path):
			for file in files:
				if file==file_name:
					return os.path.join(self.path_for_minibrowser+root, file)
		return None
	
	def open_in_browser(self, id_name):
		"""
			поиск в сети интернет
		"""
		try:
			query = f"https://www.google.com/search?q={id_name}"
			webbrowser.open(query)
		except:
			print(f"Internet search error {id_name}")
			return False
		return True
		
	def search_id(self, id_name):
		"""
			Поиск идентификатора
		"""
		# сперва ищем в лок. БД
		res = self.search_on_local_database(id_name)
		if res:
			return ("local", res)
		# затем на сервере
		res = self.search_on_server(self.host, self.port, id_name)
		if res:
			return ("global", id_name)
		# иначе есть возможность получить информацию только через интернет
		return ("net", id_name)