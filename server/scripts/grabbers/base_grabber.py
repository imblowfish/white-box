import requests as req
import json
import time
import os
import random
import codecs
"""
	Модуль базового класса грабберов
"""
class BaseGrabber:
	# заголовок для страницы
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
		"""
			Получение содержимого страницы по url
		"""
		page = req.get(url)
		if page.status_code != 200:
			print(f"Parse {url} error")
			return
		return page
		
	def save_json(self, path, data):
		"""
			Сохранение в json
		"""
		try:
			with open(path, "w") as file:
				json.dump(data, file)
		except:
			print(f"Error with writing json {path}")
			return False
		return True
			
	def save_html(self, path, ident_name, data):
		"""
			Сохранение содержимого url в локальную html страницу в заданной директории по имени граббера
		"""
		print(f"Try save in {path}/pages/{ident_name}")
		try:
			with codecs.open(f"{path}/pages/{ident_name}.html", "w", "utf8") as file:
				file.write(self.header % str(data))
		except:
			print(f"Error with writing html {ident_name}")
			return False
		return True

	def has_ident(self, ident_name):
		"""
			Проверка наличия идентификатора в директории граббера
		"""
		page_path = f"{self.dir}/pages/{ident_name}.html"
		if not os.path.exists(page_path):
			return False
		return True
		
	def parse(self):
		"""
			Разбор html-страницы
		"""
		idents = self.parse_idents_list()
		if not idents:
			print("Error with parsing")
			return
		for key in idents:
			if not self.parse_page(key, idents[key]):
				print(f"Error with parsing page {key}")
				return
			time.sleep(random.randint(2, 30))
		return True
			
	def parse_idents_list(self, path):
		"""
			Функция разбора списка идентификаторов, будет реализована в наследниках
		"""
		pass
		
	def parse_page(self, path, ident_name):
		"""
			Функция разбора html-страницы, будет реализована в наследниках
		"""
		pass