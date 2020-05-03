import requests
import os

host = "127.0.0.1"
port = 8080
output_dir = "./download"
database_name = "l_database.7z"
url = f"http://{host}:{port}/{database_name}"

def download_database():
	global output_dir, url
	path = f"{output_dir}/{database_name}"
	req = requests.get(url)
	if req.status_code != 200:
		print(f"Can't load database {url}")
		return
	if not os.path.exists(output_dir):
		os.mkdir(output_dir)
	file = open(path, "wb")
	file.write(req.content)
	file.close()
	# здесь разархивация

# download_database()