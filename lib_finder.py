# проверка наличия нужного идентификатора
import requests
import webbrowser

GLOBAL_SERVER = 0x1
LOCAL_SERVER = 0x2
INTERNET = 0x4

# данные сервера
g_host = "" # www.hostname.com
g_port = 0 # 8080, 8000 и т.д.

# данные локального сервера
l_host = "127.0.0.1"
l_port = 8080

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
		return False
	return True

# поиск в сети интернет
def search_on_net(id_name):
	try:
		query = f"https://www.google.com/search?q={id_name}"
		webbrowser.open(query)
	except:
		print(f"Internet search error {id_name}")
		return False
	return True
	
def search(id_name):
	global g_host, g_port, l_host, l_port
	if search_on_server(g_host, g_port, id_name):
		return GLOBAL_SERVER
	elif search_on_server(l_host, l_port, id_name):
		return LOCAL_SERVER
	else:
		return INTERNET

search_on_net("SDL_HINT_ACCELEROMETER_AS_JOYSTICK")
# result = search("SDL_HINT_ACCELEROMETER_AS_JOYSTICK")
# print(result)	
# res = search_on_server(g_host, g_port, "SDL_HINT_ACCELEROMETER_AS_JOYSTICK")
# print(res)