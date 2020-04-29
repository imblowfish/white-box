import os
import json
import datetime
import time

class GrabManager:
	dir = "./database"
	grab_dir = "./grabbers"
	grabbers_info = None
	
	def __init__(self):
		if not os.path.exists(f"{self.dir}"):
			os.mkdir(self.dir)
		if not os.path.exists(f"{self.dir}/index.json"):
			data = {}
			self.save_data(data)
		self.load_data()
		
	def save_data(self, data):
		with open(f"{self.dir}/index.json", "w") as file:
			json.dump(data, file, sort_keys=True, indent=4)
			
	def load_data(self):
		with open(f"{self.dir}/index.json", "r") as file:
			self.grabbers_info = json.load(file)
		print("Data loaded")
		
	def add_grabber(self, grabber_name, update_days = 1):
		if os.path.exists(f"{self.dir}/{grabber_name}"):
			print(f"Grabber {grabber_name} exist")
			return
		self.init_grabber_dir(grabber_name)
		now = datetime.datetime.now()
		self.grabbers_info[grabber_name] = {
						"directory": f"{self.dir}/{grabber_name}",
						"file": f"{self.grab_dir}/{grabber_name}.py",
						"last_update": f"{now.day}-{now.month}-{now.year} {now.hour}.{now.minute}.{now.second}",
						"update_after_days": update_days
					}
		self.save_data(self.grabbers_info)
		print(f"Grabber {grabber_name} added")
		
	def init_grabber_dir(self, grabber_name):
		os.mkdir(f"{self.dir}/{grabber_name}")
		os.mkdir(f"{self.dir}/{grabber_name}/pages")
		
	def need_update_list(self):
		if not self.grabbers_info:
			self.load_data()
		now = datetime.datetime.now()
		update_list = []
		for name in self.grabbers_info:
			updated = datetime.datetime.strptime(self.grabbers_info[name]["last_update"], "%d-%m-%Y %H.%M.%S")
			need_update_after_days = self.grabbers_info[name]["update_after_days"]
			diff = now - updated
			if diff.days >= need_update_after_days:
				update_list.append(name)
				print(f"Need update {name}")
		return update_list
		
	def update(self, update_list):
		print("Start update")
		pass
		print("End update")
		
gm = GrabManager()
# list = gm.need_update_list()
# gm.update(list)
gm.add_grabber("sdl_wiki")
# gm.add_grabber("open_gl")