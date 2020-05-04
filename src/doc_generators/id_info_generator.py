import os
from .dep_drawer import DependenciesDrawer
from .html_generator import HTMLGenerator

class IDInfoGenerator:
	generate_path = "./temp/html"
	def __init__(self):
		# очистка директории, в которой могут быть файлы
		if os.path.exists(f"{self.generate_path}/id_info.html"):
			os.remove(f"{self.generate_path}/id_info.html")
			os.remove(f"{self.generate_path}/deps.png")
	def generate(self, record, id_table, mentions):
		# генерация html с отображением членов записи
		html_gen = HTMLGenerator(self.generate_path)
		html_gen.generate_id_info_html(record, mentions, id_table)
		# отрисовка зависимостей от родительских элементов
		dep_drawer = DependenciesDrawer(self.generate_path)
		dep_drawer.draw(record, id_table)