import os, json, datetime, time
import sys, subprocess, shutil
from zip_worker import ZipWorker

"""
	Менеджер грабберов
"""

class GrabManager:
	database_dir = "../database" # путь до базы данных
	output_dir = "../database_storage" # путь до архивированной базы данных
	grab_dir = "./grabbers" # директория с грабберами
	local_database_name = "database.zip" # имя архива с бд
	grabbers_info = None # здесь хранится информация о грабберах
	
	def __init__(self):
		"""
			Инифицализация менджера
		"""
		# проверяем наличие директории с базой данных, если нет, создаем
		if not os.path.exists(f"{self.database_dir}"):
			print(f"Create directory {self.database_dir}")
			os.mkdir(self.database_dir)
		# а также файл json для хранения информации о грабберах
		if not os.path.exists(f"{self.database_dir}/index.json"):
			print(f"Create {self.database_dir}/index.json")
			data = {}
			self.save_data(data)
		# пытаемся загрузить информацию о доступных грабберах из json файла
		if not self.load_data():
			return
		
	def save_data(self, data):
		"""
			Сохранение информации о грабберах в json файл
		"""
		with open(f"{self.database_dir}/index.json", "w") as file:
			json.dump(data, file, sort_keys=True, indent=4)
			
	def load_data(self):
		"""
			Загрузка информации о грабберах из json файла
		"""
		try:
			with open(f"{self.database_dir}/index.json", "r") as file:
				self.grabbers_info = json.load(file)
		except:
			print("GrabManager, error with loading grabbers_info")
			return False
		return True
		
	def add_grabber(self, grabber_name, update_days = 1):
		"""
			Добавение нового граббера
		"""
		# проверяем, есть ли уже такой граббер
		if os.path.exists(f"{self.database_dir}/{grabber_name}"):
			print(f"Grabber {grabber_name} exist")
			return
		# создаем директорию для граббера
		self.init_grabber_dir(grabber_name)
		# минимальная дата, обозначающая, что еще не было обновлений
		now = datetime.datetime(1970, 1, 1)
		# сохраняем информацию о граббере
		self.grabbers_info[grabber_name] = {
						"directory": f"{self.database_dir}/{grabber_name}", # его директория
						"file": f"{self.grab_dir}/{grabber_name}.py", # путь до скрипта
						"last_update": f"{now.day}-{now.month}-{now.year} {now.hour}.{now.minute}.{now.second}", # дата обновления
						"update_after_days": update_days # раз в сколько дней обновлять информацию
					}
		# сохраняем граббер в json
		self.save_data(self.grabbers_info)
		
	def init_grabber_dir(self, grabber_name):
		"""
			Инициализация директории граббера
		"""
		os.mkdir(f"{self.database_dir}/{grabber_name}")
		os.mkdir(f"{self.database_dir}/{grabber_name}/pages")
		os.mkdir(f"{self.database_dir}/{grabber_name}/style")
		with open(f"{self.database_dir}/{grabber_name}/style/style.css", "w") as file:
			pass
		
	def need_update_list(self):
		"""
			Получение списка грабберов, от которых требуется обновление
		"""
		self.load_data()
		now = datetime.datetime.now()
		update_list = []
		for name in self.grabbers_info:
			updated = datetime.datetime.strptime(self.grabbers_info[name]["last_update"], "%d-%m-%Y %H.%M.%S")
			need_update_after_days = self.grabbers_info[name]["update_after_days"]
			diff = now - updated
			if diff.days >= need_update_after_days:
				update_list.append(name)
		return update_list
		
	def update(self, update_list):
		"""
			Обновление идентификаторов
		"""
		if len(update_list) == 0:
			print("Nothing update")
			return
		for grab_name in update_list:
			print(f"Updating {grab_name}...")
			command = f"python {self.grab_dir}/{grab_name}.py"
			subprocess.run(command, shell=True)
			now = datetime.datetime.now()
			self.grabbers_info[grab_name]["last_update"] = f"{now.day}-{now.month}-{now.year} {now.hour}.{now.minute}.{now.second}"
			print(f"Updating {grab_name} done")
		self.save_data(self.grabbers_info)
		print(f"Grabber {grabber_name} added")
		print("Create database archive")
		zw = ZipWorker()
		zw.zip_dir(self.database_dir, f"{self.output_dir}/{self.local_database_name}")
		print("Database archive created")
		
	def list(self):
		self.load_data()
		list = []
		for name in self.grabbers_info:
			list.append(name)
		return list
	
	def remove_grabber(self, grab_name):
		"""
			Удаление граббера
		"""
		self.load_data()
		for name in self.grabbers_info:
			if name == grab_name:
				del self.grabbers_info[name]
				shutil.rmtree(f"{self.database_dir}/{name}")
				print(f"Grabber {grab_name} deleted")
				print(self.grabbers_info)
				self.save_data(self.grabbers_info)
				return
		print(f"Can't find {grab_name}")

	def has_ident(self, id_name):
		"""
			Проверка наличия идентификатора в БД
		"""
		self.load_data()
		for grab_name in self.grabbers_info:
			page_path = f"{self.database_dir}/{grab_name}/pages/{id_name}.html"
			print(page_path)
			if not os.path.exists(page_path):
				return (False, None)
			else:
				return (True, page_path)
# команды менеджера
def do_command():
	if len(sys.argv) < 2:
		print("Too few arguments")
		return
	gm = GrabManager()
	command = sys.argv[1]
	if command == "list": # список грабберов
		list = gm.list()
		print(f"{len(list)} grabbers:")
		for name in list:
			print(name)
	elif command == "update": # обновление
		list = gm.need_update_list()
		gm.update(list)
	elif command == "update_list": # список, кому требуется обновление
		list = gm.need_update_list()
		print(f"Need update {len(list)}")
		for val in list:
			print(val)
	elif command == "add": # добавление граббера
		if len(sys.argv) < 3:
			print("Too few arguments")
			return
		gm.add_grabber(sys.argv[2])
	elif command == "del": # удаление граббера
		if len(sys.argv) < 3:
			print("Too few arguments")
			return
		gm.remove_grabber(sys.argv[2])
	else:
		print(f"Unknown command {command}")

if __name__ == "__main__":
	do_command()

