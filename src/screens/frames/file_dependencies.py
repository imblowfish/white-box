import tkinter as tk
import tkinter.ttk as ttk
import math
from .base_frame import BaseFrame

class FileDependenciesFrame(BaseFrame):
	prev_x = None
	prev_y = None
	
	def init_widgets(self):
		self.bind("<Configure>", self.resize)
		self.canvas = tk.Canvas(self, bg="white")
		self.canvas.pack(fill=tk.BOTH)
		
	def bind_commands(self):
		self.bind("<Configure>", self.resize)
		self.canvas.bind("<MouseWheel>", self.scale)
		self.canvas.bind("<B1-Motion>", self.move)
		self.canvas.bind("<ButtonRelease-1>", self.reset)
	
	def resize(self, event):
		wscale = float(event.width)/float(self.canvas["width"])
		hscale = float(event.height)/float(self.canvas["height"])
		self.canvas.configure(width=event.width, height=event.height)
		self.canvas.scale("all", 0, 0, wscale, hscale)	
		
	def scale(self, event):
		wscale, hscale = 0, 0
		center_x, center_y = float(self.canvas["width"])/2, float(self.canvas["height"])/2
		if event.delta < 0:
			wscale=0.5
			hscale=0.5
		else:
			wscale=1.5
			hscale=1.5
		self.canvas.scale("all", center_x, center_y, wscale, hscale)
		
	def move(self, event):
		if self.prev_x and self.prev_y:
			delta_x = event.x - self.prev_x
			delta_y = event.y - self.prev_y
			self.canvas.move("all", delta_x, delta_y)
		self.prev_x = event.x
		self.prev_y = event.y
	
	def reset(self, event):
		self.prev_x = None
		self.prev_y = None
	
	def show(self, records, id_table):
		self.canvas.delete("all")
		files = []
		for record in records:
			if record.kind == "file":
				files.append(record.name)
		num_of_files = len(files)
		alpha = (2 * math.pi)/num_of_files
		dt = 3 * math.pi / 2
		center_x = float(self.canvas["width"]) / 2
		center_y = float(self.canvas["height"]) / 2
		for record in records:
			if record.kind != "file":
				continue
			rec_idx = files.index(record.name)
			x1 = center_x + (math.sin(dt - rec_idx * alpha) * 180) / math.pi
			y1 = center_y + (math.cos(dt - rec_idx * alpha) * 180) / math.pi
			self.canvas.create_text(x1, y1, text=record.name, font=(None, 6))
			if not record.parents_id:
				continue
			for id in record.parents_id:
				parent = id_table.get_record_by_id(id)
				if parent.kind != "file":
					continue
				par_idx = files.index(parent.name)
				x2 = center_x + (math.sin(dt - par_idx * alpha) * 180) / math.pi
				y2 = center_y + (math.cos(dt - par_idx * alpha) * 180) / math.pi
				self.canvas.create_line(x2, y2, x1, y1, arrow=tk.LAST)