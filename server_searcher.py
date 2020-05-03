# проверка наличия нужного идентификатора
import requests
import webbrowser
import os

GLOBAL_SERVER = 0x1
LOCAL_SERVER = 0x2
INTERNET = 0x4

# данные сервера
host = "127.0.0.1"
port = 8080

local_database_path = f"./download/database"

def search_on_server(host, port, id_name):
	if len(id_name) == 0:
		print("id_name len:0")
		return
	try:
		url = f"http://{host}:{port}/{id_name}.html"
		r = requests.get(url=url);
	except:
		print(f"Connection error to http://{host}:{port}/{id_name}.html")
		return False
	if r.status_code != 200:
		return (False, None)
	return (True, None)
	
def search_on_local_database(id_name):
	global local_database_path
	file_name = f"{id_name}.html"
	print(f"search on {local_database_path}")
	for root, dirs, files in os.walk(local_database_path):
		for file in files:
			if file==file_name:
				return (True, os.path.join(root, file))
	return (False, "")

# поиск в сети интернет
def search_on_net(id_name):
	try:
		query = f"https://www.google.com/search?q={id_name}"
		webbrowser.open(query)
	except:
		print(f"Internet search error {id_name}")
		return (False, None)
	return (True, None)
	
def search(id_name):
	global host, port
	print(search_on_local_database(id_name))
	# if search_on_server(host, port, id_name):
		# return "global"
	# elif search_on_local_database(id_name):
		# return "local"
	# else:
		# return "internet"

search("SDL_HINT_ACCELEROMETER_AS_JOYSTICK")
# search_on_net("SDL_HINT_ACCELEROMETER_AS_JOYSTICK")
# result = search("SDL_HINT_ACCELEROMETER_AS_JOYSTICK")
# print(result)	
# res = search_on_server(g_host, g_port, "SDL_HINT_ACCELEROMETER_AS_JOYSTICK")
# print(res)