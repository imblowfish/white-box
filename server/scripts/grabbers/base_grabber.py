import requests as req
import json
import time
import os
import random

class BaseGrabber:
	header = f"\
	<!DOCTYPE html>\
	<html>\
	<head>\
	<link rel='stylesheet' type='text/css' href='../style/style.css'>\
	</head>\
	<body>\
	%s\
	</body>\
	</html>\
	"
	def get_page(self, url):
		page = req.get(url)
		if page.status_code != 200:
			print(f"Parse {url} error")
			return
		return page
		
	def save_json(self, path, data):
		try:
			with open(path, "w") as file:
				json.dump(data, file)
		except:
			print(f"Error with writing json {path}")
			return False
		return True
			
	def save_html(self, path, ident_name, data):
		try:
			with open(f"{path}/pages/{ident_name}.html", "w") as file:
				file.write(self.header % str(data))
		except:
			print(f"Error with writing html {ident_name}")
			return False
		return True

	def has_ident(self, ident_name):
		page_path = f"{self.dir}/pages/{ident_name}.html"
		if not os.path.exists(page_path):
			return False
		return True
		
	def parse(self):
		idents = self.parse_idents_list()
		if not idents:
			print("Error with parsing")
			return
		for key in idents:
			if not self.parse_page(key, idents[key]):
				print(f"Error with parsing page {key}")
				return
			print(f"Parsing {key} ended")
			time.sleep(random.randint(2, 30))
		return True
			
	def parse_idents_list(self, path):
		pass
		
	def parse_page(self, path, ident_name, url):
		pass