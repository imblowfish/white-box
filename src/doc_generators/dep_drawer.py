from math import fabs
from PIL import Image, ImageDraw, ImageFont

class DependencyTree:
	depth = None
	save_path = None
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
		self.depth = depth
		self.step_y = float(self.height) / (depth+1)
	
	def save(self):
		# print("save")
		self.image.save(self.save_path)
	
	def draw_node(self, record, layer, layer_size):
		step_x = float(self.width) / (layer_size+1)
		num = layer_size - self.levels[layer]
		x1 = (num+1) * step_x
		y1 = (self.depth - layer) * self.step_y + self.icon_size
		x2 = x1 + self.icon_size
		y2 = y1 + self.icon_size
		if layer == 0:
			self.draw.line((x1, y1, x2, y1), fill=self.line_color, width=2)
			self.draw.line((x1, y2, x2, y2), fill=self.line_color, width=2)
		else:
			self.draw.line((x1, y1, x2, y1), fill=self.line_color, width=2)
			self.draw.line((x1, y2, x2, y2), fill=self.line_color, width=2)
		
		w, h = self.draw.textsize(f"{record.name}", font=self.name_font)
		text_x = (x1+x2)/2 - w/2
		text_y = (y1+y2)/2 - h/2
		self.draw.text((text_x, text_y), f"{record.name}", font=self.name_font, fill=self.font_color)
		self.levels[layer] -= 1

	def connect(self, node1, node2, connection_type):
		layer, num, layer_size = node1
		step_x = float(self.width) / (layer_size+1)
		x1 = (num+1) * step_x + self.icon_size/2
		y1 = (self.depth - layer) * self.step_y + self.icon_size

		layer, layer_size = node2
		num = layer_size - self.c_levels[layer]
		step_x = float(self.width) / (layer_size+1)
		x2 = (num+1) * step_x + self.icon_size/2
		y2 = (self.depth - layer) * self.step_y + 2*self.icon_size
		self.c_levels[layer] -=1
		self.draw.line((x1, y1, x2, y2), fill=self.line_color)
		
		w, h = self.draw.textsize(connection_type, font=self.connect_font)
		text_x = (x1+x2)/2 - w/2
		text_y = (y1+y2)/2 - h/2
		
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
		self.dep_tree.set_depth( self.calculate_depth(record, id_table) )
		self.levels = [0] * (self.dep_tree.depth+1)
		self.calculate_num_on_layers(record, id_table)
		self.dep_tree.levels = self.levels.copy()
		self.dep_tree.c_levels = self.levels.copy()
		self.draw_level(record, id_table)
		self.dep_tree.save()
		
	def calculate_depth(self, record, id_table, now_depth=1):
		if not record.parents_id:
			return 1
		max_depth = 0
		for id in record.parents_id:
			parent = id_table.get_record_by_id(id)
			parent_depth = self.calculate_depth(parent, id_table)
			if parent_depth > max_depth:
				max_depth = parent_depth
		return now_depth+max_depth
		
	def calculate_num_on_layers(self, record, id_table, layer=0):
		print(layer)
		self.levels[layer] += 1
		if record.parents_id:
			for id in record.parents_id:
				parent = id_table.get_record_by_id(id)
				self.calculate_num_on_layers(parent, id_table, layer+1)
		if record.bases_id:
			for id in record.bases_id:
				base = id_table.get_record_by_id(id)
				self.calculate_num_on_layers(base, id_table, layer+1)
				
	def draw_level(self, record, id_table, layer=0, num=0):
		l_size = self.levels[layer]
		self.dep_tree.draw_node(record, layer, l_size)
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
		# if not record.parents_id and not record.bases_id:
			# return
		# parents_cnt = 0
		# if record.parents_id:
			# parents_cnt += len(record.parents_id)
		# bases_cnt = 0
		# if record.bases_id:
			# bases_cnt += len(record.bases_id)
		# sum_size = parents_cnt
		# if record.parents_id:
			# sum_size = len(record.parents_id)
			# print(record.name, sum_size)
			# parents = []
			# for id in record.parents_id:
				# parents.append(id_table.get_record_by_id(id))
			# for i, parent in enumerate(parents):
				# print(i, sum_size)
				# self.draw_level(parent, id_table, layer+1, i, sum_size)
				# try:
					# con_type = self.connections[f"{record.kind} in {parent.kind}"]
				# except:
					# print(f"Index error in dep_drawer connections {record.kind} in {parent.kind}")
					# input()
				# self.dep_tree.connect((layer, num, layer_size), (layer+1, i, sum_size), con_type)
		# if record.bases_id:
			# bases = []
			# for id in record.bases_id:
				# bases.append(id_table.get_record_by_id(id))
			# for i, base in enumerate(bases):
				# self.draw_level(base, id_table, layer+1, parents_cnt+i, sum_size)
				# try:
					# con_type = self.connections[f"{record.kind} in {base.kind} inh"]
				# except:
					# print(f"Index error in dep_drawer connections {record.kind} in {base.kind}")
					# input()
				# self.dep_tree.connect((layer, num, layer_size), (layer+1, parents_cnt+i, sum_size), con_type)