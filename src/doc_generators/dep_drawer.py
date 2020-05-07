from math import fabs
from PIL import Image, ImageDraw, ImageFont

class DependencyTree:
	depth = None
	save_path = None
	width = 500
	height = 500
	icon_size = 40
	font = "./conf/open-sans/OpenSans-Light.ttf"
	name_font = ImageFont.truetype(font, 15)
	connect_font = ImageFont.truetype(font, 10)
	
	def __init__(self, gen_path):
		self.save_path = gen_path+"/deps.png"
		self.image = Image.new("RGB", (self.width, self.height), color="white")
		self.draw = ImageDraw.Draw(self.image)
	
	def set_depth(self, depth):
		self.depth = depth
		self.step_y = float(self.height) / (depth+1)
	
	def save(self):
		self.image.save(self.save_path)
	
	def draw_node(self, record, layer, num, layer_size):
		step_x = float(self.width) / (layer_size+1)
		x1 = (num+1) * step_x
		y1 = (self.depth - layer) * self.step_y + self.icon_size
		x2 = x1 + self.icon_size
		y2 = y1 + self.icon_size
		self.draw.line((x1, y1, x2, y1), fill="black", width=2)
		self.draw.line((x1, y2, x2, y2), fill="black", width=2)
		
		w, h = self.draw.textsize(f"{record.kind}:{record.name}", font=self.name_font)
		text_x = (x1+x2)/2 - w/2
		text_y = (y1+y2)/2 - h/2
		self.draw.text((text_x, text_y), f"{record.kind}:{record.name}", font=self.name_font, fill="black")

	def connect(self, node1, node2, connection_type):
		layer, num, layer_size = node1
		step_x = float(self.width) / (layer_size+1)
		x1 = (num+1) * step_x + self.icon_size/2
		y1 = (self.depth - layer) * self.step_y + self.icon_size
		
		layer, num, layer_size = node2
		step_x = float(self.width) / (layer_size+1)
		x2 = (num+1) * step_x + self.icon_size/2
		y2 = (self.depth - layer) * self.step_y + 2*self.icon_size
		self.draw.line((x1, y1, x2, y2), fill="black")
		
		w, h = self.draw.textsize(connection_type, font=self.connect_font)
		text_x = (x1+x2)/2 - w/2
		text_y = (y1+y2)/2 - h/2
		
		self.draw.rectangle((text_x, text_y, text_x+w, text_y+h), fill="white")
		self.draw.text((text_x, text_y), connection_type, font=self.connect_font, fill="black")
	
class DependenciesDrawer:
	# типа связей между записями
	connections = {
		"file in file": "include",
		"class in file": "inner",
		"function in file": "inner",
		"enum in file": "inner",
		"function in class": "member",
	}
	def __init__(self, gen_path):
		self.dep_tree = DependencyTree(gen_path)
	def draw(self, record, id_table):
		self.dep_tree.set_depth( self.calculate_depth(record, id_table) )
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
		
	def draw_level(self, record, id_table, layer=1, num=0, layer_size=1):
		self.dep_tree.draw_node(record, layer, num, layer_size)
		if not record.parents_id:
			return
		parents = []
		for id in record.parents_id:
			parents.append(id_table.get_record_by_id(id))
		for i, parent in enumerate(parents):
			self.draw_level(parent, id_table, layer+1, i, len(parents))
			try:
				con_type = self.connections[f"{record.kind} in {parent.kind}"]
			except:
				print(f"Index error in dep_drawer connections {record.kind} in {parent.kind}")
				input()
			self.dep_tree.connect((layer, num, layer_size), (layer+1, i, len(parents)), con_type)