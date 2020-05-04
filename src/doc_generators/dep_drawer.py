from math import fabs
from PIL import Image, ImageDraw, ImageFont

class DependencyTree:
	save_path = None
	font = "./conf/open-sans/OpenSans-Light.ttf"
	levels = None
	width = 500
	height = 500
	def __init__(self, gen_path):
		self.save_path = gen_path+"/deps.png"
		self.image = Image.new("RGB", (self.width, self.height), color="white")
		self.draw = ImageDraw.Draw(self.image)
		self.levels = []
	def clear(self):
		self.levels = []
		self.draw.rectangle((0, 0, self.width, self.height), fill="white")
	def add_root(self, record):
		self.levels.append([(record.kind, record.name)])
	def add_next_level(self, records):
		level = []
		for record in records:
			level.append((record.kind, record.name))
		self.levels.append(level)
		
	def draw_image(self):
		depth = len(self.levels)
		step_y = float(self.height)/depth
		for i in range(depth):
			num_on_layer = len(self.levels[i])
			step_x = float(self.width) / (num_on_layer+1)
			for j in range(len(self.levels[i])):
				if i+1 >= depth:
					self.draw_node(self.levels[i][j], i, j+1, step_x, step_y, root=True)
				else:
					self.draw_node(self.levels[i][j], i, j+1, step_x, step_y)
		self.image.save(self.save_path)
					
	def draw_node(self, node, level, num, step_x, step_y, root=False):
		x1 = num * step_x
		y1 = level * step_y + 20
		x2 = x1 + float(self.width)/10
		y2 = y1 + float(self.height)/10
		if root:
			self.draw_kind(node[0], x1, y1, x2, y2, "red")
		else:
			self.draw_kind(node[0], x1, y1, x2, y2)
		self.draw.text((x1, y1), node[1], font=ImageFont.truetype(self.font), fill="black")
		
	def draw_kind(self, kind, x1, y1, x2, y2, color="black"):
		if kind == "file":
			self.draw.rectangle([x1, y1, x2, y2], outline=color)
		elif kind == "class":
			self.draw.ellipse([x1, y1, x2, y2], outline=color)
		
class DependenciesDrawer:
	def __init__(self, gen_path):
		self.dep_tree = DependencyTree(gen_path)
	def draw(self, record, id_table):
		self.dep_tree.clear()
		self.add_parents(record.parents_id, id_table)
		self.dep_tree.add_root(record)
		self.dep_tree.draw_image()
	def add_parents(self, parents_id, id_table):
		if not parents_id:
			return None
		parents = []
		for id in parents_id:
			parent = id_table.get_record_by_id(id, copy=True)
			if parent:
				parents.append(parent)
			self.add_parents(parent.parents_id, id_table)
		self.dep_tree.add_next_level(parents)