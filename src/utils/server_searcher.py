# проверка наличия нужного идентификатора
import requests
import webbrowser
import os

class ServerSearcher:
	# данные сервера
	host = "127.0.0.1"
	port = 8080
	local_database_path = f"./database"
	path_for_minibrowser = "../../"
	
	def search_on_server(self, host, port, id_name):
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
		file_name = f"{id_name}.html"
		print(f"search on {self.local_database_path}")
		for root, dirs, files in os.walk(self.local_database_path):
			for file in files:
				if file==file_name:
					return os.path.join(self.path_for_minibrowser+root, file)
		return None
	
	# поиск в сети интернет
	def search_on_net(self, id_name):
		try:
			query = f"https://www.google.com/search?q={id_name}"
			webbrowser.open(query)
		except:
			print(f"Internet search error {id_name}")
			return False
		return True
		
	def search(self, id_name):
		res = self.search_on_local_database(id_name)
		if res:
			return ("local", res)
		res = self.search_on_server(self.host, self.port, id_name)
		if res:
			return ("global", id_name)
		return ("net", id_name)