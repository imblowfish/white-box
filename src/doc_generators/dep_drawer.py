from math import fabs
from PIL import Image, ImageDraw, ImageFont

"""
	Генератор визуализации зависимостей для выбранного пользователем идентификатора
"""

class DependencyTree:
	depth = None # глубина дерева зависимостей
	save_path = None # путь для сохранения изображения
	width = 500
	height = 500
	icon_size = 20
	font = "./conf/open-sans/OpenSans-Bold.ttf"
	name_font = ImageFont.truetype(font, 12)
	connect_font = ImageFont.truetype(font, 12)
	bg_color = "#3c3836"
	font_color = "white"
	line_color = "#83a598"
	
	def __init__(self, gen_path):
		self.save_path = gen_path+"/deps.png"
		self.image = Image.new("RGB", (self.width, self.height), color=self.bg_color)
		self.draw = ImageDraw.Draw(self.image)
	
	def set_depth(self, depth):
		"""
			Установка глубины дерева
			Сразу расчитывает шаг по y для элементов зависимостей
		"""
		self.depth = depth
		self.step_y = float(self.height) / (depth+1)
	
	def save(self):
		self.image.save(self.save_path)
	
	def draw_node(self, record, layer, layer_size):
		"""
			Отрисовка узла
			Принимает запись из id-таблицы, номер ее слоя и кол-во эл-ов в слое
		"""
		# рассчитывается шаг по x для элементов
		step_x = float(self.width) / (layer_size+1)
		# узнаем порядковый номер элемента на уровне
		num = layer_size - self.levels[layer]
		# определяем точки
		x1 = (num+1) * step_x
		y1 = (self.depth - layer) * self.step_y + self.icon_size
		x2 = x1 + self.icon_size
		y2 = y1 + self.icon_size
		# отрисовываем линии
		self.draw.line((x1, y1, x2, y1), fill=self.line_color, width=2)
		self.draw.line((x1, y2, x2, y2), fill=self.line_color, width=2)
		# узнаем, сколько потребуется ширины и высоты под имя записи id-таблицы
		w, h = self.draw.textsize(f"{record.name}", font=self.name_font)
		# определяем координаты, чтобы текст не съехал
		text_x = (x1+x2)/2 - w/2
		text_y = (y1+y2)/2 - h/2
		self.draw.text((text_x, text_y), f"{record.name}", font=self.name_font, fill=self.font_color)
		# т.к. отрисовали один элемент, уменьшаем кол-во на уровне на 1
		self.levels[layer] -= 1

	def connect(self, node1, node2, connection_type):
		"""
			Функция связи 2 узлов
			Принимает кортежи node1 и node2 состоящие из: слоя, номера элемента в слое и кол-во элементов в слое
			Также принимает текст-обозначение связи
		"""
		# рассчитываем координаты 2 узлов
		layer, num, layer_size = node1
		step_x = float(self.width) / (layer_size+1)
		x1 = (num+1) * step_x + self.icon_size/2
		y1 = (self.depth - layer) * self.step_y + self.icon_size

		layer, layer_size = node2
		num = layer_size - self.c_levels[layer]
		step_x = float(self.width) / (layer_size+1)
		x2 = (num+1) * step_x + self.icon_size/2
		y2 = (self.depth - layer) * self.step_y + 2*self.icon_size
		# уменьшаем количество элементов в массиве слоев для связи, чтобы при следующей прорисовке не было сдвигов
		self.c_levels[layer] -=1
		self.draw.line((x1, y1, x2, y2), fill=self.line_color)
		# находим координату центра между 2мя узлами
		w, h = self.draw.textsize(connection_type, font=self.connect_font)
		text_x = (x1+x2)/2 - w/2
		text_y = (y1+y2)/2 - h/2
		# отрисовываем
		self.draw.rectangle((text_x, text_y, text_x+w, text_y+h), fill=self.bg_color)
		self.draw.text((text_x, text_y), connection_type, font=self.connect_font, fill=self.font_color)
	
class DependenciesDrawer:
	# типа связей между записями
	connections = {
		"file in file": "include",
		"class in file": "inner",
		"class in class": "member",
		"function in file": "inner",
		"var in file": "inner",
		"enum in file": "inner",
		"function in class": "member",
		"variable in class": "member",
		"enum in class": "member",
		"class in class inh": "inheritor",
		"enum_value in enum": "value"
	}
	levels = None
	
	def __init__(self, gen_path):
		self.dep_tree = DependencyTree(gen_path)
	def draw(self, record, id_table):
		"""
			Отрисовка зависимостей идентификатора
			Принимает запись id-таблицы и саму id-таблицу
		"""
		# определяем глубину дерева
		self.dep_tree.set_depth( self.calculate_depth(record, id_table) )
		# создаем массив из числа строк = глубине
		self.levels = [0] * (self.dep_tree.depth+1)
		# рассчитываем, сколько узлов на каждом слое
		self.calculate_num_on_layers(record, id_table)
		# устанвливаем вспомогательные массивы для отрисовщика
		self.dep_tree.levels = self.levels.copy()
		self.dep_tree.c_levels = self.levels.copy()
		# отрисовываем
		self.draw_level(record, id_table)
		self.dep_tree.save()
		
	def calculate_depth(self, record, id_table, now_depth=1):
		"""
			Расчет глубины дерева связей
		"""
		if not record.parents_id:
			return 1
		max_depth = 0
		# рекурсивно обходим узлы вглубь, считая глубину
		for id in record.parents_id:
			parent = id_table.get_record_by_id(id)
			parent_depth = self.calculate_depth(parent, id_table)
			if parent_depth > max_depth:
				max_depth = parent_depth
		return now_depth+max_depth
		
	def calculate_num_on_layers(self, record, id_table, layer=0):
		"""
			Расчет количества узлов на каждой слое
		"""
		self.levels[layer] += 1
		# рекурсивно обходим родителей записи
		if record.parents_id:
			for id in record.parents_id:
				parent = id_table.get_record_by_id(id)
				self.calculate_num_on_layers(parent, id_table, layer+1)
		# и базовые классы
		if record.bases_id:
			for id in record.bases_id:
				base = id_table.get_record_by_id(id)
				self.calculate_num_on_layers(base, id_table, layer+1)
				
	def draw_level(self, record, id_table, layer=0, num=0):
		"""
			Отрисовка дерева связей
		"""
		l_size = self.levels[layer]
		# отрисовываем узел записи
		self.dep_tree.draw_node(record, layer, l_size)
		# рекурсивно проходим по родителям записи
		if record.parents_id:
			for i, id in enumerate(record.parents_id):
				parent = id_table.get_record_by_id(id)
				self.draw_level(parent, id_table, layer+1, i)
				try:
					con_type = self.connections[f"{record.kind} in {parent.kind}"]
				except:
					print(f"Index error in dep_drawer connections {record.kind} in {parent.kind}")
				next_l_size = self.levels[layer+1]
				self.dep_tree.connect((layer, num, l_size), (layer+1, next_l_size), con_type)
		# и по базовым классам
		if record.bases_id:
			for i, id in enumerate(record.bases_id):
				base = id_table.get_record_by_id(id)
				self.draw_level(base, id_table, layer+1, i)
				try:
					con_type = self.connections[f"{record.kind} in {base.kind} inh"]
				except:
					print(f"Index error in dep_drawer connections {record.kind} in {base.kind} inh")
				next_l_size = self.levels[layer+1]
				self.dep_tree.connect((layer, num, l_size), (layer+1, next_l_size), con_type)